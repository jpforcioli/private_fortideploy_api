# coding: utf-8
"""
Class to operate a private FortiDeploy
"""

import requests
import base64
import json
import logging

logging.captureWarnings(True)


class FortiDeploy:
    """
    Class to operate a private FortiDeploy
    """

    def __init__(self):
        self._debug = False
        self.s = requests.Session()
        self.headers = {
            "Content-Type": "application/json",
        }
        self.s.headers.update(self.s.headers)
        self.base_url = "https://{}/api/v1"

    def login(self, ip, login, password):
        self.base_url = self.base_url.format(ip)
        url = self.base_url + "/auth"
        data = {
            "username": login,
            "password": password,
        }
        r = self.s.post(url, data, verify=False)
        r.raise_for_status()

        response = r.json()
        self.accessToken = response["accessToken"]
        self.headers["Authorization"] = "Bearer {}".format(self.accessToken)
        self.s.headers.update(self.headers)

        self.debug_print(r)

    def logout(self):
        url = self.base_url + "/logout"
        r = self.s.post(url)

        self.debug_print(r)

    def backup(self):
        url = self.base_url + "/backup"
        r = self.s.get(url)
        r.raise_for_status()

        response = r.json()
        content = response["content"]

        self.debug_print(r)

        return content

    def restore(self, content, append=True):
        """
        Restore Private FortiDeploy's rules.

        Args:
            content (bytes): Base64 encoded backup file
            append (bool, optional): True: append, False: overwrite. Defaults to True.
        """
        url = self.base_url + "/restore"

        # appendMode: 0 => overwrite
        data = {
            "appendMode": 0,
            "content": content.decode(),
        }
        print(data)

        if append:
            data["appendMode"] = 1

        r = self.s.post(url, json=data)
        r.raise_for_status()

        self.debug_print(r)

    def debug(self, value):
        if value == "on":
            self._debug = True
        else:
            self._debug = False

    def debug_print(self, response):
        if self._debug:
            # Print the request:
            method = response.request.method
            url = response.request.url
            print("==> REQUEST:\n\n{} {}".format(method, url))
            for key in response.request.headers:
                value = response.request.headers[key]
                print("{}: {}".format(key, value))

            body = response.request.body

            if body != None:
                try:
                    json_object = json.loads(body)
                except ValueError:
                    print("\n{}".format(body))
                else:
                    print(
                        "\n{}".format(
                            json.dumps(json.loads(response.request.body), indent=4)
                        )
                    )

            # Print the response:
            print("\n==> RESPONSE: \n")
            print(response.status_code)
            for key in response.headers:
                value = response.headers[key]
                print("{}: {}".format(key, value))

            print("\n{}".format(json.dumps(response.json(), indent=4)))


if __name__ == "__main__":

    ip = "192.168.194.9"
    login = "admin"
    password = "pass"

    fdp = FortiDeploy()
    fdp.debug("on")
    fdp.login(ip, login, password)

    # To export base64 encoded Rules Config
    # b64Content = fdp.backup()
    # print base64.b64decode(b64Content)

    # To restore (i.e. import) base64 encoded Rules Config
    file = "436_rules.config.cfg"
    f = open(file)
    content = f.read()
    base64Content = base64.b64encode(content)
    fdp.restore(base64Content, append=True)
    fdp.logout()
