from st2tests.base import BaseActionTestCase

from local import SaltLocal
import requests_mock
from requests_mock.contrib import fixture
import testtools

__all__ = ["SaltLocalActionTestCase"]

no_args = {"module": "this.something", "target": "*", "tgt_type": "glob", "args": []}

one_arg = {
    "module": "this.something",
    "target": "*",
    "tgt_type": "glob",
    "args": ["os"],
}

multiple_args = {
    "module": "this.something",
    "target": "*",
    "tgt_type": "glob",
    "args": ["this", "that", "home"],
}

CONFIG_DATA = {"api_url": "https://example.com", "username": "this", "password": "that"}
requests_mock.Mocker.TEST_PREFIX = "test"


class SaltLocalActionTestCase(testtools.TestCase, BaseActionTestCase):
    action_cls = SaltLocal

    def setUp(self):
        super(SaltLocalActionTestCase, self).setUp()
        self.m = self.useFixture(fixture.Fixture())
        self.action = self.get_action_instance(config=CONFIG_DATA)
        # Mock authentication
        self.m.register_uri(
            "POST",
            "{}/login".format(CONFIG_DATA["api_url"]),
            json={},
            headers={"X-Auth-Token": "mock-auth-ok-token"},
        )
        # Mock run API
        self.m.register_uri("POST", "{}/".format(CONFIG_DATA["api_url"]), json={})

    def test_generic_action_no_args(self):
        self.action.run(**no_args)
        self.assertNotIn("arg", self.action.data)

    def test_generic_action_one_arg(self):
        self.action.run(**one_arg)
        self.assertIn("arg", self.action.data)
        self.assertIsInstance(self.action.data["arg"], list)

    def test_generic_action_multiple_args(self):
        self.action.run(**multiple_args)
        self.assertIn("arg", self.action.data)
        self.assertIsInstance(self.action.data["arg"], list)
