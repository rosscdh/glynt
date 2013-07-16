# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import SafeText
from glynt.apps.transact.models import Transaction

register = template.Library()


@register.inclusion_tag('transact/partials/transaction_choice.html', takes_context=True)
def transactions(context, transaction):
    if type(transaction) in [SafeText, str, unicode]:
        transaction = Transaction.objects.filter(slug=unicode(transaction))
    elif type(transaction) in [list, tuple]:
        transaction = Transaction.objects.filter(slug__in=transaction)
    else:
        transaction = Transaction.objects.all()

    context.update({
        'transactions': transaction
    })
    return context


@register.simple_tag(takes_context=True)
def transpose_company_data(context, value):
    user = context.get('user')
    if user:
        try:
            company = user.companies.all()[0]
        except IndexError:
            company = None
    t = template.Template(value)
    c = template.Context(company.__dict__)
    return t.render(c)
