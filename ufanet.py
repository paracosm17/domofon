import requests
from typing import Optional


class Ufanet:
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

        self._ufanet_host = "https://dom.ufanet.ru"
        self._ucams_host = "https://cloud.ucams.ru/api/v0"

        self.ufanet_token = self._get_token_ufanet()
        self.ucams_token = self._get_ucams_token()

        self._ufanet_headers = {"Authorization": f"JWT {self.ufanet_token}"}
        self._ucams_headers = {"Authorization": f"Bearer {self.ucams_token}"}

        self._skud = self._get_skud()

    def _get_token_ufanet(self):
        response = requests.post(
            self._ufanet_host+"/api-token-auth/",
            json={"contract": self.login, "password": self.password}
        )
        if response.ok:
            return response.json().get("token")

    def _get_skud(self, skud_id: Optional[int] = None):
        skuds = requests.get(
            self._ufanet_host+"/api/v0/skud/shared/",
            headers=self._ufanet_headers
        ).json()
        if skud_id:
            for skud in skuds:
                if skud.get("id") == skud_id:
                    return skud
        else:
            skud = skuds[0]
            return skud

    def _get_open_door_link(self):
        return f"https://dom.ufanet.ru/api/v0/skud/shared/{self._skud.get('id')}/open/"

    def _get_cctv_number(self):
        return self._skud.get("cctv_number")

    def _get_ucams_token(self):
        response = requests.post(
            self._ucams_host+"/auth/",
            json={"username": self.login, "password": self.password, "ttl": 172800}
        )
        if response.ok:
            return response.json().get("token")

    def get_stream_url(self):
        cctv = self._get_cctv_number()
        response = requests.post(
            self._ucams_host+"/cameras/this/",
            headers=self._ucams_headers,
            json={"fields": ["number", "token_l"], "token_l_ttl": "86400", "numbers": [cctv]}
        )
        if response.ok:
            token_for_stream = response.json().get("results")[0].get("token_l")
            self.ucams_live_token = token_for_stream
            return f"rtsp://flussonic-cloud-9.cams.ufanet.ru:554/{cctv}?token={token_for_stream}&tracks=v1a1"

    def open_door(self):
        response = requests.get(
            self._get_open_door_link(),
            headers=self._ufanet_headers
        )
