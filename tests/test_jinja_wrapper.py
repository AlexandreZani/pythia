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

from pythia.jinja_wrappers import TemplateWrapper, EnvironmentWrapper

class MockTemplate(object):
  def render(self, *args, **kwargs):
    a = dict(*args, **kwargs)
    print a
    assert 0 == a['a']
    assert 1 == a['b']
    assert 2 == a['c']
    return "render"

class TestTemplateWrapper(object):
  def test_simple(self):
    t = TemplateWrapper(MockTemplate())

    assert "render" == t.render(a=0, b=1, c=2)

  def test_add_context(self):
    t = TemplateWrapper(MockTemplate(), {'b' : 1, 'c' : 2})

    assert "render" == t.render(a=0)

  def test_add_context_overwrite(self):
    t = TemplateWrapper(MockTemplate(),{'b' : 5, 'c' : 2})

    assert "render" == t.render(a=0, b=1)

class MockEnvironment(object):
  def get_template(self, name, parent, globals):
    assert "hsr/login.html" == name 
    assert "parent" == parent
    assert "globals" == globals
    return MockTemplate()

class TestEnvironmentWrapper(object):
  def test_simple(self):
    e = EnvironmentWrapper(MockEnvironment())

    t = e.get_template("hsr/login.html", "parent", "globals")

    assert "render" == t.render(a=0, b=1, c=2)

  def test_add_context_kw(self):
    e = EnvironmentWrapper(MockEnvironment())

    t = e.get_template("hsr/login.html", "parent", "globals")

    e.add_context_variables(b=1, c=2)

    assert "render" == t.render(a=0)

  def test_add_context_dict(self):
    e = EnvironmentWrapper(MockEnvironment())

    t = e.get_template("hsr/login.html", "parent", "globals")

    e.add_context_variables({'b' : 1, 'c' : 2})

    assert "render" == t.render(a=0)

  def test_add_context_overwrite(self):
    e = EnvironmentWrapper(MockEnvironment())

    t = e.get_template("hsr/login.html", "parent", "globals")

    e.add_context_variables({'b' : 5, 'c' : 2})

    assert "render" == t.render(a=0, b=1)
