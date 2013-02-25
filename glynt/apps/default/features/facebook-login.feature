# features/facebook-login.feature
Feature: Log a user in using facebook
  In order to use the system
  As an anonymous user
  I need to be able to log in using my facebook account

  Scenario: The user should not see the facebook login button at root
    Given I am on "/"
    Then the response should not contain "</fb:login-button>"
    Then the response should not contain "email,user_likes,user_about_me,read_stream"

  Scenario: The user should see the facebook login button at signup and login
    Given I am on "/client/login/"
    Then the response should contain "</fb:login-button>"
    Then the response should contain "email,user_likes,user_about_me,read_stream"

    Given I am on "/client/signup/"
    Then the response should contain "</fb:login-button>"
    Then the response should contain "email,user_likes,user_about_me,read_stream"

