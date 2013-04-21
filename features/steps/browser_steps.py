# -*- coding: utf-8 -*-
""""""
from behave import *

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode

import logging
logger = logging.getLogger('django.test.behave')

BEHAVE_DEFAULT_USER_PASSWORD = getattr(settings, 'BEHAVE_DEFAULT_USER_PASSWORD', 'test') # take from settings one day
BEHAVE_DEFAULT_USER_PASSWORD = getattr(settings, 'BEHAVE_DEFAULT_USER_PASSWORD', 'test') # take from settings one day


# Step Setup
@given(u'I am logged in as "{username_pass}"')
def step(context, username_pass):
    context.loaddata('test_users')

    try:
        username, password = username_pass.split(':')
    except:
        username, password = (username_pass, BEHAVE_DEFAULT_USER_PASSWORD)

    user = User(username=username, email='%s+behave@lawpal.com')
    user.set_password(password)
    log_in_as(context, username, password)

    assert user.is_authenticated() is True


def log_in_as(context, username, password):
    context.go_to(reverse('client:login'))
    original_url = context.browser.geturl()
    br = context.browser
    br.select_form(nr=0)
    br.form['username'] = username
    br.form['password'] = password
    br.submit()
    # go pack to that page
    context.go_to(original_url)


@given(u'there is no "([^"]*)" user')
def step(context):
    pass

@given(u'I am on "{url_path}"')
def step(context, url_path):
    context.go_to(url_path)


# @given(u'(?:|I )click "([^"]*)"')
# def step(context):
#     pass

# @given(u'(?:|I )am on ([^"]*)')
# def step(context):
#     pass

# @given(u'(?:|I )am on "(?P<page>[^"]+)"')
# def step(context):
#     pass

# @when(u'(?:|I )go to "(?P<page>[^"]+)"')
# def step(context):
#     pass

# @when(u'(?:|I )reload the page')
# def step(context):
#     pass

# @when(u'(?:|I )move backward one page')
# def step(context):
#     pass

# @when(u'(?:|I )move forward one page')
# def step(context):
#     pass

# @when(u'(?:|I )press "(?P<button>(?:[^"]|\\")*)"')
# def step(context):
#     pass

@when(u'I follow "{link_selector}"')
def step(context, link_selector):
    found = False
    link_selector = link_selector.strip()
    for m in context.csss('a[href]'):
        url = m.get('href')
        for i in [smart_unicode(m.text_content()), m.get('href'), m.get('title'), m.get('name'), m.get('alt')]:
            if type(i) in [str,unicode] and link_selector == i.strip():
                context.go_to(url)
                break


# @when(u'(?:|I )fill in "(?P<field>(?:[^"]|\\")*)" with "(?P<value>(?:[^"]|\\")*)"')
# def step(context):
#     pass

# @when(u'(?:|I )fill in "(?P<field>(?:[^"]|\\")*)" with:')
# def step(context):
#     pass

# @when(u'(?:|I )fill in "(?P<value>(?:[^"]|\\")*)" for "(?P<field>(?:[^"]|\\")*)"')
# def step(context):
#     pass

# @when(u'(?:|I )fill in the following:')
# def step(context):
#     pass

# @when(u'(?:|I )select "(?P<option>(?:[^"]|\\")*)" from "(?P<select>(?:[^"]|\\")*)"')
# def step(context):
#     pass

# @when(u'(?:|I )additionally select "(?P<option>(?:[^"]|\\")*)" from "(?P<select>(?:[^"]|\\")*)"')
# def step(context):
#     pass

# @when(u'(?:|I )check "(?P<option>(?:[^"]|\\")*)"')
# def step(context):
#     pass

# @when(u'(?:|I )uncheck "(?P<option>(?:[^"]|\\")*)"')
# def step(context):
#     pass

# @when(u'(?:|I )attach the file "(?P[^"]*)" to "(?P<field>(?:[^"]|\\")*)"')
# def step(context):
#     pass

