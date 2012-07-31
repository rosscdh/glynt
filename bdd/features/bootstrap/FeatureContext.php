<?php

use Behat\Behat\Context\ClosuredContextInterface,
    Behat\Behat\Context\TranslatedContextInterface,
    Behat\Behat\Context\BehatContext,
    Behat\Behat\Exception\PendingException;
use Behat\Gherkin\Node\PyStringNode,
    Behat\Gherkin\Node\TableNode;

use Behat\MinkExtension\Context\MinkContext;

use Behat\Behat\Context\Step;
//
// Require 3rd-party libraries here:
//
//   require_once 'PHPUnit/Autoload.php';
//   require_once 'PHPUnit/Framework/Assert/Functions.php';
//

/**
 * Features context.
 */
class FeatureContext extends MinkContext {

    private 
        $loginUrl = '/client/login/';

    /**
     * Initializes context.
     * Every scenario gets it's own context object.
     *
     * @param array $parameters context parameters (set them up through behat.yml)
     */
    public function __construct(array $parameters)
    {
        // Initialize your context here
    }

    private function getUserPassword($username) {
        return 'test';
    }

    /**
     * @Given /^(?:|I )am logged in as "([^"]*)"$/
     */
    public function loggedInAs($username)
    {
        return array(
            new Step\Given(sprintf('I am on "%s"', $this->loginUrl)),
            new Step\When(sprintf('I fill in "username" with "%s"', $username)),
            new Step\When(sprintf('I fill in "password" with "%s"', $this->getUserPassword($username))),
            new Step\When('I press "Login"'),
            new Step\Then('the response status code should be 200')
        );
    }

    /**
     * @Then /^I click Facebook Login$/
     */
    public function iClickFacebookLogin()
    {
        //throw new PendingException();
    }
}
