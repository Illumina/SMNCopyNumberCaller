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


import os
import sys

dir_name = os.path.join(os.path.dirname(os.path.dirname(__file__)), "depth_calling")
if os.path.exists(dir_name):
    sys.path.append(dir_name)
from depth_calling.copy_number_call import call_reg1_cn, process_raw_call_denovo


def call_cn_var_homo(total_cn, lsnp1, lsnp2, max_cn=None):
    """
    Call CN for variant sites in homology regions.
    """
    cn_prob = []
    for i, count1 in enumerate(lsnp1):
        count2 = lsnp2[i]
        cn_prob.append(call_reg1_cn(total_cn, count1, count2, 4))
    cn_call = []
    for site_call in process_raw_call_denovo(cn_prob, 0.8, 0.65):
        if site_call is None:
            cn_call.append(None)
        else:
            if max_cn is None:
                cn_call.append(min(site_call, total_cn - 2))
            else:
                cn_call.append(min(site_call, max_cn))
    return cn_call


def get_called_variants(var_list, cn_prob_processed, starting_index=0):
    """
    Return called variant names based on called copy number and list of variant names
    """
    total_callset = []
    if starting_index != 0:
        assert len(var_list) == len(cn_prob_processed) + starting_index
    for i, cn_called in enumerate(cn_prob_processed):
        if cn_called is not None and cn_called != 0:
            for _ in range(cn_called):
                total_callset.append(var_list[i + starting_index])
    return total_callset
