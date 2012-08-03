# features/user-signup.feature
Feature: Allow user to sign up manually
  In order to use the system
  As an anonymous user
  I need to be able to complete a signup process and be registered

  Scenario: The user should see the signup link
    Given I am on "/"
    Then I should see a "a#user-signup" element

  Scenario: The user should be able to click the signup button and be taken to a signup form
    Given I am on "/"
    When I follow "a#user-signup"
    Then the response status code should be 200
    And the url should match "/accounts/signup/"
    And I should see a "form#user-signup" element
    And I should see a "form#user-signup input[name=firstname]" element
    And I should see a "form#user-signup input[name=lastname]" element
    And I should see a "form#user-signup input[name=email]" element
    And I should see a "form#user-signup input[name=password]" element
    And I should see a "form#user-signup input[name=confirmpassword]" element
    And I should see a "form#user-signup select[name=country]" element
    And I should see a "form#user-signup input[name=state]" element
    And I should see a "form#user-signup input[type=button].submit" element

    Scenario: The user should be able to submit the signup form
      Given I am on "/accounts/signup/"
      Then I should see a "form#user-signup" element
      And I should see a "form#user-signup input[name=firstname]" element
        When I fill in "form#user-login input[name=firstname]" with "Test"
      And I should see a "form#user-signup input[name=lastname]" element
        When I fill in "form#user-login input[name=lastname]" with "User"
      And I should see a "form#user-signup input[name=email]" element
        When I fill in "form#user-login input[name=email]" with "userC@weareml.com"
      And I should see a "form#user-signup input[name=password]" element
        When I fill in "form#user-login input[name=password]" with "test"
      And I should see a "form#user-signup input[name=confirmpassword]" element
        When I fill in "form#user-login input[name=confirmpassword]" with "test"
      And I should see a "form#user-signup select[name=country]" element
        When I select "US" from "form#user-signup select[name=country]"
      And I should see a "form#user-signup input[name=state]" element
        When I fill in "form#user-login input[name=state]" with "AL"
      And I should see a "form#user-signup input[type=button].submit" element

      When I press "form#user-login input[type=button].submit"
        Then the response status code should be 200
        And the url should match "/"
        And I should see "Congratulations, you have signed up successfully"