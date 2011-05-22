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

import re
from pythia.pipeline import Pipeline
from pythia.views import errors

class URLDispatcher(object):
  def __init__(self, view_paths):
    self._view_paths = view_paths

  def _parse_url(self, url):
    if url[-1] != '/':
      url += '/'

    for path in self._view_paths:
      result = re.search(path[0], url)
      if result:
        return (path[1], dict(zip(path[2], result.groups())))

    return (None, None)

  def __call__(self, pipeline, environ, start_response):
    url = environ['PATH_INFO']

    (view, parameters) = self._parse_url(url)

    if view == None:
      pipeline.append(errors.http404)
    else:
      pipeline.append(view)

    try:
      environ['pythia']['url_params'] = parameters
    except KeyError:
      environ['pythia'] = {'url_params' : parameters}

    return pipeline(environ, start_response)
