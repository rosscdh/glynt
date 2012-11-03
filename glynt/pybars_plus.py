# -*- coding: utf-8 -*-
from pybars import Compiler


class PybarsPlus(object):
  source = None
  compiler = None
  template = None

  def __init__(self, source):
    self.compiler = Compiler()
    self.source = unicode(source)
    self.compiler.register_helper(u'if_eq', self.helper_if_eq)
    self.compiler.register_helper(u'unless_eq', self.helper_unless_eq)
    self.compiler.register_helper(u'if_gt', self.helper_if_gt)
    self.compiler.register_helper(u'if_lt', self.helper_if_lt)
    self.compiler.register_helper(u'if_gteq', self.helper_if_gteq)
    self.compiler.register_helper(u'if_lteq', self.helper_if_lteq)

  def render(self, context):
    template = self.compiler.compile(self.source)
    if template:
      html = template(context)
      return unicode(''.join(html))
    return None

  def helper_if_eq(self, this, *args, **kwargs):
    options = args[0]
    if args[1] == kwargs['compare']:
      return options['fn'](this)
    else:
      return options['inverse'](this)

  def helper_unless_eq(self, this, *args, **kwargs):
    options = args[0]
    if args[1] != kwargs['compare']:
      return options['fn'](this)
    else:
      return options['inverse'](this)

  def helper_if_gt(self, this, *args, **kwargs):
    options = args[0]
    if args[1] > kwargs['compare']:
      return options['fn'](this)
    else:
      return options['inverse'](this)

  def helper_unless_gt(self, this, *args, **kwargs):
    pass

  def helper_if_lt(self, this, *args, **kwargs):
    options = args[0]
    if args[1] < kwargs['compare']:
      return options['fn'](this)
    else:
      return options['inverse'](this)

  def helper_unless_lt(self, this, *args, **kwargs):
    pass

  def helper_if_gteq(self, this, *args, **kwargs):
    options = args[0]
    if args[1] >= kwargs['compare']:
      return options['fn'](this)
    else:
      return options['inverse'](this)

  def helper_unless_gteq(self, this, *args, **kwargs):
    pass

  def helper_if_lteq(self, this, *args, **kwargs):
    options = args[0]
    if args[1] <= kwargs['compare']:
      return options['fn'](this)
    else:
      return options['inverse'](this)

  def helper_unless_lteq(self, this, *args, **kwargs):
    pass