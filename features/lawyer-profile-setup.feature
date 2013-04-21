Feature: Setup a Lawyer Profile
    In order to have a profile on LawPal.com
    As an authenticated lawyer user 
    I need to be able to get to and edit my profile settings

Scenario: Get to the Setup Profile Page
    Given I am logged in as "userA:test"
    Given I am on "/"
    When I follow "Complete your profile"
    Then I should be on "/lawyers/profile/setup/"

