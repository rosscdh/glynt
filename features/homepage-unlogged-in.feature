Feature: View the Public Homepage
    In order to get interested in LawPal.com
    An unauthenticated user 
    I need to be able to see the pubic homepage

Scenario: The unauthenticated Homepage
    Given I am on "/"
    Then I should see a "img[src='/static/homepage/assets/img/logo-white.png']" element
    Then I should see "Connecting beautifully" in the "hgroup > h1" element
    Then I should see "Legal services marketplace and relationship management for startups" in the "hgroup > h2" element

    Then I should see "Startups" in the "hgroup > h3" element
    Then I should see "" in the "input[name='EMAIL'][placeholder='Sign up for updates']" element

    Then I should see "Lawyers" in the "div.right hgroup > h3" element
    Then I should see "Sign in with LinkedIn" in the "a.btn.linkedin" element


Scenario: Redirect to LinkedIn
    Given I am on "/"
    Then I should see "Lawyers" in the "div.right hgroup > h3" element
    Then I should see "Sign in with LinkedIn" in the "a.btn.linkedin" element

    Given I follow "Sign in with LinkedIn"

    # Redirect to the linkedin auth page
    Then I should be on "/uas/oauth/authorize"


@mink:zombie
Scenario: Starups signup for updates (Mailchimp)
    Given I am on "/"
    Then I should see "Startups" in the "hgroup > h3" element
    Then I should see "" in the "input[name='EMAIL'][placeholder='Sign up for updates']" element
    Then I should see "Sign Up" in the "button[type=submit]" element
