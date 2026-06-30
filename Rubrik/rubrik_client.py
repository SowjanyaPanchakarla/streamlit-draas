import os
import requests
import urllib3
from dotenv import load_dotenv

load_dotenv()

urllib3.disable_warnings()

class RubrikClient:

    def __init__(self):

        self.client_id = os.getenv("RUBRIK_CLIENT_ID")
        self.client_secret = os.getenv("RUBRIK_CLIENT_SECRET")

        self.token_url = os.getenv(
            "RUBRIK_TOKEN_URL",
            "https://unisys-demo.my.rubrik.com/api/client_token"
        )

        self.graphql_url = os.getenv(
            "RUBRIK_GRAPHQL_URL",
            "https://unisys-demo.my.rubrik.com/api/graphql"
        )

        self.token = None

    def get_access_token(self):

        if self.token:
            return self.token

        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        response = requests.post(
            self.token_url,
            json=payload,
            verify=False,
            timeout=30
        )

        response.raise_for_status()

        self.token = response.json()["access_token"]

        return self.token

    def execute_query(self, query):

        token = self.get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            self.graphql_url,
            json={"query": query},
            headers=headers,
            verify=False,
            timeout=60
        )

        response.raise_for_status()

        return response.json()