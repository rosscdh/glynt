Feature: Register as a lawyer
    In order to be registered as a lawyer
    An unauthenticated user 
    I need to be able to use linkedin or angelllist to signup

Scenario: Login as lawyer
    Given I am on "/"
    I should see a "button.linkedin" element
    And I should see a "button.angel" element 
    When I click on "button.linkedin" 
    I should be prompted to authenticate via linkedin and return logged in
    When I click on "button.angel" 
    I should be prompted to authenticate via linkedin and return logged in

Scenario: Logged in as A lawyer
    As I have chosen the lawyer path
    I should land on "/lawyers/"
    I should see "Get your profile ready"
    I should see a "Prepare your profile" element

Scenario: Prepare lawyer profile
    As I have chosen the lawyer path
    Given I am on "/lawyers/"
    Then I follow "Prepare your profile"
    I should see "Confirm your details"
    And I should see a "form[action=/lawyers/setup/profile/]"
