# pylint: disable=no-member

from st2common.runners.base_action import Action
import requests
from lib.utils import sanitize_payload


class SaltPackage(object):
    _expression_forms = ["glob", "grain", "pillar", "nodegroup", "list", "compound"]

    def __init__(self, client="local"):
        self._data = {"client": "", "fun": ""}
        self._data["client"] = client

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, key_value=[]):
        key, value = key_value
        self._data[key] = value


class SaltAction(Action):
    sensitive_keys = ["eauth", "password"]

    def __init__(self, config):
        super().__init__(config=config)
        self.url = self.config.get("api_url", None)
        self.eauth = self.config.get("eauth", None)
        self.username = self.config.get("username", None)
        self.password = self.config.get("password", None)
        self.verify_tls = self.config.get("verify_tls", self.config.get("verify_ssl", True))

    def login(self):
        """
        Authenticate with Salt API to receive an authentication token.
        """
        resp = requests.request(
            "POST",
            f"{self.url}/login",
            json={"eauth": self.eauth, "username": self.username, "password": self.password},
            verify=self.verify_tls,
        )
        token = resp.headers.get("X-Auth-Token", "failed-login")
        return token

    def generate_package(self, client="local", cmd=None, **kwargs):
        self.data = SaltPackage(client).data

        if cmd:
            self.data["fun"] = cmd
        if client == "local":
            self.data["tgt"] = kwargs.get("target", "*")
            self.data["tgt_type"] = kwargs.get("tgt_type", "glob")
        if isinstance(kwargs.get("args", []), list) and len(kwargs.get("args", [])) > 0:
            self.data["arg"] = kwargs["args"]
        if len(kwargs.get("data", {})) > 0:
            if kwargs["data"].get("kwargs", None) is not None:
                self.data["kwarg"] = kwargs["data"]["kwargs"]
        clean_payload = sanitize_payload(SaltAction.sensitive_keys, self.data)
        self.logger.info("[salt] Payload to be sent: %s", clean_payload)

    def generate_request(self):
        req = requests.Request(
            "POST",
            self.url,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "charset": "utf-8",
                "x-auth-token": self.login(),
                "User-Agent": "St2 Salt pack",
            },
        )
        return req.prepare()
