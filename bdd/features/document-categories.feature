# features/document-categories.feature
Feature: View Documents by Category
  In order to select specific documents
  As any user
  I need to be able to select a document from a categorized list

  Scenario: The user should see the a list of document categories on the homepage
    Given I am on "/"
    Then I should see a "ul#document-category-list" element
    Then I should see a "ul#document-category-list li h3" element
    Then I should see a "ul#document-category-list li ul.document-category" element
    Then I should see a "ul#document-category-list li ul.document-category li" element
    Then I should see a "ul#document-category-list li ul.document-category li a.document-link" element

  Scenario: The user should be able to click on a sub-category
    Given I am on "/"
    When I follow "a.document-link:first"
    Then the response status code should be 200
    And the url should match "/doc/category/"
