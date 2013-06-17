# -*- coding: utf-8 -*-
from django import template

from glynt.apps.transaction.models import Transaction

register = template.Library()


@register.inclusion_tag('transaction/transactions.html', takes_context=True)
def transactions(context, transactions=[]):
    if transactions:
        transactions = Transaction.objects.filter(slug__in=transactions)
    else:
        transactions = Transaction.objects.all()

    context.update({
        'transactions': transactions
    })
    return context