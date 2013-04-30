Feature: View the Private Homepage
    In order to get use LawPal.com
    As an authenticated user 
    I need to have a launchpad dashboard

Scenario: The authenticated Homepage
    Given I am logged in as "userA:test"
    And I am on "/"
    Then print last response
    Then I should see "Complete your profile"
    And I should see "Preview"
