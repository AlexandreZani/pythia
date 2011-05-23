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

from pythia.errors import *
from pythia.pipeline import Pipeline

def raise_404(pipe, environ, start_response):
  raise Http404

class StartResponse(object):
  def __init__(self, expected_status=None, expected_headers=None):
    self.status = expected_status
    self.headers = expected_headers

  def __call__(self, status, headers):
    if self.status:
      assert self.status == status

    if self.headers:
      assert self.headers == headers

class TestExceptionHandler(object):
  def test_default404(self):
    pipe = Pipeline([ExceptionHandler(), raise_404])

    expected = "<html><title>404 Not Found</title><body>404 Not Found</body></html>"

    start_response = StartResponse(expected_status="404 Not Found")

    assert expected == pipe(None, start_response).next()

  def test_override404(self):
    def overriding404(environ, start_response):
      return "overriding404"

    pipe = Pipeline([ExceptionHandler({Http404 : overriding404}), raise_404])

    assert "overriding404" == pipe(None, None)

  def test_overrideCustom(self):
    class CustomException(Exception): pass

    def throw_custom(pipe, environ, start_response):
      raise CustomException

    def custom_handler(environ, start_response):
      return "custom_handler"

    pipe = Pipeline([ExceptionHandler({CustomException : custom_handler}),
      throw_custom])

    assert "custom_handler" == pipe(None, None)

