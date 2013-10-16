# -*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse
from glynt.casper import BaseLawyerCustomerProjectCaseMixin

from model_mommy import mommy

import json


class ProjectTeamManagementApiEndpointTest(BaseLawyerCustomerProjectCaseMixin):
    def setUp(self):
        super(ProjectTeamManagementApiEndpointTest, self).setUp()

        self.url = reverse('api_v2:project_team', kwargs={'uuid': self.project.uuid})
        self.client.login(username=self.customer_user.username, password=self.password)

    def valid_patch_object(self, team_ids):
        assert type(team_ids) is list
        return {"team": team_ids}

    def invalid_patch_object(self, team_ids):
        """
        return an incorrect patch object
        """
        assert type(team_ids) is list
        return team_ids

    def ensure_correct_team_response(self, resp, expected_status=200):
        """
        response should contain
        {"team": [{object}]}
        """
        self.assertEqual(expected_status, resp.status_code)

        # ensure is json
        json_response = json.loads(resp.content)
        self.assertEqual(dict, type(json_response))

        # test generic json response
        self.assertEqual([u'team'], json_response.keys())
        self.assertEqual(list, type(json_response['team']))

        return json_response

    def test_invalid_unauthorised_user_access(self):
        self.client.logout()
        resp = self.client.put(self.url)
        self.assertEqual(403, resp.status_code)  #forbidden

        random_customer_user = mommy.make('auth.User', username='unauthorised-customer', first_name='Unuathorised', last_name='Customer', email='customer+unauthorised@lawpal.com')
        password = 'test'
        random_customer_user.set_password(password)

        self.client.login(username=random_customer_user.username, password=password)
        resp = self.client.put(self.url)
        self.assertEqual(403, resp.status_code)  #forbidden

    def test_project_participants_api_endpoint_invalid_request_types(self):
        """
        PUT should throw a 403
        """
        resp = self.client.put(self.url)
        # PUT should throw 405 method not allowed
        self.assertEqual(405, resp.status_code)

        # POST should also throw an invalid error
        resp = self.client.post(self.url)
        # PUT should throw 405 method not allowed
        self.assertEqual(405, resp.status_code)

    def test_project_participants_api_endpoint_GET(self):
        resp = self.client.get(self.url)

        json_response = self.ensure_correct_team_response(resp=resp)

        # the user and the lawyer
        self.assertEqual(2, len(json_response['team']))

        # test team item 0 keys (customer)
        for t in json_response['team']:
            # test keys are correct
            self.assertEqual([u'username', u'first_name', u'last_name', u'is_customer', u'photo', u'email', u'is_lawyer', u'full_name', u'id'], t.keys())

            # test for values
            if t.get('is_customer') is True:
                self.assertEqual([u'customer', u'Customer', u'A', True, u'/static/img/default_avatar.png', u'customer+test@lawpal.com', False, u'Customer A', self.customer_user.pk], t.values())

            elif t.get('is_lawyer') is True:
                self.assertEqual([u'lawyer', u'Lawyer', u'A', False, u'/static/img/default_avatar.png', u'lawyer+test@lawpal.com', True, u'Lawyer A', self.lawyer_user.pk], t.values())        

    def test_invalid_PATCH_object(self):
        resp = self.client.patch(path=self.url, data=self.invalid_patch_object(team_ids=[1, 2, 3, 4, 5]), content_type='application/json')
        self.assertEqual(400, resp.status_code)

    def test_project_participants_api_endpoint_PATCH(self):
        """
        Add a new user to the participants endpoint
        Remove that user and ensure all is updated
        """
        resp = self.client.get(self.url)
        json_response = json.loads(resp.content)
        team = [i['id'] for i in json_response['team']]

        new_user = mommy.make('auth.User', username='some-random-monkey', first_name='Some', last_name='RandomMonkey', email='invited-participant@lawpal.com')

        # add new_user pk to the team
        team.append(new_user.pk)
        # convert list to valid object
        team = self.valid_patch_object(team_ids=team)
        json_team = json.dumps(team)

        resp = self.client.patch(path=self.url, data=json_team, content_type='application/json')

        json_response = self.ensure_correct_team_response(resp=resp, expected_status=202)

        # access the team object
        team = json_response['team']
        self.assertEqual(3, len(team))

        # test item 2 keys (participant)
        team = json_response['team'][2]

        self.assertEqual([u'username', u'first_name', u'last_name', u'is_customer', u'photo', u'email', u'is_lawyer', u'full_name', u'id'], team.keys())
        self.assertEqual([u'some-random-monkey', u'Some', u'RandomMonkey', False, u'/static/img/default_avatar.png', u'invited-participant@lawpal.com', False, u'Some RandomMonkey', new_user.pk], team.values())

        # test participant removal
        team = [i['id'] for i in json_response['team']]
        team.remove(new_user.pk)
        # convert list to valid object
        team = self.valid_patch_object(team_ids=team)

        json_team = json.dumps(team)

        resp = self.client.patch(path=self.url, data=json_team, content_type='application/json')
        json_response = json.loads(resp.content)
        team = json_response['team']

        # we only have 2 participants now
        self.assertEqual(2, len(team))
        # extract the ids
        team_ids = [i['id'] for i in json_response['team']]
        # ensure the new_user is no longer in the participants list
        self.assertTrue(new_user.pk not in team_ids)
