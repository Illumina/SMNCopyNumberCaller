#!/usr/bin/env python3
#
# SMNCopyNumberCaller
# Copyright (c) 2019 Illumina, Inc.
#
# Author: Xiao Chen <xchen2@illumina.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import argparse
import json
import logging
import datetime
from collections import namedtuple
import pysam


from depth_calling.snp_count import get_supporting_reads, get_fraction, \
    get_snp_position
from depth_calling.gmm import Gmm
from depth_calling.utilities import parse_gmm_file, parse_region_file
from depth_calling.bin_count import get_normed_depth, \
    get_normed_depth_from_count, get_read_length
from caller.call_smn12 import get_smn12_call

MAD_THRESHOLD = 0.11


def load_parameters():
    """Return parameters."""
    parser = argparse.ArgumentParser(
        description='Call Copy number of full-length SMN1, full-length SMN2 and \
        SMN* (Exon7-8 deletion) from a WGS bam file.')
    parser.add_argument(
        '--manifest', help='Manifest listing absolute paths to bam files',
        required=True)
    parser.add_argument(
        '--genome', help='Reference genome, select from 19, 37, or 38',
        required=True)
    parser.add_argument(
        '--outDir', help='Output directory', required=True)
    parser.add_argument(
        '--prefix', help='Prefix to output file', required=True)
    parser.add_argument(
        '--threads', help='Number of threads to use', type=int, default=1,
        required=False)
    parser.add_argument(
        '--countFilePath', help='Path to count files', required=False)

    args = parser.parse_args()
    if args.genome not in ['19', '37', '38']:
        raise Exception('Genome not recognized. Select from 19, 37, or 38')

    return args


def smn_cn_caller(
        bam, region_dic, gmm_parameter,
        snp_db, variant_db, threads, count_file=None):
    """Return SMN CN calls for each sample."""
    # 1. read counting, normalization
    if count_file is not None:
        bamfile = pysam.AlignmentFile(bam, "rb")
        reads = bamfile.fetch()
        read_length = get_read_length(reads)
        bamfile.close()
        normalized_depth = get_normed_depth_from_count(
            count_file, region_dic, read_length, gc_correct=False)
    else:
        normalized_depth = get_normed_depth(
            bam, region_dic, threads, gc_correct=False)

    # 2. GMM and CN call
    cn_call = namedtuple(
        'cn_call', 'exon16_cn exon16_depth exon78_cn exon78_depth'
    )
    gmm_exon16 = Gmm()
    gmm_exon16.set_gmm_par(gmm_parameter, 'exon1-6')
    gcall_exon16 = gmm_exon16.gmm_call(normalized_depth.normalized['exon16'])
    gmm_exon78 = Gmm()
    gmm_exon78.set_gmm_par(gmm_parameter, 'exon7-8')
    gcall_exon78 = gmm_exon78.gmm_call(normalized_depth.normalized['exon78'])
    raw_cn_call = cn_call(
        gcall_exon16.cn, gcall_exon16.depth_value,
        gcall_exon78.cn, gcall_exon78.depth_value
    )

    # 3. Get SNP ratios
    smn1_read_count, smn2_read_count = get_supporting_reads(
        bam, snp_db.dsnp1, snp_db.dsnp2, snp_db.nchr, snp_db.dindex
    )
    smn1_fraction = get_fraction(smn1_read_count, smn2_read_count)
    var_ref_count, var_alt_count = get_supporting_reads(
        bam, variant_db.dsnp1, variant_db.dsnp2, variant_db.nchr,
        variant_db.dindex
    )

    # 4. Call CN of SMN1 and SMN2
    final_call = get_smn12_call(
        raw_cn_call, smn1_read_count, smn2_read_count,
        var_ref_count, var_alt_count,
        normalized_depth.mediandepth
    )

    # 5. Prepare final call set
    sample_call = namedtuple(
        'sample_call',
        'Coverage_MAD \
        Full_length_CN_raw Total_CN_raw \
        SMN1_read_support SMN2_read_support SMN1_fraction \
        g27134TG_REF_count g27134TG_ALT_count'
    )
    sample_cn_call = sample_call(
        round(normalized_depth.mad, 3),
        raw_cn_call.exon78_depth, raw_cn_call.exon16_depth,
        smn1_read_count, smn2_read_count, [round(a, 2) for a in smn1_fraction],
        var_ref_count, var_alt_count
    )

    doutput = sample_cn_call._asdict()
    doutput.update(final_call._asdict())
    return doutput


