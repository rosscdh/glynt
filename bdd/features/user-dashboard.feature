# features/user-hompeage.feature
Feature: Logged in User Dashboard
  In order to manage my documents
  As a user
  I need to be able to beable to view documentsI have created and their status'

  Scenario: The user should be able to see a list of their created documents
    Given I am on "/client"
    And I am logged in as "userA"
    And I should see a "dl#available-document-list" element
    And I should see 4 "dl#available-document-list dt" elements

  Scenario: The user should be able to create a new document
    Given I am on "/client"
    And I am logged in as "userA"
    Then I should see a "a#create-document" element

    When I follow "a#create-document"
    Then the response status code should be 200
    And I should see "Create a document"
    And I should see a "div#md-document" element
