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
import math
import numpy as np
from scipy.stats import norm

# sd for CN=0 is arbitrarily set at 0.032
SIGMA_CN0 = 0.032
PV_CUTOFF = 1e-3
POSTERIOR_CUTOFF = 0.95
# CN = 0 - 10
DEFAULT_GMM_NSTATE = 11


class Gmm:
    def __init__(self, num_state=DEFAULT_GMM_NSTATE):
        self.mu_state = []
        self.sigma_state = []
        self.prior_state = []
        self.value_shift = None
        self.nstate = num_state

    def set_gmm_par(self, dpar_tmp, svid):
        """Return the complete set of gmm parameters based on depth value."""
        if svid not in dpar_tmp:
            raise Exception("Variant id %s is not recognized." % svid)
        gmm_parameter = dpar_tmp[svid]
        # The gmm parameter file stores the adjustment factor (value_shift) for
        # all depth values. This value should be one if there is no bias
        # between target regions and the normalization regions.
        # But this value may vary slightly depending on the aligner
        # choice and aligner setting. If running the caller on a population,
        # it may be desirable to run GMM modeling for the population and make
        # this value more accurate.
        self.value_shift = float(gmm_parameter["shift"][0])

        # The means are modeled as 0, 0.5, 1, 1.5, 2, 2.5, etc.
        # (We could also do 0, 1, 2, 3, 4, 5, etc.)
        # The gmm parameter file stores the mean depth values for CN=2 and CN=3
        self.mu_state = [
            0,
            0.5,
            float(gmm_parameter["mean"][0]),
            float(gmm_parameter["mean"][1]),
        ]
        mu_width = float(gmm_parameter["mean"][1]) - float(gmm_parameter["mean"][0])
        for i in range(self.nstate):
            if i > 3:
                self.mu_state.append(1 + mu_width * (i - 2))

        sum_prior = sum([float(a) for a in gmm_parameter["prior"]])
        if sum_prior >= 1:
            raise Exception("Sum of priors is larger than 1.")
        for i in range(self.nstate):
            # The gmm parameter file stores the prior frequencies for CN=0-6
            if i < len(gmm_parameter["prior"]):
                self.prior_state.append(float(gmm_parameter["prior"][i]))
            else:
                prior_value = (1 - sum_prior) / (
                    self.nstate - len(gmm_parameter["prior"])
                )
                self.prior_state.append(prior_value)

        self.sigma_state = [SIGMA_CN0]
        # The gmm parameter file stores the standard deviation for CN=2.
        # The other sd values are derived from it.
        for i in range(self.nstate):
            if i > 0:
                sigma_value = float(gmm_parameter["sd"][0]) * np.sqrt(float(i) / 2)
                self.sigma_state.append(sigma_value)

    def gmm_call(self, val):
        """Return the final copy number call."""
        val_new = (val / 2) / self.value_shift
        fcall = self.call_post_prob(val_new, POSTERIOR_CUTOFF)
        if fcall is not None:
            gauss_p_value = self.get_gauss_pmf_cdf(
                val_new, self.mu_state[fcall], self.sigma_state[fcall]
            )[1]
            # apply another p-value cutoff
            # just comparing the depth value and the called CN
            if gauss_p_value < PV_CUTOFF:
                fcall = None
        cn_call = namedtuple("cn_call", "cn depth_value")
        return cn_call(fcall, round(val / self.value_shift, 3))

    def get_gauss_pmf_cdf(self, test_value, gauss_mean, gauss_sd):
        """Return the pmf and cdf of a gaussian distribution."""
        test_stats = (test_value - gauss_mean) / gauss_sd
        pdf = norm.pdf(test_stats) / gauss_sd
        p_value = min(norm.cdf(test_stats), 1 - norm.cdf(test_stats))
        return (pdf, p_value)

    def call_post_prob(self, val, post_cutoff):
        """Return the copy number call based on gaussian mixture model."""
        number_state = len(self.prior_state)
        prob = []
        for i in range(0, number_state):
            gauss_pmf = self.get_gauss_pmf_cdf(
                val, self.mu_state[i], self.sigma_state[i]
            )[0]
            prob.append(gauss_pmf * self.prior_state[i])
        sum_prob = float(sum(prob))
        post_prob = [float(a) / sum_prob for a in prob]
        max_prob = max(post_prob)
        if max_prob >= post_cutoff:
            return post_prob.index(max_prob)
        else:
            return None
