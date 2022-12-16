import io

from django.contrib.auth.models import User
from django.http.response import FileResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class WorkflowTests(APITestCase):
    def setUp(self) -> None:
        User.objects.create(username="user1")
        User.objects.create(username="user2")

    def test_create(self) -> None:
        user = User.objects.filter(username="user1").first()
        assert not user is None

        create_url = reverse("workflows:workflow-list", args=[user.username])
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

        list_url = reverse("workflows:workflow-list", args=[user.username])
        list_resp = self.client.get(list_url)
        assert list_resp.json()[0]["name"] == "hello-world"

    def test_workflow_namespacing(self) -> None:
        user = User.objects.filter(username="user1").first()
        assert not user is None
        create_url = reverse("workflows:workflow-list", args=[user.username])
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

        other_user = User.objects.filter(username="user2").first()
        assert not other_user is None

        self.client.force_authenticate(other_user)
        list_url = reverse("workflows:workflow-list", args=[other_user.username])
        list_resp = self.client.get(list_url)
        assert len(list_resp.json()) == 0

    def test_workflow_file(self) -> None:
        user = User.objects.filter(username="user1").first()
        assert not user is None

        create_url = reverse("workflows:workflow-list", args=[user.username])
        self.client.force_authenticate(user)
        with open("example-assets/workflows/hello-world.cwl", "r") as workflow_file:
            response = self.client.post(
                create_url,
                data={
                    "name": "hello-world",
                    "file": workflow_file,
                },
            )
        assert response.status_code == status.HTTP_201_CREATED

        file_url = reverse(
            "workflows:workflow-file", args=[user.username, "hello-world"]
        )
        file_response: FileResponse = self.client.get(file_url)
        file_str = b""
        for chunk in file_response.streaming_content:
            file_str += chunk
        with open("example-assets/workflows/hello-world.cwl", "rb") as workflow_file:
            assert file_str == workflow_file.read()
