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
from collections import namedtuple
import pytest

from ..call_smn12 import update_full_length_cn, get_smn12_call, smn1_cn_zero

SMA_CUTOFF = 1e-6
cn_call = namedtuple("cn_call", "exon16_cn exon16_depth exon78_cn exon78_depth")


class TestCN(object):
    def test_smn1_cn_zero(self):
        likelihood_ratio = smn1_cn_zero(0, 30, 30)
        assert likelihood_ratio > 1 / SMA_CUTOFF
        likelihood_ratio = smn1_cn_zero(15, 15, 30)
        assert likelihood_ratio < SMA_CUTOFF
        likelihood_ratio = smn1_cn_zero(2, 32, 30)
        assert likelihood_ratio < 1 / SMA_CUTOFF
        assert likelihood_ratio > SMA_CUTOFF
        likelihood_ratio = smn1_cn_zero(1, 32, 30)
        assert likelihood_ratio < 1 / SMA_CUTOFF
        assert likelihood_ratio > SMA_CUTOFF

    def test_update_full_length_cn(self):
        raw_cn_call = cn_call(3, 3.01, None, 3.44)
        updated_call = update_full_length_cn(raw_cn_call)
        assert updated_call == cn_call(3, 3.01, 3, 3.44)

        raw_cn_call = cn_call(3, 3.01, None, 2.77)
        updated_call = update_full_length_cn(raw_cn_call)
        assert updated_call == cn_call(3, 3.01, None, 2.77)

        raw_cn_call = cn_call(None, 2.15, 2, 2.17)
        updated_call = update_full_length_cn(raw_cn_call)
        assert updated_call == cn_call(2, 2.15, 2, 2.17)

        raw_cn_call = cn_call(None, 2.19, 2, 2.17)
        updated_call = update_full_length_cn(raw_cn_call)
        assert updated_call == cn_call(None, 2.19, 2, 2.17)

        raw_cn_call = cn_call(2, 2.1, 3, 2.7)
        updated_call = update_full_length_cn(raw_cn_call)
        assert updated_call == cn_call(2, 2.1, 2, 2.7)


