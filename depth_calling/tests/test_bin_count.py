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

import sys
import os
import pytest
import pysam


from ..bin_count import (
    get_read_count,
    get_read_length,
    mad,
    normalize,
    get_normed_depth,
)
from ..utilities import parse_region_file, open_alignment_file

test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")


class TestBinCount(object):
    def test_read_count_from_bam(self):
        bam = os.path.join(test_data_dir, "NA12878.bam")
        bamfile = open_alignment_file(bam)

        region1 = ("5", 69372349, 69372400)
        region1_count = get_read_count(bamfile, region1)
        assert region1_count == 11

        region2 = ("5", 70248246, 70248303)
        region2_count = get_read_count(bamfile, region2)
        assert region2_count == 30

        bamfile.close()

    def test_get_readlength(self):
        bam = os.path.join(test_data_dir, "NA12878.bam")
        bamfile = open_alignment_file(bam)
        reads = bamfile.fetch("5", 69372349, 70248303)
        read_length = get_read_length(reads)
        assert read_length == 150
        bamfile.close()

    def test_mad(self):
        list_number = [1, 2, 3, 4, 5]
        assert mad(list_number) == 1.4826
        list_number = [1, 2, 3, 4, 5, 6]
        assert mad(list_number) == 2.2239

    def test_normalize(self):
        counts_for_normalization = [0.3, 0.25, 0.3, 0.228, 0.29, 0.35, 0.31, 0.38, 0.42]
        gc_for_normalization = [0.42, 0.42, 0.43, 0.39, 0.4, 0.45, 0.43, 0.5, 0.6]
        region_type_cn = {"exon16": 2, "exon78": 2}
        norm = normalize(
            counts_for_normalization,
            gc_for_normalization,
            region_type_cn,
            150,
            gc_correct=False,
        )
        assert norm.normalized["exon16"] == 4
        assert round(norm.normalized["exon78"], 3) == 3.333
        assert norm.mediandepth == 45
        assert round(norm.mad, 5) == 0.057

    def test_bin_count(self):
        bam = os.path.join(test_data_dir, "NA12885.bam")
        region_file = os.path.join(test_data_dir, "SMN_region_37_short.bed")
        region_dic = parse_region_file(region_file)
        normed_depth = get_normed_depth(bam, region_dic, gc_correct=False)
        assert round(normed_depth.normalized["exon16"], 3) == 3.876
        assert round(normed_depth.normalized["exon78"], 3) == 4.024
        assert round(normed_depth.mediandepth, 2) == 48.75
        assert round(normed_depth.mad, 5) == 0.066
