# features/user-hompeage.feature
Feature: Logged in User Dashboard
  In order to manage my documents
  As a user
  I need to be able to beable to view documentsI have created and their status'

  Scenario: The user should be able to see a list of public documents
    When I am logged in as "userA"
    Then I am on "/client"
    And I should see a "div#public-documents" element
    And I should see a "div#public-documents a.template-document" element

  Scenario: The user should be able to see a list of their created documents
    When I am logged in as "userA"
    Then I am on "/client"
    And I should see a "ul#my-documents" element

  @mink:zombie
  Scenario: The user should be able to create a document from a template
    When I am logged in as "userA"
    Then I am on "/client"
    And I follow "Test Buy a Gift Contract"
    Then I should see "Click to create new document..."
    And I click "h2#document-title"
    Then I should see a "h2#document-title form textarea" element
    And I should see a "h2#document-title form button" element

    When I fill in "value" with "Gift For a Friend"
    And I press "Save"
    Then I should be on "/doc/my/gift-for-a-friend/"

  @mink:zombie
  Scenario: The user should be able to edit their new document
    When I am logged in as "userA"
    Then I am on "/doc/my/gift-for-a-friend/"
    Then I should see "Gift for a Friend"
    And I should see "Your Name:"
    And I should see "Your Country:"
    And I should see a "span#document-md" element

#  Scenario: The user should be able to create a new document
#    When I am logged in as "userA"
#    Then I am on "/client"
#
#    Then I should see a "a#create-document" element
#
#    When I follow "create-document"
#    Then the response status code should be 200
#    And I should see "Create a document"
#    And I should see "Doc Variables"
#    And I should see "Steps"
#    And I should see a "textarea#doc_input" element
