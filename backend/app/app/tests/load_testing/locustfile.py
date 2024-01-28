import random
import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 20)
        

    @task(3)
    def view_items(self):
        self.client.get("/api/v1/license/domain/")
        self.client.get("/api/v1/license/source/")
        self.client.get("/api/v1/license/restriction/")

        time.sleep(random.randint(5, 30))

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
        if r.status_code == 200:
            id = r.json()["id"]

            # wait random time between 5 and 30 seconds
            time.sleep(random.randint(5, 30))

            for file_type in ["md", "txt", "rtf", "latex"]:
                self.client.get(f"/api/v1/license/{id}/generate?file_type={file_type}", name=f"/api/v1/license/id/generate?file_type={file_type}")
                time.sleep(1)