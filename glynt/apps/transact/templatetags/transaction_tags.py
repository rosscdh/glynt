# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import SafeText
from glynt.apps.transact.models import Transaction

register = template.Library()


@register.inclusion_tag('transaction/transactions.html', takes_context=True)
def transactions(context, transactions):
    if type(transactions) == SafeText:
        transactions = Transaction.objects.filter(slug=transactions)
    elif type(transactions) is list:
        # Doesn't work...
        transactions = Transaction.objects.filter(slug__in=transactions)
    else:
        transactions = Transaction.objects.all()

    context.update({
        'transactions': transactions
    })
    return context