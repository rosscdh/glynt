# features/facebook-login.feature
Feature: Log a user in using facebook
  In order to use the system
  As an anonymous user
  I need to be able to log in using my facebook account

  @mink:sahi
  Scenario: The user should see the facebook login button
    Given I am on "/"
    Then the response should contain "</fb:login-button>"
    Then the response should contain "email,user_likes,user_about_me,read_stream"

  @mink:sahi
  Scenario: The user should be able to click the facebook button and log in
    Given I am on "/"
    Then I click Facebook Login