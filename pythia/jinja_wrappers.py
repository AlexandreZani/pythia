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

class TemplateWrapper(object):
  """This is a wrapper class for jinja.environment.Template
  This object contains extra context variables which are passed
  to the rendering engine. Very useful to not clobber the
  global context
  Most of its methods are nothing more than wrappers for the
  Template methos of the same name
  """
  def __init__(self, template, context = {}):
    self.template = template
    self.context = context

  def render(self, *args, **kwargs):
    vars = dict(self.context)
    vars.update(dict(*args, **kwargs))
    return self.template.render(vars)

  def stream(self, *args, **kwargs):
    vars = dict(self.context)
    vars.update(dict(*args, **kwargs))
    return self.template.stream(vars)

  def generate(self, *args, **kwargs):
    vars = dict(self.context)
    vars.update(dict(*args, **kwargs))
    return self.template.generate(vars)

class EnvironmentWrapper(object):
  """This is a wrapper class for jinja.environment.Environment
  When a new request comes in, instantiate this class with the
  global environment. Then, use add_context_variable to add
  some request-specific context without clobbering the global
  environment with all the race-conditions that would introduce
  """
  def __init__(self, environment):
    self.environment = environment
    self.context = {}

  def add_context_variables(self, *args, **kwargs):
    """Adds the passed variables to the context of this wrapper.
    This takes the same arguments as dict
    """
    vars = dict(*args, **kwargs)
    self.context.update(vars)

  def get_template(self, name, parent=None, globals=None):
    """Returns a TemplateWrapper that contains the requested template
    """
    return TemplateWrapper(self.environment.get_template(name, parent, globals),
        self.context)
