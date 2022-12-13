from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class WorkflowTests(APITestCase):
    def setUp(self) -> None:
        User.objects.create(username="admin")

    def test_create(self) -> None:
        create_url = reverse("workflows:workflow-list")
        user = User.objects.filter(username="admin").first()
        assert not user is None

        workflow_file = open("example-assets/workflows/hello-world.cwl", "r")
        self.client.force_authenticate(user)
        response = self.client.post(
            create_url,
            data={
                "name": "hello-world",
                "file": workflow_file,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED

        workflow_url = reverse("workflows:workflow-list")
        list_resp = self.client.get(workflow_url)
        assert list_resp.json()[0]["name"] == "hello-world"
