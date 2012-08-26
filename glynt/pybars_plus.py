from pybars import Compiler

class PybarsPlus(object):
  def __init__(self):
    self.compiler = Compiler()
    self.compiler.register_helper(u'if_eq', self._if_eq)

  def _if_eq(self, this, *args, **kwargs):
    options = args[0]
    if args[1] == kwargs['compare']:
      return options['fn'](this)
    else:
      return options['inverse'](this)

