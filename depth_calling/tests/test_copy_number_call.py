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

from ..copy_number_call import (
    call_reg1_cn,
    process_raw_call_gc,
    process_raw_call_denovo,
)


class TestCallCN(object):
    def test_call_reg1_cn(self):
        call = call_reg1_cn(4, 30, 30)
        assert call == [2]
        call = call_reg1_cn(4, 10, 30)
        assert call == [1]
        call = call_reg1_cn(4, 30, 10)
        assert call == [3]
        call = call_reg1_cn(3, 30, 30)
        assert call == [2, 0.689, 1, 0.311]

    def test_process_raw_call_gc(self):
        lcn = [[1], [1, 0.8, 2, 0.2]]
        filtered_call = process_raw_call_gc(lcn, 0.7)
        assert filtered_call == [1, 1]
        filtered_call = process_raw_call_gc(lcn, 0.9)
        assert filtered_call == [1, None]
        filtered_call = process_raw_call_gc(lcn, 0.9, keep_none=False)
        assert filtered_call == [1]

    def test_process_raw_call_denovo(self):
        lcn = [[1], [0, 0.8, 1, 0.2], [2, 0.6, 1, 0.4]]
        filtered_call = process_raw_call_denovo(lcn, 0.9, 0.7)
        assert filtered_call == [1, None, 1]
        filtered_call = process_raw_call_denovo(lcn, 0.9, 0.55)
        assert filtered_call == [1, None, 2]

        lcn = [[1], [1, 0.65, 0, 0.35], [2, 0.6, 1, 0.4]]
        filtered_call = process_raw_call_denovo(lcn, 0.9, 0.62, [1, 1, 1])
        assert filtered_call == [1, 1, 1]
        filtered_call = process_raw_call_denovo(lcn, 0.9, 0.7, [1, 1, 1])
        assert filtered_call == [1, 0, 1]
