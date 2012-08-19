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
    And I am on "/client/"
    Then I should see a "a[href='/doc/my/gift-for-a-friend/']" element
    When I follow "Gift For a Friend"
    Then the url should match "/doc/my/gift-for-a-friend/"
    And I should see "Gift for a Friend"
    And I should see "Your Name:"
    And I should see "Your Country:"
    And I should see a "span#document-md" element

  @mink:zombie
  Scenario: The user should be able to clone their new document
    When I am logged in as "userA"
    And I am on "/client/"
    Then I should see "Gift for a Friend"
    And I should see a "a[href='#clone']" element
    When I follow "clone-1"
    Then the url should match "/doc/my/copy-of-gift-for-a-friend/"

  @mink:zombie
  Scenario: The user should be able to delete their cloned document
    When I am logged in as "userA"
    And I am on "/client/"
    Then I should see "Copy of Gift For a Friend"
    And I should see a "a#delete-2[href='#delete']" element

    When I click "a#delete-2"
    Then I should see "Deleted Copy of Gift For a Friend"
    And I should see a "a#undelete-2" element

    Given I am on "/client/"
    Then I should not see "Copy of Gift For a Friend"
    And I should not see a "a#delete-2[href='#delete']" element


  @mink:zombie @wip
  Scenario: The user should be able to export their document as a PDF
    When I am logged in as "userA"
    And I am on "/client/"
    Then I should see "Gift For a Friend"
    And I should see a "a#export-1[href='#export']" element

