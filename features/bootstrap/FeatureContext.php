<?php
/**
* Please add: 
*    'Monolog' => $vendorDir . '/monolog/monolog/src/',
*    'Idiorm' => $vendorDir . '/Idiorm/',
* to the array found in vendor/composer/autoload_namespaces.php
*/
use Idiorm\ORM;
use Monolog\Logger;
use Monolog\Handler\StreamHandler;

use Behat\Behat\Context\ClosuredContextInterface,
    Behat\Behat\Context\TranslatedContextInterface,
    Behat\Behat\Context\BehatContext,
    Behat\Behat\Exception\PendingException;
use Behat\Gherkin\Node\PyStringNode,
    Behat\Gherkin\Node\TableNode,
    Behat\Mink\Driver\ZombieDriver,
    Behat\Mink\Driver\NodeJS\Server\ZombieServer;

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
        $loginUrl = '/client/login/',
        $logger;
    /**
     * Initializes context.
     * Every scenario gets it's own context object.
     *
     * @param array $parameters context parameters (set them up through behat.yml)
     */
    public function __construct(array $parameters)
    {
        ORM::configure('sqlite:/tmp/testserver.db');
        // setup logging
        $this->logger = new Logger('name');
        $this->logger->pushHandler(new StreamHandler('/tmp/behat.log', Logger::DEBUG));
        // setup guardian missing table permissions
        $this->setupGuardianDynamicPermissions();
        // Initialize your context here
    }

    private function setupGuardianDynamicPermissions() {
        // get content object type
        // 
        //ContentType.objects.get_for_model(model_obj)
        $ASSIGNED_PERMISSIONS = array(
            'profile' => array(
                'view_profile' => 'Can view profile',
                'change_profile' => 'Can change profile',
                'delete_profile' => 'Can delete profile',
            ),
            'user' => array(
                'change_user' => 'Can change user',
                'delete_user'=> 'Can delete user',
            ),
        );
        foreach ($ASSIGNED_PERMISSIONS as $model => $perms) {
            if ($model == 'profile') {
                $table = ORM::for_table('django_content_type')->where('model', 'clientprofile')->where('app_label', 'client')->find_one();
            }else{
                $table = ORM::for_table('django_content_type')->where('model', 'user')->where('app_label', 'auth')->find_one();
            }

            foreach ($perms as $perm => $name) {
                $permission = ORM::for_table('auth_permission')->where('codename', $perm)->where('content_type_id', $table->id)->find_one();

                if (!$permission) {
                    $this->logger->addWarning(sprintf('Could not find permission %s so creating it as content_type_id %d',$perm, $table->id));
                    $permission = ORM::for_table('auth_permission')->create();
                    $permission->name = $name;
                    $permission->codename = $perm;
                    $permission->content_type_id = $table->id;
                    $permission->save();
                }else{
                    $this->logger->addInfo(sprintf('Found permission %s under content_type_id %d',$perm, $table->id));
                }
            }
        }
    }

    private function getUsername($username) {
        $username = explode(':', $username);
        return $username[0];
    }

    private function getUserPassword($username) {
        $username = explode(':', $username);
        if (isset($username[1])) {
            return $username[1];
        } else {
            return 'test';
        }
    }

    /**
     * @Given /^(?:|I )am logged in as "([^"]*)"$/
     */
    public function loggedInAs($username)
    {
        return array(
            new Step\Given(sprintf('I am on "%s"', $this->loginUrl)),
            new Step\When(sprintf('I fill in "id_username" with "%s"', $this->getUsername($username))),
            new Step\When(sprintf('I fill in "id_password" with "%s"', $this->getUserPassword($username))),
            new Step\When('I press "Login"'),
            new Step\Then('the response status code should be 200')
        );
    }

    /**
     * @Given /^there is no "([^"]*)" user$/
     */
    public function thereIsNoUser($username_or_email)
    {
        if (strpos($username_or_email,'@') !== false) {
            $users = ORM::for_table('auth_user')->where('email', $username_or_email)->find_many();
        }else{
            $users = ORM::for_table('auth_user')->where('username', $username_or_email)->find_many();
        }

        if (count($users) >= 1) {
            foreach($users as $user) {
                $user->delete();
            }
        }
    }

    /**
     * @Then /^I click Facebook Login$/
     */
    public function iClickFacebookLogin()
    {
        //throw new PendingException();
    }

    /**
     * @Given /^I click "([^"]*)"$/
     */
    public function iClick($element)
    {
        $this->getSession()->wait(500, '$("'.$element.'").trigger("click")');
        $this->getSession()->wait(1000);
    }
}
