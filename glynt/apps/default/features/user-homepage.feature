# features/user-hompeage.feature
Feature: Logged in User Homepage
  In order to select a document
  As a user
  I need to be able to select an avaliable document to workon, from the homepage

  Scenario: The user should be able to see a list of  documents on the homepage
    Given I am on "/"
    And I am logged in as "userA"
    