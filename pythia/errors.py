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

from pythia.pipeline import Pipeline

class HttpError(Exception): pass

class Http400(HttpError): 
  num = 400
  name = "Bad Request"

class Http401(HttpError):
  num = 401
  name = "Unauthorized"

class Http402(HttpError):
  num = 402
  name = "Payment Required"

class Http403(HttpError):
  num = 403
  name = "Forbidden"

class Http404(HttpError):
  num = 404
  name = "Not Found"

class Http500(HttpError):
  num = 500
  name = "Internal Error"

class Http501(HttpError):
  num = 501
  name = "Not Implemented"

class Http503(HttpError):
  num = 503
  name = "Gateway Timeout"

class ErrorView(object):
  def __init__(self, err):
    self.num = err.num
    self.name = err.name

  def __call__(self, environ, start_response):
    status = str(self.num) + " " + self.name
    data = "<html><title>%s</title><body>%s</body></html>" % (status, status)

    response_headers = [
        ('Content-type', 'text/html'),
        ('Content-Lenght', str(len(data))),
        ]

    start_response(status, response_headers)

    return iter([data])

_default_exception_handlers = {
    Http400 : ErrorView(Http400),
    Http401 : ErrorView(Http401),
    Http402 : ErrorView(Http402),
    Http403 : ErrorView(Http403),
    Http404 : ErrorView(Http404),
    Http500 : ErrorView(Http500),
    Http501 : ErrorView(Http501),
    Http503 : ErrorView(Http503),
    }

class ExceptionHandler(object):
  def __init__(self, override_handlers = None):
    self.handlers = dict(_default_exception_handlers)

    if override_handlers:
      self.handlers.update(override_handlers)

    self.exceptions = tuple(self.handlers)

  def __call__(self, pipe, environ, start_response):
    try:
      return pipe(environ, start_response)
    except self.exceptions, e:
      return self.handlers[type(e)](environ, start_response)
