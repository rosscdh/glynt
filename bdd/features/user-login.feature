# features/user-login.feature
Feature: Allow user to login to the system, using a username password
  In order to use the system
  As an anonymous user
  I need to be able to complete a login process and be logged in to the site

  Scenario: The user should see the login link
    Given I am on "/"
    Then I should see a "a#user-login" element

  Scenario: The user should be able to click the login button and be taken to a login form
    Given I am on "/"
    When I follow "a#user-login"
    Then the response status code should be 200
    And the url should match "/client/login/"
    And I should see a "form#user-login" element
    And I should see a "form#user-login input[name=username]" element
#    And I should see a "form#user-login input[name=email]" element
    And I should see a "form#user-login input[name=password]" element
    And I should see a "form#user-login input[type=button].submit" element

    Scenario: The user should be able to complete and then submit the login form
      Given I am on "/client/signup/"
      Then I should see a "form#user-login" element
      And I should see a "form#user-login input[name=username]" element
        When I fill in "form#user-login input[name=username]" with "userA"
#      And I should see a "form#user-login input[name=email]" element
#      When I fill in "form#user-login input[name=email]" with "userA@weareml.com"
      And I should see a "form#user-login input[name=password]" element
        When I fill in "form#user-login input[name=password]" with "test"
      And I should see a "form#user-login input[type=button].submit" element

      When I press "form#user-login input[type=button].submit"
        Then the response status code should be 200
        And the url should match "/"
        And I should see "Congratulations, you have logged in successfully"