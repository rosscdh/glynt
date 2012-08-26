from pybars import Compiler


class PybarsPlus(object):
  source = None
  compiler = None
  template = None

  def __init__(self, source):
    self.compiler = Compiler()
    self.source = unicode(source)
    self.compiler.register_helper(u'if_eq', self.helper_if_eq)

  def render(self, context):
    template = self.compiler.compile(self.source)
    if template:
      html = template(context)
      return ''.join(html)
    return ''

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