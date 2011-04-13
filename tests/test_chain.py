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
from pythia.chain import FunctionChain

def add(x, y):
  return x + y

def mul(x, y):
  return x * y

class TestFunctionChain(object):
  def test_simple(self):
    chain = FunctionChain([add, add, mul])

    assert 10 == chain(4, 6)
    assert 20 == chain(15, 5)
    assert 30 == chain(6, 5)

  def test_last_func(self):
    chain = FunctionChain([add])

    assert 10 == chain(4, 6)
    with pytest.raises(StopIteration):
      chain()

  def test_push(self):
    chain = FunctionChain([add, add])

    assert 10 == chain(4, 6)
    chain.push(mul)
    assert 30 == chain(6, 5)
    assert 20 == chain(15, 5)

  def test_add(self):
    chain_1 = FunctionChain([add, add])
    chain_2 = FunctionChain([mul, mul])

    chain_a = FunctionChain([add, add, mul, mul])

    assert chain_1 + chain_2 == chain_a

  def test_non_function(self):
    chain = FunctionChain([add, 32, 12, add, mul])

    assert 10 == chain(4, 6)
    assert 20 == chain(15, 5)
    assert 30 == chain(6, 5)

  def test_last_non_func(self):
    chain = FunctionChain([add, 4])

    assert 10 == chain(4, 6)
    with pytest.raises(StopIteration):
      chain()
