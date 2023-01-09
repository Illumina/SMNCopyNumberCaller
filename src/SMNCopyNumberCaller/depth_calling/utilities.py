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


def parse_region_file(region_file):
    """Return the set of regions for counting from a bed file."""
    region_dic = {}
    with open(region_file) as read_region:
        for line in read_region:
            nchr, region_start, region_end, region_name, region_type, region_gc = (
                line.strip().split()
            )
            region_start = int(region_start)
            region_end = int(region_end)
            region = (nchr, region_start, region_end, region_name)
            region_dic.setdefault(region_type, []).append((region, region_gc))
    return region_dic


def parse_gmm_file(gmm_file):
    """Return the gmm parameters stored in input file."""
    dpar_tmp = {}
    with open(gmm_file) as read_gmm:
        for line in read_gmm:
            split_line = line.strip().split()
            dpar_tmp.setdefault(split_line[0], {})
            list_value = [a.split(":")[-1] for a in split_line[2:]]
            dpar_tmp[split_line[0]].setdefault(split_line[1], list_value)
    return dpar_tmp


def open_alignment_file(alignment_file, reference_fasta=None):
    if alignment_file.endswith("cram"):
        return pysam.AlignmentFile(
            alignment_file, "rc", reference_filename=reference_fasta
        )
    return pysam.AlignmentFile(alignment_file, "rb")
