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


import math
import os
import sys
from collections import namedtuple, Counter
from scipy.stats import poisson

dir_name = os.path.join(os.path.dirname(os.path.dirname(__file__)), "depth_calling")
if os.path.exists(dir_name):
    sys.path.append(dir_name)
from depth_calling.copy_number_call import (
    call_reg1_cn,
    process_raw_call_gc,
    process_raw_call_denovo,
)

SMA_CUTOFF = 1e-6
TOTAL_NUM_SITES = 16
SELECTED_SITES_INDEX = [a - 1 for a in [7, 8, 10, 11, 12, 13, 14, 15]]
SPLICE_INDEX = 12
POSTERIOR_CUTOFF_STRINGENT = 0.9
POSTERIOR_CUTOFF_MEDIUM = 0.8
POSTERIOR_CUTOFF_LOOSE = 0.6
ERROR_RATE = 0.01


def safe_division(x, y):
    return 0 if y == 0 else x / y


def get_fraction(lsnp1, lsnp2):
    """Return the fraction of reads supporting SMN1."""
    return [safe_division(count1, count1 + lsnp2[i]) for i, count1 in enumerate(lsnp1)]


def smn1_cn_zero(count_smn1, count_smn2, mdepth):
    """Return the likelihood ratio between SMN1 CN=0 and SMN1 CN=1."""
    nsum = count_smn1 + count_smn2
    depthexpected0 = (ERROR_RATE / 3) * float(nsum)
    # haploid depth
    depthexpected1 = float(mdepth) / 2
    prob_cp0 = poisson.pmf(count_smn1, depthexpected0)
    prob_cp1 = poisson.pmf(count_smn1, depthexpected1)
    return prob_cp0 / prob_cp1


def get_raw_smn1_cn(full_length_cn, smn1_fraction):
    """
    Return the raw SMN1 CN by muliplying full-length SMN CN and SMN1 fraction.
    """
    lcount = []
    for site_fraction in smn1_fraction:
        lcount.append(round(full_length_cn * site_fraction, 2))
    return lcount


def update_full_length_cn(raw_cn_call):
    """Return the updated full-length SMN CN."""
    # full-length CN can't be higher than total CN
    cn_call = namedtuple("cn_call", "exon16_cn exon16_depth exon78_cn exon78_depth")
    if raw_cn_call.exon78_depth >= raw_cn_call.exon16_depth:
        if raw_cn_call.exon78_cn is None and raw_cn_call.exon16_cn is not None:
            updated_cn_call = cn_call(
                raw_cn_call.exon16_cn,
                raw_cn_call.exon16_depth,
                raw_cn_call.exon16_cn,
                raw_cn_call.exon78_depth,
            )
            return updated_cn_call
        if raw_cn_call.exon78_cn is not None and raw_cn_call.exon16_cn is None:
            updated_cn_call = cn_call(
                raw_cn_call.exon78_cn,
                raw_cn_call.exon16_depth,
                raw_cn_call.exon78_cn,
                raw_cn_call.exon78_depth,
            )
            return updated_cn_call
    if (
        raw_cn_call.exon78_cn is not None
        and raw_cn_call.exon16_cn is not None
        and raw_cn_call.exon16_cn < raw_cn_call.exon78_cn
    ):
        updated_cn_call = cn_call(
            raw_cn_call.exon16_cn,
            raw_cn_call.exon16_depth,
            raw_cn_call.exon16_cn,
            raw_cn_call.exon78_depth,
        )
        return updated_cn_call
    return raw_cn_call


