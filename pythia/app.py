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
from pythia.custom_start_response import CustomStartResponse
from pythia.jinja_wrappers import EnvironmentWrapper
from jinja2 import Environment, PackageLoader, PrefixLoader

class Application(object):
  def __init__(self, settings):
    self.settings = settings
    self.chain = self.settings.pre_views
    self.chain.append(URLDispatcher(self.settings.view_paths))
    loaders = { 
        "pythia" : PackageLoader('pythia', 'views/templates'),
        settings.app_pkg : PackageLoader(settings.app_pkg, settings.templates),
        }
    self.jinja_env = Environment(loader=PrefixLoader(loaders))
    self.jinja_env.globals['app_name'] = settings.app_name

  def __call__(self, environ, start_response):
    environ['pythia'] = {
        'chain' : FunctionChain(self.chain),
        'jinja_env' : EnvironmentWrapper(self.jinja_env),
        'app_settings' : self.settings,
        }

    return environ['pythia']['chain'](environ, CustomStartResponse(start_response))