def write_to_tsv(final_output, out_tsv):
    """Write to tsv output."""
    header = [
        'Sample', 'isSMA', 'isCarrier', 'SMN1_CN', 'SMN2_CN', 'SMN*_CN',
        'Total_CN_raw', 'Full_length_CN_raw', 'g.27134T>G_CN',
        'SMN1_CN_raw'
    ]
    with open(out_tsv, 'w') as tsv_output:
        tsv_output.write('\t'.join(header)+'\n')
        for sample_id in final_output:
            final_call = final_output[sample_id]
            output_per_sample = [
                sample_id, final_call['isSMA'], final_call['isCarrier'],
                final_call['SMN1'], final_call['SMN2'], final_call['SMNstar'],
                final_call['Total_CN_raw'], final_call['Full_length_CN_raw'],
                final_call['g27134TG_CN'],
                ','.join([str(a) for a in final_call['SMN1_CN_raw']])
            ]
            tsv_output.write('\t'.join([str(a)
                                        for a in output_per_sample]) + '\n')


def main():
    parameters = load_parameters()
    manifest = parameters.manifest
    outdir = parameters.outDir
    genome = parameters.genome
    prefix = parameters.prefix
    threads = parameters.threads
    path_count_file = parameters.countFilePath
    logging.basicConfig(level=logging.DEBUG)

    datadir = os.path.join(os.path.dirname(__file__), "data")
    # Region file to use
    region_file = os.path.join(datadir, "SMN_region_%s.bed" % genome)
    snp_file = os.path.join(datadir, "SMN_SNP_%s.txt" % genome)
    variant_file = os.path.join(datadir, "SMN_target_variant_%s.txt" % genome)
    gmm_file = os.path.join(datadir, "SMN_gmm.txt")

    for required_file in [region_file, snp_file, variant_file, gmm_file]:
        if os.path.exists(required_file) == 0:
            raise Exception('File %s not found.' % required_file)

    if os.path.exists(outdir) == 0:
        os.makedirs(outdir)

    snp_db = get_snp_position(snp_file)
    variant_db = get_snp_position(variant_file)
    gmm_parameter = parse_gmm_file(gmm_file)
    region_dic = parse_region_file(region_file)
    out_json = os.path.join(outdir, prefix + '.json')
    out_tsv = os.path.join(outdir, prefix + '.tsv')
    final_output = {}
    with open(manifest) as read_manifest:
        for line in read_manifest:
            bam_name = line.strip()
            sample_id = os.path.splitext(os.path.basename(bam_name))[0]
            count_file = None
            if path_count_file is not None:
                count_file = os.path.join(
                    path_count_file, sample_id + '_count.txt')
            if count_file is None and os.path.exists(bam_name) == 0:
                logging.warning(
                    'Input bam file for sample %s does not exist.', sample_id)
            elif count_file is not None and os.path.exists(count_file) == 0:
                logging.warning(
                    'Input count file for sample %s does not exist', sample_id)
            else:
                logging.info(
                    'Processing sample %s at %s', sample_id,
                    datetime.datetime.now()
                )
                smn_call = smn_cn_caller(
                    bam_name, region_dic, gmm_parameter,
                    snp_db, variant_db, threads, count_file
                )
                # Use normalized coverage MAD across stable regions
                # as a sample QC measure.
                if smn_call['Coverage_MAD'] > MAD_THRESHOLD:
                    logging.warning(
                        "Sample %s has uneven coverage. CN calls may be \
                            unreliable.", sample_id)
                final_output.setdefault(sample_id, smn_call)

    # Write to json
    logging.info('Writing to json at %s', datetime.datetime.now())
    with open(out_json, 'w') as json_output:
        json.dump(final_output, json_output)

    # Write to tsv
    logging.info('Writing to tsv at %s', datetime.datetime.now())
    write_to_tsv(final_output, out_tsv)


if __name__ == "__main__":
    main()
