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

def http404(environ, start_response):
  settings = environ['pythia']['app_settings']
  status = "404 Not Found"
  template = environ['pythia']['jinja_env'].get_template("pythia/404.html")
  data = template.render(url=environ['PATH_INFO'])
  response_headers = [
      ('Content-type','text/html'),
      ('Content-Length', str(len(data))),
      ]
  start_response(status, response_headers)
  return iter([data])
