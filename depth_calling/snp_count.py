#!/usr/bin/env python3
#
# SMNCopyNumberCaller
# Copyright 2019-2020 Illumina, Inc.
# All rights reserved.
#
# Author: Xiao Chen <xchen2@illumina.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

from collections import namedtuple
import pysam
from .utilities import open_alignment_file


COMPLEMENT = {"A": "T", "T": "A", "C": "G", "G": "C", "N": "N"}
SITES_STRINGENT = []  # consider being more stringent for exon8 site for SMN


def reverse_complement(sequence):
    """Return the reverse complement of a sequence."""
    return "".join(COMPLEMENT[b] for b in sequence[::-1])


def get_nm(ltag):
    """Return the value of the NM tag."""
    for tag in ltag:
        if tag[0] == "NM":
            return tag[1]
    return None


def get_snp_position(pos_file):
    """Get all base differences listed in the SNP location file."""
    dsnp1 = {}
    dsnp2 = {}
    dindex = {}

    with open(pos_file) as read_pos:
        counter = -1
        for line in read_pos:
            if line[0] != "#" and line[0] != "\n":
                counter += 1
                split_line = line.strip().split()
                reg1_name = split_line[1] + "_" + str(counter)
                reg2_name = split_line[3] + "_" + str(counter)
                reg1_base = split_line[2].upper()
                reg2_base = split_line[4].upper()
                if split_line[-1] != "-":
                    dsnp1.setdefault(reg1_name, "_".join([reg1_base, reg2_base]))
                    dsnp2.setdefault(reg2_name, "_".join([reg1_base, reg2_base]))
                else:
                    dsnp1.setdefault(
                        reg1_name, "_".join([reg1_base, reverse_complement(reg2_base)])
                    )
                    dsnp2.setdefault(
                        reg2_name, "_".join([reverse_complement(reg1_base), reg2_base])
                    )
                dindex.setdefault(reg1_name, counter)
                dindex.setdefault(reg2_name, counter)
    nchr = split_line[0]
    snp_lookup = namedtuple("snp_lookup", "dsnp1 dsnp2 nchr dindex")
    dbsnp = snp_lookup(dsnp1, dsnp2, nchr, dindex)
    return dbsnp


def passing_read(pileupread):
    """Return whether a read passes filter."""
    return (
        not pileupread.is_del
        and not pileupread.is_refskip
        and pileupread.alignment.is_secondary == 0
        and pileupread.alignment.is_supplementary == 0
        and pileupread.alignment.is_duplicate == 0
    )


def passing_read_stringent(pileupread):
    """Return whether a read passes more stringent filter."""
    number_mismatch = get_nm(pileupread.alignment.tags)
    align_len = pileupread.alignment.query_alignment_length
    read_len = len(pileupread.alignment.query_sequence)
    return (
        number_mismatch <= float(align_len) * 0.08
        and pileupread.query_position > 0
        and pileupread.query_position < read_len - 1
    )


def get_reads_by_region(bamfile_handle, nchr, dsnp, dindex, min_mapq=0):
    """
    Return the number of reads supporting region1 and region2.
    """
    lsnp1 = [0] * len(dsnp)
    lsnp2 = [0] * len(dsnp)
    for snp_position_ori in dsnp:
        snp_position = int(snp_position_ori.split("_")[0])
        for pileupcolumn in bamfile_handle.pileup(
            nchr,
            snp_position - 1,
            snp_position + 1,
            truncate=True,
            stepper="nofilter",
            ignore_overlaps=False,
            ignore_orphan=False,
        ):
            site_position = pileupcolumn.pos + 1
            if site_position == snp_position:
                reg1_allele, reg2_allele = dsnp[snp_position_ori].split("_")
                for read in pileupcolumn.pileups:
                    if (
                        passing_read(read)
                        and read.alignment.mapping_quality >= min_mapq
                    ):
                        dsnp_index = dindex[snp_position_ori]
                        read_seq = read.alignment.query_sequence
                        if (
                            site_position not in SITES_STRINGENT
                            or passing_read_stringent(read)
                        ):
                            reg1_allele_split = reg1_allele.split(",")
                            reg2_allele_split = reg2_allele.split(",")
                            start_pos = read.query_position
                            for allele in reg1_allele_split:
                                end_pos = start_pos + len(allele)
                                if read_seq[start_pos:end_pos] == allele:
                                    lsnp1[dsnp_index] += 1
                            for allele in reg2_allele_split:
                                end_pos = start_pos + len(allele)
                                if read_seq[start_pos:end_pos] == allele:
                                    lsnp2[dsnp_index] += 1
    return lsnp1, lsnp2


def get_fraction(lsnp1, lsnp2):
    """Return the fraction of reads supporting region1."""
    reg1_fraction = []
    for index in range(len(lsnp1)):
        sumdepth = lsnp1[index] + lsnp2[index]
        if sumdepth == 0:
            reg1_fraction.append(0)
        else:
            reg1_fraction.append(float(lsnp1[index]) / float(sumdepth))
    return reg1_fraction


def get_supporting_reads(bamf, dsnp1, dsnp2, nchr, dindex, reference=None):
    """
    Return the number of supporting reads at each position in
    both region1 and region2.
    """
    bamfile_handle = open_alignment_file(bamf, reference)
    assert len(dsnp1) == len(dsnp2)
    # Go through SNP sites in both regions,
    # and count the number of reads supporting each gene.
    lsnp1_reg1, lsnp2_reg1 = get_reads_by_region(bamfile_handle, nchr, dsnp1, dindex)
    lsnp1_reg2, lsnp2_reg2 = get_reads_by_region(bamfile_handle, nchr, dsnp2, dindex)
    lsnp1 = [sum(x) for x in zip(lsnp1_reg1, lsnp1_reg2)]
    lsnp2 = [sum(x) for x in zip(lsnp2_reg1, lsnp2_reg2)]
    bamfile_handle.close()
    return lsnp1, lsnp2


def get_supporting_reads_single_region(bamf, dsnp1, nchr, dindex, reference=None):
    """
    Return the number of supporting reads at each position only in region1.
    """
    bamfile_handle = open_alignment_file(bamf, reference)
    lsnp1, lsnp2 = get_reads_by_region(bamfile_handle, nchr, dsnp1, dindex, 10)
    bamfile_handle.close()
    return lsnp1, lsnp2
