import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 20)
        

    @task(3)
    def view_items(self):
        self.client.get("/api/v1/license/domain/")
        self.client.get("/api/v1/license/source/")
        self.client.get("/api/v1/license/restriction/")

        time.sleep(20)

        r = self.client.post(f"/api/v1/license/", json={
            "timestamp": "2023-11-24T10:36:37.726Z",
            "name": "string",
            "artifact": "",
            "license": "OpenRAIL",
            "data": False,
            "application": False,
            "model": False,
            "sourcecode": False,
            "derivatives": True,
            "researchOnly": False,
            "specifiedDomain_ids": [],
            "additionalRestriction_ids": []
            }
        )
        id = r.json()["id"]

        time.sleep(4)

        self.client.get(f"/api/v1/license/{id}/generate")