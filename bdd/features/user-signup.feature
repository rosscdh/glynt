# features/user-signup.feature
Feature: Allow user to sign up manually
  In order to use the system
  As an anonymous user
  I need to be able to complete a signup process and be registered

  Scenario: The user should see the signup link
    Given there is no "userD@weareml.com" user

  Scenario: The user should see the signup link
    Given I am on "/"
    Then I should see a "a#user-signup" element

  Scenario: The user should be able to click the signup button and be taken to a signup form
    Given I am on "/"
    When I follow "user-signup"
    Then the response status code should be 200
    And the url should match "/client/signup/"
    And I should see a "form#user-signup" element
    And I should see a "form#user-signup input[name=first_name]" element
    And I should see a "form#user-signup input[name=last_name]" element
    And I should see a "form#user-signup input[name=email]" element
    And I should see a "form#user-signup input[name=password2]" element
    And I should see a "form#user-signup input[name=password2]" element
    And I should see a "form#user-signup select[name=country]" element
    And I should see a "form#user-signup input[name=state]" element
    And I should see a "form#user-signup button#user-signup-submit" element

    Scenario: The user should be able to submit the signup form
      Given I am on "/client/signup/"
      Then I should see a "form#user-signup" element
      And I should see a "form#user-signup input[name=first_name]" element
        When I fill in "id_first_name" with "Test"
      And I should see a "form#user-signup input[name=last_name]" element
        When I fill in "id_last_name" with "User"
      And I should see a "form#user-signup input[name=email]" element
        When I fill in "id_email" with "userD@weareml.com"
      And I should see a "form#user-signup input[name=password1]" element
        When I fill in "id_password1" with "test"
      And I should see a "form#user-signup input[name=password2]" element
        When I fill in "id_password2" with "test"
      And I should see a "form#user-signup select[name=country]" element
        When I select "US" from "country"
      And I should see a "form#user-signup input[name=state]" element
        When I fill in "state" with "AL"
      And I should see a "form#user-signup button#user-signup-submit" element

      When I press "user-signup-submit"
        And the url should match "/"
        And I should see "Welcome, you have successfully signed up. Please remember to check your email and activate your account once you recieve our welcome email."

    Scenario: Once logged in the user should not be able to see the login form again and should be redirected to /
      Given I am logged in as "userD"
      And I am on "/client/signup/"
      Then the url should match "/"