#   Copyright 2011 Alexandre Zani (alexandre.zani@gmail.com) 
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import pytest
from pythia.custom_start_response import CustomStartResponse

def base(status, response_headers):
  assert "200 OK" == status
  assert [1, 2, 3, 4] == response_headers

  return 1

class TestCustomStartResponse(object):
  def test_simple(self):
    custom = CustomStartResponse(base)

    assert 1 == custom("200 OK", [1, 2, 3, 4])

  def test_extend(self):
    custom = CustomStartResponse(base)

    custom.add_headers([3, 4])
    
    assert 1 == custom("200 OK", [1, 2])

  def test_init(self):
    custom = CustomStartResponse(base, [3, 4])

    assert 1 == custom("200 OK", [1, 2])
