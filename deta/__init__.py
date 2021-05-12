import os
import urllib.error
import urllib.request
import json

from .base import Base
from .drive import Drive


try:
    from detalib.app import App

    app = App()
except Exception:
    pass

__version__ = 0.8


class Deta:
    def __init__(self, project_key: str = None, *, project_id: str = None):
        self.project_key = project_key or os.getenv("DETA_PROJECT_KEY")
        assert self.project_key, "No project key defined"

        self.project_id = project_id
        if not self.project_id:
            self.project_id = self.project_key.split("_")[0]

    def Base(self, name: str, host: str = None):
        return Base(name, self.project_key, self.project_id, host)

    def Drive(self, name: str, host: str = None):
        return Drive(
            name=name,
            project_key=self.project_key,
            project_id=self.project_id,
            host=host,
        )

    def send_email(self, to, subject, message, charset="UTF-8"):
        return send_email(to, subject, message, charset)


def send_email(to, subject, message, charset="UTF-8"):
    pid = os.getenv("AWS_LAMBDA_FUNCTION_NAME")
    url = os.getenv("DETA_MAILER_URL")
    api_key = os.getenv("DETA_PROJECT_KEY")
    endpoint = f"{url}/mail/{pid}"

    to = to if type(to) == list else [to]
    data = {
        "to": to,
        "subject": subject,
        "message": message,
        "charset": charset,
    }

    headers = {"X-API-Key": api_key}

    req = urllib.request.Request(endpoint, json.dumps(data).encode("utf-8"), headers)

    try:
        resp = urllib.request.urlopen(req)
        if resp.getcode() != 200:
            raise Exception(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise Exception(e.reason)
