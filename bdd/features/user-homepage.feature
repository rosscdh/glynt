# features/user-hompeage.feature
Feature: Logged in User Homepage
  In order to select a document
  As a user
  I need to be able to select an avaliable document to workon, from the homepage

  Scenario: The user should be able to see a list of available documents on the homepage
    Given I am on "/"
    And I am logged in as "userA"
    And I should see a "ul#available-document-list" element
    And I should see 3 "ul#available-document-list li" elements
