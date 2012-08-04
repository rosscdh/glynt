# features/user-hompeage.feature
Feature: Logged in User Dashboard
  In order to manage my documents
  As a user
  I need to be able to beable to view documentsI have created and their status'

  Scenario: The user should be able to see a list of their created documents
    When I am logged in as "userA"
    Then I am on "/client"
    And I should see a "dl#available-document-list" element
    And I should see 4 "dl#available-document-list dt" elements

  Scenario: The user should be able to create a new document
    When I am logged in as "userA"
    Then I am on "/client"

    Then I should see a "a#create-document" element

    When I follow "create-document"
    Then the response status code should be 200
    And I should see "Create a document"
    And I should see "Create a document"
    And I should see "Doc Variables"
    And I should see "Steps"
    And I should see a "textarea#doc_input" element