def get_smn1_call_and_tag(cn_prob_all, combined_call):
    """Return the final SMN1 CN call and its tag value."""
    cn_prob = [cn_prob_all[a] for a in SELECTED_SITES_INDEX]
    lsitecall_stringent = process_raw_call_gc(
        cn_prob, POSTERIOR_CUTOFF_STRINGENT, keep_none=False
    )
    lsitecall_medium = process_raw_call_gc(
        cn_prob, POSTERIOR_CUTOFF_MEDIUM, keep_none=False
    )
    lsitecall_loose = process_raw_call_gc(
        cn_prob, POSTERIOR_CUTOFF_LOOSE, keep_none=False
    )

    lsitecall_medium_counter = sorted(
        Counter(lsitecall_medium).items(), key=lambda kv: kv[1], reverse=True
    )
    lsitecall_loose_counter = sorted(
        Counter(lsitecall_loose).items(), key=lambda kv: kv[1], reverse=True
    )

    # sliding window of three sites covering the splice site
    # [11, 12, 13], [12, 13, 14], [13, 14, 15] (1-based)
    if lsitecall_loose_counter != [] and lsitecall_loose_counter[0][1] >= 5:
        for i in [11, 12, 13]:
            sliding_window = [i, i + 1, i + 2]
            prob_window = [cn_prob_all[a - 1] for a in sliding_window]
            call_window_loose = process_raw_call_gc(
                prob_window, POSTERIOR_CUTOFF_LOOSE, keep_none=False
            )
            if len(call_window_loose) == 3 and (
                min(call_window_loose) > lsitecall_loose_counter[0][0]
                or max(call_window_loose) < lsitecall_loose_counter[0][0]
            ):
                cn_smn1 = None
                tag = "SpliceDisagree"
                return tag, cn_smn1, lsitecall_loose

    # At least 5 sites need to agree
    if lsitecall_medium_counter != [] and lsitecall_medium_counter[0][1] >= 5:
        tag = "PASS:Majority"
        cn_smn1 = lsitecall_medium_counter[0][0]
        return tag, cn_smn1, lsitecall_loose

    # When the call summing up all sites is very confident
    if (
        len(combined_call) == 1
        and lsitecall_loose_counter != []
        and combined_call[0] == lsitecall_loose_counter[0][0]
        and lsitecall_loose_counter[0][1] >= 5
    ):
        tag = "PASS:AgreeWithSum"
        cn_smn1 = lsitecall_loose_counter[0][0]
        return tag, cn_smn1, lsitecall_loose

    # The remaining ones will be no-call
    cn_smn1 = None
    tag = "Ambiguous"
    return tag, cn_smn1, lsitecall_loose


def get_sma_status(site_calls, cn_prob, cn_smn1, sma_likelihood_ratio):
    """Return the SMA status of the sample."""
    if 0 not in cn_prob[SPLICE_INDEX] and (
        sma_likelihood_ratio < SMA_CUTOFF or site_calls.count(0) <= 1
    ):
        if cn_smn1 == 0:
            return None
        else:
            return False
    if cn_smn1 is not None:
        if sma_likelihood_ratio > 1 / SMA_CUTOFF and cn_smn1 != 0:
            return None
        return bool(cn_smn1 == 0)
    return None


def get_carrier_status(site_calls, cn_prob, cn_smn1, sma_likelihood_ratio):
    """Return the carrier status of the sample."""
    if 1 not in cn_prob[SPLICE_INDEX] and len([a for a in site_calls if a <= 1]) <= 1:
        if cn_smn1 == 1:
            return None
        else:
            return False
    if cn_smn1 is not None:
        if sma_likelihood_ratio > 1 / SMA_CUTOFF and cn_smn1 == 1:
            return None
        if sma_likelihood_ratio < SMA_CUTOFF and cn_smn1 == 0:
            return None
        return bool(cn_smn1 == 1)
    return None


