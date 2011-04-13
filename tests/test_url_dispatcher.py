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

from pythia.url_dispatcher import URLDispatcher
from pythia.chain import FunctionChain

class TestURLDispatcher(object):
  def test_simple_parse(self):
    view_paths = [
        (r"^/hello/$", "bad", ()),
        (r"^/winner/$", "good", ()),
        ]

    dispatcher = URLDispatcher(view_paths)

    assert ("good", {}) == dispatcher._parse_url("/winner/")

  def test_add_slash(self):
    view_paths = [
        (r"^/hello/$", "bad", ()),
        (r"^/winner/$", "good", ()),
        ]

    dispatcher = URLDispatcher(view_paths)

    assert ("good", {}) == dispatcher._parse_url("/winner")

  def test_parse_number(self):
    view_paths = [
        (r"^/hello/$", "bad", ()),
        (r"^/winner/$", "bad", ()),
        (r"^/user/(\d+)/$", "good", ("user_id",)),
        ]

    dispatcher = URLDispatcher(view_paths)

    assert ("good", {"user_id" : '1234'}) == dispatcher._parse_url("/user/1234/")

  def test_call(self):
    def func(environ, start_response):
      assert environ['pythia']['url_params']['user_id'] == '1234'
      return "func"

    view_paths = [ (r"^/user/(\d+)/$", func, ("user_id",)), ]

    dispatcher = URLDispatcher(view_paths)

    environ = { "PATH_INFO" : "/user/1234" }

    assert "func" == dispatcher(environ, None)