@then(u'I should be on "{url}"')
def step(context, url):
    url = url.strip()
    assert smart_unicode(url) in smart_unicode(context.browser.geturl().strip())

# @then(u'(?:|I )should be on (?:|the )homepage')
# def step(context):
#     pass

# @then(u'the (?i)url(?-i) should match (?P<pattern>"([^"]|\\")*")')
# def step(context):
#     pass

# @then(u'the response status code should be (?P<code>\d+)')
# def step(context):
#     pass

# @then(u'the response status code should not be (?P<code>\d+)')
# def step(context):
#     pass

# @then(u'(?:|I )should see "(?P<text>(?:[^"]|\\")*)"')
# def step(context):
#     pass

# @then(u'(?:|I )should not see "(?P<text>(?:[^"]|\\")*)"')
# def step(context):
#     pass

# @then(u'(?:|I )should see text matching (?P<pattern>"(?:[^"]|\\")*")')
# def step(context):
#     pass

# @then(u'(?:|I )should not see text matching (?P<pattern>"(?:[^"]|\\")*")')
# def step(context):
#     pass

# @then(u'the response should contain "(?P<text>(?:[^"]|\\")*)"')
# def step(context):
#     pass

# @then(u'the response should not contain "(?P<text>(?:[^"]|\\")*)"')
# def step(context):
#     pass

@then(u'I should see "{text}"')
def step(context, text):
    assert text == context.pq(text).text()


@then(u'I should see "{text}" in the "{css_selector}" element')
def step(context, text, css_selector):
    found = False
    text = smart_unicode(text.strip())
    print context.csss(css_selector)
    for m in context.csss(css_selector):
        print m.text_content()
        if smart_unicode(m.text_content().strip()) == text:
            found = True
            break
    assert found == True

@then(u'the "{css_selector}" should be empty')
def step(context, css_selector):
    m = context.csss(css_selector)[0]
    assert m.value is None

# @then(u'(?:|I )should not see "(?P<text>(?:[^"]|\\")*)" in the "(?P<element>[^"]*)" element')
# def step(context):
#     pass

# @then(u'the "(?P<element>[^"]*)" element should contain "(?P<value>(?:[^"]|\\")*)"')
# def step(context):
#     pass

# @then(u'the "(?P<element>[^"]*)" element should not contain "(?P<value>(?:[^"]|\\")*)"')
# def step(context):
#     pass

@then(u'I should see a "{css_selector}" element')
def step(context, css_selector):
    pass

# @then(u'(?:|I )should not see an? "(?P<element>[^"]*)" element')
# def step(context):
#     pass

# @then(u'the "(?P<field>(?:[^"]|\\")*)" field should contain "(?P<value>(?:[^"]|\\")*)"')
# def step(context):
#     pass

# @then(u'the "(?P<field>(?:[^"]|\\")*)" field should not contain "(?P<value>(?:[^"]|\\")*)"')
# def step(context):
#     pass

# @then(u'the "(?P<checkbox>(?:[^"]|\\")*)" checkbox should be checked')
# def step(context):
#     pass

# @then(u'the checkbox "(?P<checkbox>(?:[^"]|\\")*)" (?:is|should be) checked')
# def step(context):
#     pass

# @then(u'the "(?P<checkbox>(?:[^"]|\\")*)" checkbox should not be checked')
# def step(context):
#     pass

# @then(u'the checkbox "(?P<checkbox>(?:[^"]|\\")*)" should (?:be unchecked|not be checked)')
# def step(context):
#     pass

# @then(u'the checkbox "(?P<checkbox>(?:[^"]|\\")*)" is (?:unchecked|not checked)')
# def step(context):
#     pass

# @then(u'(?:|I )should see (?P<num>\d+) "(?P<element>[^"]*)" elements?')
# def step(context):
#     pass

@then(u'print current URL')
def step(context):
    print smart_unicode(context.browser.geturl().strip())

@then(u'print html')
def print_html(context):
    print smart_unicode(context.browser.response().read())


# @then(u'show last response')
# def step(context):
#     pass
