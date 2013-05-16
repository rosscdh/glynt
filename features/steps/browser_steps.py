# -*- coding: utf-8 -*-
""""""
from behave import given, when, then

from behaving.web.steps import *

# Environment Setup

def before_all(context):
    pass

def after_all(context):
    pass

def before_feature(context, feature):
    pass

# Step Setup
@step(u'I am on "{url}"')
def when_i_visit_url(context, url):
    full_url = context.browser_url(url)
    context.browser.open(full_url)

@step(u'I should see a "{css}" element')
def should_see_element_with_css_within_timeout(context, css, timeout=0):
    assert context.browser.is_element_present_by_css(css, wait_time=timeout), u'Element not present'

@given('/^(?:|I )am logged in as "([^"]*)"$/')
def step(context):
    pass

@given('/^there is no "([^"]*)" user$/')
def step(context):
    pass

@given('/^^(?:|I )click "([^"]*)"$/')
def step(context):
    pass

# @given('/^(?:|I )am on (?:|the )homepage$/')
# def step(context):
#     pass

@when('/^(?:|I )go to (?:|the )homepage$/')
def step(context):
    pass

# @given('/^(?:|I )am on "(?P<page>[^"]+)"$/')
# def step(context):
#     pass

# @when('/^(?:|I )go to "(?P<page>[^"]+)"$/')
# def step(context):
#     pass

# @when('/^(?:|I )reload the page$/')
# def step(context):
#     pass

# @when('/^(?:|I )move backward one page$/')
# def step(context):
#     pass

# @when('/^(?:|I )move forward one page$/')
# def step(context):
#     pass

# @when('/^(?:|I )press "(?P<button>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @when('/^(?:|I )follow "(?P<link>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @when('/^(?:|I )fill in "(?P<field>(?:[^"]|\\")*)" with "(?P<value>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @when('/^(?:|I )fill in "(?P<field>(?:[^"]|\\")*)" with:$/')
# def step(context):
#     pass

# @when('/^(?:|I )fill in "(?P<value>(?:[^"]|\\")*)" for "(?P<field>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @when('/^(?:|I )fill in the following:$/')
# def step(context):
#     pass

# @when('/^(?:|I )select "(?P<option>(?:[^"]|\\")*)" from "(?P<select>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @when('/^(?:|I )additionally select "(?P<option>(?:[^"]|\\")*)" from "(?P<select>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @when('/^(?:|I )check "(?P<option>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @when('/^(?:|I )uncheck "(?P<option>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @when('/^(?:|I )attach the file "(?P[^"]*)" to "(?P<field>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @then('/^(?:|I )should be on "(?P<page>[^"]+)"$/')
# def step(context):
#     pass

# @then('/^(?:|I )should be on (?:|the )homepage$/')
# def step(context):
#     pass

# @then('/^the (?i)url(?-i) should match (?P<pattern>"([^"]|\\")*")$/')
# def step(context):
#     pass

# @then('/^the response status code should be (?P<code>\d+)$/')
# def step(context):
#     pass

# @then('/^the response status code should not be (?P<code>\d+)$/')
# def step(context):
#     pass

# @then('/^(?:|I )should see "(?P<text>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @then('/^(?:|I )should not see "(?P<text>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @then('/^(?:|I )should see text matching (?P<pattern>"(?:[^"]|\\")*")$/')
# def step(context):
#     pass

# @then('/^(?:|I )should not see text matching (?P<pattern>"(?:[^"]|\\")*")$/')
# def step(context):
#     pass

# @then('/^the response should contain "(?P<text>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @then('/^the response should not contain "(?P<text>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @then('/^(?:|I )should see "(?P<text>(?:[^"]|\\")*)" in the "(?P<element>[^"]*)" element$/')
# def step(context):
#     pass

# @then('/^(?:|I )should not see "(?P<text>(?:[^"]|\\")*)" in the "(?P<element>[^"]*)" element$/')
# def step(context):
#     pass

# @then('/^the "(?P<element>[^"]*)" element should contain "(?P<value>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @then('/^the "(?P<element>[^"]*)" element should not contain "(?P<value>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @then('/^(?:|I )should see an? "(?P<element>[^"]*)" element$/')
# def step(context):
#     pass

# @then('/^(?:|I )should not see an? "(?P<element>[^"]*)" element$/')
# def step(context):
#     pass

# @then('/^the "(?P<field>(?:[^"]|\\")*)" field should contain "(?P<value>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @then('/^the "(?P<field>(?:[^"]|\\")*)" field should not contain "(?P<value>(?:[^"]|\\")*)"$/')
# def step(context):
#     pass

# @then('/^the "(?P<checkbox>(?:[^"]|\\")*)" checkbox should be checked$/')
# def step(context):
#     pass

# @then('/^the checkbox "(?P<checkbox>(?:[^"]|\\")*)" (?:is|should be) checked$/')
# def step(context):
#     pass

# @then('/^the "(?P<checkbox>(?:[^"]|\\")*)" checkbox should not be checked$/')
# def step(context):
#     pass

# @then('/^the checkbox "(?P<checkbox>(?:[^"]|\\")*)" should (?:be unchecked|not be checked)$/')
# def step(context):
#     pass

# @then('/^the checkbox "(?P<checkbox>(?:[^"]|\\")*)" is (?:unchecked|not checked)$/')
# def step(context):
#     pass

# @then('/^(?:|I )should see (?P<num>\d+) "(?P<element>[^"]*)" elements?$/')
# def step(context):
#     pass

# @then('/^print current URL$/')
# def step(context):
#     pass

# @then('/^print last response$/')
# def step(context):
#     pass

# @then('/^show last response$/')
# def step(context):
#     pass
