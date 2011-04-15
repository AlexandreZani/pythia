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

class CustomStartResponse(object):
  def __init__(self, start_response, headers = []):
    self.start_response = start_response
    self.headers = headers

  def add_headers(self, headers):
    self.headers.extend(headers)

  def __call__(self, status, response_headers):
    return self.start_response(status, response_headers + self.headers)
