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

from ..utilities import parse_region_file

test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")


class TestUtilities(object):
    def test_parse_reigon_file(self):
        region_file = os.path.join(test_data_dir, "SMN_region_19_short.bed")
        region_dic = parse_region_file(region_file)
        assert len(region_dic["norm"]) == 500
        assert len(region_dic["exon16"]) == 2
        assert len(region_dic["exon78"]) == 2