def get_smn12_call(raw_cn_call, lsnp1, lsnp2, var_ref, var_alt, mdepth):
    """Return the copy nubmer call of SMN1, SMN2 and SMNstar."""
    smn1_fraction = get_fraction(lsnp1, lsnp2)
    smn_call = namedtuple(
        "smn_call",
        "SMN1 SMN2 SMN2delta78 isCarrier isSMA \
        SMN1_CN_raw Info Confidence g27134TG_raw g27134TG_CN",
    )
    raw_cn_call = update_full_length_cn(raw_cn_call)
    full_length_cn = raw_cn_call.exon78_cn

    if full_length_cn is None:
        # No-call for full-length CN
        tag = "FLCNnoCall"
        full_length_cn = raw_cn_call.exon78_depth
        raw_smn1_cn = get_raw_smn1_cn(full_length_cn, smn1_fraction)
        # In cases where full length copy number is no-call,
        # Test for zero copy of SMN1 at the splice variant site.
        # If true, report range for SMN2 CN
        sma_likelihood_ratio = smn1_cn_zero(
            lsnp1[SPLICE_INDEX], lsnp2[SPLICE_INDEX], mdepth
        )
        if sma_likelihood_ratio > 1 / SMA_CUTOFF:
            cn_smn2 = "%i-%i" % (math.floor(full_length_cn), math.ceil(full_length_cn))
            dout = smn_call(
                0,
                cn_smn2,
                None,
                False,
                True,
                raw_smn1_cn,
                tag,
                [None] * TOTAL_NUM_SITES,
                None,
                None,
            )
        elif sma_likelihood_ratio < SMA_CUTOFF:
            dout = smn_call(
                None,
                None,
                None,
                None,
                False,
                raw_smn1_cn,
                tag,
                [None] * TOTAL_NUM_SITES,
                None,
                None,
            )
        else:
            dout = smn_call(
                None,
                None,
                None,
                None,
                None,
                raw_smn1_cn,
                tag,
                [None] * TOTAL_NUM_SITES,
                None,
                None,
            )

    else:
        full_length_cn = int(full_length_cn)
        raw_smn1_cn = get_raw_smn1_cn(full_length_cn, smn1_fraction)

        # Most likely SMN1 CN (or the best two if posterior probability is low)
        # at each site.
        cn_prob = []
        for i in range(TOTAL_NUM_SITES):
            cn_prob.append(call_reg1_cn(full_length_cn, lsnp1[i], lsnp2[i]))
        # Combine all 6 sites and make a call.
        combined_call = call_reg1_cn(
            full_length_cn,
            sum([lsnp1[a] for a in SELECTED_SITES_INDEX]),
            sum([lsnp2[a] for a in SELECTED_SITES_INDEX]),
        )

        tag, cn_smn1, lsitecall_loose = get_smn1_call_and_tag(cn_prob, combined_call)
        sma_likelihood_ratio = smn1_cn_zero(
            lsnp1[SPLICE_INDEX], lsnp2[SPLICE_INDEX], mdepth
        )
        is_sma = get_sma_status(lsitecall_loose, cn_prob, cn_smn1, sma_likelihood_ratio)
        is_carrier = get_carrier_status(
            lsitecall_loose, cn_prob, cn_smn1, sma_likelihood_ratio
        )

        # targeted variant(s)
        var_cn_confident = None
        raw_var_cn = None
        var_fraction = get_fraction(var_alt, var_ref)
        raw_var_cn = get_raw_smn1_cn(full_length_cn, var_fraction)[0]
        var_cn = [call_reg1_cn(full_length_cn, var_alt[0], var_ref[0])]
        var_cn_filtered = process_raw_call_denovo(
            var_cn, POSTERIOR_CUTOFF_MEDIUM, POSTERIOR_CUTOFF_LOOSE, keep_none=False
        )
        if var_cn_filtered != []:
            var_cn_confident = var_cn_filtered[0]
        if (
            var_cn_confident is not None
            and cn_smn1 is not None
            and cn_smn1 < var_cn_confident
        ):
            var_cn_confident = cn_smn1

        # Call CN for SMN2 and SMN*
        cn_smn2 = None
        cn_smnstar = None
        if raw_cn_call.exon16_cn is not None:
            cn_smnstar = int(raw_cn_call.exon16_cn) - full_length_cn
            if cn_smnstar < 0:
                raise Exception("Total SMN CN is smaller than full-length SMN CN.")
        if cn_smn1 is not None:
            cn_smn2 = full_length_cn - cn_smn1

        dout = smn_call(
            cn_smn1,
            cn_smn2,
            cn_smnstar,
            is_carrier,
            is_sma,
            raw_smn1_cn,
            tag,
            cn_prob,
            raw_var_cn,
            var_cn_confident,
        )

    return dout
