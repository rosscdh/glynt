Feature: View a Lawyer Profile
    In order to be accessable on LawPal.com
    As an authenticated lawyer user 
    I need to be able to get to and edit my profile settings

Scenario: Get to the Preview Profile Page
    Given I am logged in as "userA:test"
    Given I am on "/"
    When I follow "Preview"
    Then I should be on "/lawyers/userA/"