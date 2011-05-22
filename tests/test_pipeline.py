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
from pythia.pipeline import Pipeline

def add(pipeline, x, y):
  return x + y

def mul(pipeline, x, y):
  return x * y

def inc(pipeline, x):
  return pipeline(x+1)

def identity(pipeline, x):
  return x

class Adder(object):
  def __init__(self, y):
    self.y = y

  def add(self, pipeline, x):
    return pipeline(x + self.y)

class TestPipeline(object):
  def test_simple(self):
    pipeline = Pipeline([add, add, mul])

    assert 10 == pipeline(4, 6)
    assert 20 == pipeline(15, 5)
    assert 30 == pipeline(6, 5)

  def test_last_func(self):
    pipeline = Pipeline([add])

    assert 10 == pipeline(4, 6)
    with pytest.raises(StopIteration):
      pipeline()

  def test_push(self):
    pipeline = Pipeline([add, add])

    assert 10 == pipeline(4, 6)
    pipeline.push(mul)
    assert 30 == pipeline(6, 5)
    assert 20 == pipeline(15, 5)

  def test_add(self):
    pipeline_1 = Pipeline([add, add])
    pipeline_2 = Pipeline([mul, mul])

    pipeline_a = Pipeline([add, add, mul, mul])

    assert pipeline_1 + pipeline_2 == pipeline_a

  def test_inequal(self):
    pipeline_1 = Pipeline([add, add])
    pipeline_2 = Pipeline([mul, mul])

    assert pipeline_1 != pipeline_2

  def test_non_function(self):
    pipeline = Pipeline([add, 32, 12, add, mul])

    assert 10 == pipeline(4, 6)
    assert 20 == pipeline(15, 5)
    assert 30 == pipeline(6, 5)

  def test_last_non_func(self):
    pipeline = Pipeline([add, 4])

    assert 10 == pipeline(4, 6)
    with pytest.raises(StopIteration):
      pipeline()

  def test_arg_insert(self):
    pipeline = Pipeline([inc, inc, inc, identity])

    assert 3 == pipeline(0)

  def test_methods(self):
    a = Adder(5)

    pipeline = Pipeline([a.add, a.add, a.add, identity])

    assert 15 == pipeline(0)
