Feature: Sign the Lawyer on
    In order to use LawPal I need to complete my signin details and be guided to my profile
    As a linkedin authenticated user
    Once I sign in I should be asked to validate my signin details and be shown the welcome screen.

Scenario: Confirm login details
    Given I have signed in as a new linked in user
    Given I am on "/"
    Then I should see a "form#lawyer-signin-details" element

    When I enter "ross@lawpal.com" into the "#id_email" element
    And I enter "test2007" into the "#id_password" element
    And I enter "test2007" into the "#id_confirm_password" element
    And I click "submit"

    Then I should be on "/welcome"
    And I should see "Claim your profile and join the LawPal community"
    And I should see "Complete your profile"
    And I should see "Preview Profile"

Scenario: Complete your profile
    Given I am on "/lawyers/profile/setup/"
    Then I should see a "ul#profile-tab" element
    And I should see "General"
    And I should see "Transactions & Startups"
    And I should see "Profile"
    And I should see "Connected Accounts"