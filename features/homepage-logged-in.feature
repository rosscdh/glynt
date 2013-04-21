Feature: View the Authenticated Welcome Page
    In order to get use LawPal.com
    As an authenticated user 
    I need to have a launchpad dashboard

Scenario: The authenticated Homepage
    Given I am logged in as "userA:test"
    Given I am on "/"
    Then I should see "Claim your profile and join the LawPal community"
    And I should see "Complete your profile"
    And I should see "Complete your profile" in the "a.btn-large" element
    And I should see "Preview"
    And I should see "Preview" in the "a.btn-large" element

Scenario: Get to the Setup Profile Page
    Given I am logged in as "userA:test"
    Given I am on "/"
    When I follow "Complete your profile"
    Then I should be on "/lawyers/profile/setup/"

Scenario: Get to the Preview Profile Page
    Given I am logged in as "userA:test"
    Given I am on "/"
    When I follow "Preview"
    Then I should be on "/lawyers/userA/"