class TestCallSMN12(object):
    # p5: total SMN, exon1-6
    # p3: full-length SMN, exon7-8
    # when p5 is no-call
    def test_p5_nocall(self):
        raw_cn_call = cn_call(None, 4.66, 4, 4.02)
        lsnp1 = [0, 0, 0, 0, 0, 0, 0, 15, 15, 15, 15, 15, 15, 15, 15, 15]
        lsnp2 = [0, 0, 0, 0, 0, 0, 0, 45, 45, 45, 45, 45, 45, 45, 45, 45]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 == 1
        assert final_call.SMN2 == 3
        # SMN* is a no-call
        assert final_call.SMN2delta78 is None
        assert final_call.isSMA is False
        assert final_call.isCarrier is True
        assert final_call.Info == "PASS:Majority"

    # when p3 is no-call but p3 depth value is larger than p5,
    # take CN(p5) as CN(p3)
    def test_p3_nocall_larger_than_p5(self):
        raw_cn_call = cn_call(4, 3.98, None, 4.66)
        lsnp1 = [0, 0, 0, 0, 0, 0, 0, 15, 15, 15, 15, 15, 15, 15, 15, 15]
        lsnp2 = [0, 0, 0, 0, 0, 0, 0, 45, 45, 45, 45, 45, 45, 45, 45, 45]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 == 1
        assert final_call.SMN2 == 3
        assert final_call.SMN2delta78 == 0
        assert final_call.isSMA is False
        assert final_call.isCarrier is True
        assert final_call.Info == "PASS:Majority"

    # ===========================================================================
    # when p3 is no-call, but we can call SMA based on read count
    # at splice site => isSMA
    def test_p3_nocall_issma(self):
        raw_cn_call = cn_call(None, 4.66, None, 3.46)
        lsnp1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        lsnp2 = [0, 0, 0, 0, 0, 0, 0, 45, 45, 45, 45, 45, 45, 45, 45, 45]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 == 0
        assert final_call.SMN2 == "3-4"
        assert final_call.SMN2delta78 is None
        assert final_call.isSMA is True
        assert final_call.isCarrier is False
        assert final_call.Info == "FLCNnoCall"

    # when p3 is no-call, #reads ambiguous at splice site => isSMA is no-call
    def test_p3_nocall_issma_nocall(self):
        raw_cn_call = cn_call(None, 4.66, None, 3.46)
        lsnp1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0]
        lsnp2 = [0, 0, 0, 0, 0, 0, 0, 45, 45, 45, 45, 45, 45, 45, 45, 45]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 is None
        assert final_call.SMN2 is None
        assert final_call.SMN2delta78 is None
        assert final_call.isSMA is None
        assert final_call.isCarrier is None
        assert final_call.Info == "FLCNnoCall"

    # when p3 is no-call, not SMA
    def test_p3_nocall_not_sma(self):
        raw_cn_call = cn_call(4, 3.98, None, 3.46)
        lsnp1 = [0, 0, 0, 0, 0, 0, 0, 15, 15, 15, 15, 15, 7, 15, 15, 15]
        lsnp2 = [0, 0, 0, 0, 0, 0, 0, 45, 45, 45, 45, 45, 45, 45, 45, 45]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 is None
        assert final_call.SMN2 is None
        assert final_call.SMN2delta78 is None
        # we can tell this sample is not SMA based on read count at splice site
        assert final_call.isSMA is False
        assert final_call.isCarrier is None
        assert final_call.Info == "FLCNnoCall"

    # ===========================================================================
    def test_carrier(self):
        raw_cn_call = cn_call(4, 3.98, 4, 4.02)
        lsnp1 = [0, 0, 0, 0, 0, 0, 0, 15, 15, 15, 15, 15, 15, 15, 15, 15]
        lsnp2 = [0, 0, 0, 0, 0, 0, 0, 45, 45, 45, 45, 45, 45, 45, 45, 45]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 == 1
        assert final_call.SMN2 == 3
        assert final_call.SMN2delta78 == 0
        assert final_call.isSMA is False
        assert final_call.isCarrier is True
        assert final_call.Info == "PASS:Majority"

    def test_sma(self):
        raw_cn_call = cn_call(4, 3.98, 3, 3.1)
        lsnp1 = [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0]
        lsnp2 = [0, 0, 0, 0, 0, 0, 0, 45, 45, 45, 45, 45, 45, 45, 45, 45]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 == 0
        assert final_call.SMN2 == 3
        assert final_call.SMN2delta78 == 1
        assert final_call.isSMA is True
        assert final_call.isCarrier is False
        assert final_call.Info == "PASS:Majority"

    def test_sma2_noise(self):
        raw_cn_call = cn_call(4, 3.98, 3, 3.1)
        lsnp1 = [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 3, 3, 1, 2]
        lsnp2 = [0, 0, 0, 0, 0, 0, 0, 45, 45, 45, 45, 45, 45, 45, 45, 45]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 == 0
        assert final_call.SMN2 == 3
        assert final_call.SMN2delta78 == 1
        assert final_call.isSMA is True
        assert final_call.isCarrier is False
        assert final_call.Info == "PASS:Majority"

    def test_not_carrier(self):
        raw_cn_call = cn_call(4, 3.98, 4, 4.02)
        lsnp1 = [0, 0, 0, 0, 0, 0, 0, 31, 36, 32, 31, 36, 32, 25, 28, 30]
        lsnp2 = [0, 0, 0, 0, 0, 0, 0, 26, 21, 31, 26, 21, 31, 30, 27, 29]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 == 2
        assert final_call.SMN2 == 2
        assert final_call.SMN2delta78 == 0
        assert final_call.isSMA is False
        assert final_call.isCarrier is False
        assert final_call.Info == "PASS:Majority"

    def test_not_carrier_majority_rule_agreewithsum(self):
        raw_cn_call = cn_call(4, 3.98, 4, 4.02)
        lsnp1 = [0, 0, 0, 0, 0, 0, 15, 21, 18, 42, 50, 45, 38, 21, 18, 12]
        lsnp2 = [0, 0, 0, 0, 0, 0, 25, 35, 37, 50, 30, 35, 20, 35, 37, 50]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 == 2
        assert final_call.SMN2 == 2
        assert final_call.SMN2delta78 == 0
        assert final_call.isSMA is False
        assert final_call.isCarrier is False
        assert final_call.Info == "PASS:AgreeWithSum"

    # check that the sites surrounding splice variant site are consistent with
    # overall call
    def test_not_carrier_majority_rule_splicedisagree(self):
        raw_cn_call = cn_call(4, 3.98, 4, 4.02)
        lsnp1 = [0, 0, 0, 0, 0, 0, 15, 15, 15, 15, 15, 15, 30, 30, 30, 30]
        lsnp2 = [0, 0, 0, 0, 0, 0, 45, 45, 45, 45, 45, 45, 30, 30, 30, 30]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 is None
        assert final_call.SMN2 is None
        assert final_call.SMN2delta78 == 0
        assert final_call.isSMA is False
        assert final_call.isCarrier is None
        assert final_call.Info == "SpliceDisagree"

    def test_smn1_nocall_ambiguous(self):
        raw_cn_call = cn_call(4, 3.98, 4, 4.02)
        lsnp1 = [0, 0, 0, 0, 0, 0, 12, 21, 18, 12, 50, 15, 38, 21, 18, 12]
        lsnp2 = [0, 0, 0, 0, 0, 0, 50, 35, 37, 50, 30, 35, 20, 35, 37, 50]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 is None
        assert final_call.SMN2 is None
        assert final_call.SMN2delta78 == 0
        assert final_call.isSMA is False
        assert final_call.isCarrier is None
        assert final_call.Info == "Ambiguous"

    def test_smn1_nocall_ambiguous_isSMA_false(self):
        raw_cn_call = cn_call(4, 3.98, 4, 4.02)
        lsnp1 = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 36, 32, 25, 28, 50]
        lsnp2 = [0, 0, 0, 0, 0, 0, 0, 55, 55, 55, 55, 21, 31, 30, 27, 29]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 is None
        assert final_call.SMN2 is None
        assert final_call.SMN2delta78 == 0
        assert final_call.isSMA is False
        assert final_call.isCarrier is None
        assert final_call.Info == "Ambiguous"

    # ===========================================================================
    def test_0smn1_0smn2(self):
        raw_cn_call = cn_call(0, 0, 0, 0)
        lsnp1 = [0] * 16
        lsnp2 = [0] * 16
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 == 0
        assert final_call.SMN2 == 0
        assert final_call.SMN2delta78 == 0
        assert final_call.isSMA is True
        assert final_call.isCarrier is False
        assert final_call.Info == "PASS:Majority"

    # ===========================================================================
    def test_target_variant(self):
        raw_cn_call = cn_call(4, 3.98, 4, 4.02)
        lsnp1 = [0, 0, 0, 0, 0, 0, 0, 31, 36, 32, 31, 36, 32, 25, 28, 30]
        lsnp2 = [0, 0, 0, 0, 0, 0, 0, 26, 21, 31, 26, 21, 31, 30, 27, 29]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [42], [16], 30)
        assert final_call.SMN1 == 2
        assert final_call.SMN2 == 2
        assert final_call.SMN2delta78 == 0
        assert final_call.isSMA is False
        assert final_call.isCarrier is False
        assert final_call.Info == "PASS:Majority"
        assert final_call.g27134TG_raw == round(4 * 16 / (42 + 16), 2)
        assert final_call.g27134TG_CN == 1

    def test_target_variant_larger_than_smn1cn(self):
        raw_cn_call = cn_call(4, 3.98, 4, 4.02)
        lsnp1 = [0, 0, 0, 0, 0, 0, 0, 31, 36, 32, 31, 36, 32, 25, 28, 30]
        lsnp2 = [0, 0, 0, 0, 0, 0, 0, 26, 21, 31, 26, 21, 31, 30, 27, 29]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [16], [42], 30)
        assert final_call.SMN1 == 2
        assert final_call.SMN2 == 2
        assert final_call.SMN2delta78 == 0
        assert final_call.isSMA is False
        assert final_call.isCarrier is False
        assert final_call.Info == "PASS:Majority"
        assert final_call.g27134TG_raw == round(4 * 42 / (42 + 16), 2)
        # called 3, update to be equal to SMN1 CN
        assert final_call.g27134TG_CN == 2

    # ======================== Corner Cases ===================================
    # in this extreme case, all sites look like SMA except the splice site
    # itself based on the majority rule SMN1 CN is called as 0
    # but we want to call isSMA to be no-call
    def test_corner1(self):
        raw_cn_call = cn_call(4, 3.98, 3, 3.1)
        lsnp1 = [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 7, 1, 1, 1]
        lsnp2 = [0, 0, 0, 0, 0, 0, 0, 45, 45, 45, 45, 45, 45, 45, 45, 45]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 == 0
        assert final_call.SMN2 == 3
        assert final_call.SMN2delta78 == 1
        assert final_call.isSMA is None
        assert final_call.isCarrier is None
        assert final_call.Info == "PASS:Majority"

    # all sites look like 1 and splice site looks like 0
    def test_corner2(self):
        raw_cn_call = cn_call(4, 3.98, 4, 4.1)
        lsnp1 = [0, 0, 0, 0, 0, 0, 15, 15, 15, 15, 15, 15, 0, 15, 15, 15]
        lsnp2 = [0, 0, 0, 0, 0, 0, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 == 1
        assert final_call.SMN2 == 3
        assert final_call.SMN2delta78 == 0
        assert final_call.isSMA is None
        assert final_call.isCarrier is None
        assert final_call.Info == "PASS:Majority"

    # a mixture of 0s and 1s so isSMA is no-call
    def test_corner3(self):
        raw_cn_call = cn_call(4, 3.98, 4, 4.1)
        lsnp1 = [0, 0, 0, 0, 0, 0, 3, 15, 5, 1, 0, 1, 6, 15, 25, 1]
        lsnp2 = [0, 0, 0, 0, 0, 0, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 is None
        assert final_call.SMN2 is None
        assert final_call.SMN2delta78 == 0
        assert final_call.isSMA is None
        assert final_call.isCarrier is None
        assert final_call.Info == "Ambiguous"

    # a mixture of 0s and 1s, but enough reads at splice site to say isSMA is
    # false
    def test_corner4(self):
        raw_cn_call = cn_call(4, 3.98, 4, 4.1)
        lsnp1 = [0, 0, 0, 0, 0, 0, 3, 15, 5, 1, 0, 1, 7, 15, 25, 1]
        lsnp2 = [0, 0, 0, 0, 0, 0, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 is None
        assert final_call.SMN2 is None
        assert final_call.SMN2delta78 == 0
        assert final_call.isSMA is False
        assert final_call.isCarrier is None
        assert final_call.Info == "Ambiguous"

    # all sites look like 2 and splice site looks like 0
    def test_corner5(self):
        raw_cn_call = cn_call(4, 3.98, 4, 4.1)
        lsnp1 = [0, 0, 0, 0, 0, 0, 30, 30, 30, 30, 30, 30, 0, 30, 30, 30]
        lsnp2 = [0, 0, 0, 0, 0, 0, 30, 30, 30, 30, 30, 30, 45, 30, 30, 30]
        final_call = get_smn12_call(raw_cn_call, lsnp1, lsnp2, [60], [0], 30)
        assert final_call.SMN1 == 2
        assert final_call.SMN2 == 2
        assert final_call.SMN2delta78 == 0
        assert final_call.isSMA is None
        assert final_call.isCarrier is False
        assert final_call.Info == "PASS:Majority"
