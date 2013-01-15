# features/user-login.feature
Feature: Allow user to login to the system, using a username password
  In order to use the system
  As an anonymous user
  I need to be able to complete a login process and be logged in to the site

  Scenario: The user should see the login link
    Given I am on "/"
    Then I should see a "a#user-login-link" element

  Scenario: The user should be able to click the login button and be taken to a login form
    Given I am on "/"
    When I follow "user-login-link"
    Then the response status code should be 200
    And the url should match "/client/login/"
    And I should see a "form#user-login" element
    And I should see a "form#user-login input[name=username]" element
    And I should see a "form#user-login input[name=password]" element
    And I should see a "form#user-login button#user-login-submit" element

    Scenario: The user should be able to complete and then submit the login form using an email address
      Given I am on "/client/login/"
      Then I should see a "form#user-login" element
      And I should see a "form#user-login input[name=username]" element
        When I fill in "id_username" with "userA@weareml.com"
      And I should see a "form#user-login input[name=password]" element
        When I fill in "id_password" with "test"
      And I should see a "form#user-login button#user-login-submit" element

      When I press "user-login-submit"
        Then the response status code should be 200
        And the url should match "/"
        And I should see a "ul#messages li.success" element
        And I should see "Welcome, you have successfully logged in."

    Scenario: The user should be able to complete and then submit the login form using a username
      Given I am on "/client/login/"
      Then I should see a "form#user-login" element
      And I should see a "form#user-login input[name=username]" element
        When I fill in "id_username" with "userA"
      And I should see a "form#user-login input[name=password]" element
        When I fill in "id_password" with "test"
      And I should see a "form#user-login button#user-login-submit" element

      When I press "user-login-submit"
        Then the response status code should be 200
        And the url should match "/"
        And I should see a "ul#messages li.success" element
        And I should see "Welcome, you have successfully logged in."

    Scenario: Once logged in the user should not be able to see the login form again and should be redirected to /
      Given I am logged in as "userA"
      And I am on "/client/login/"
      Then the url should match "/"