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
        user = self.get_user("user1")
        self.client.force_authenticate(user)

        self.add_workflow(
            user, "hello-world", "example-assets/workflows/hello-world.cwl"
        )

        list_url = reverse("workflows:workflow-list", args=[user.username])
        list_resp = self.client.get(list_url)
        assert list_resp.json()[0]["name"] == "hello-world"

    def test_workflow_namespacing(self) -> None:
        user = self.get_user("user1")
        self.client.force_authenticate(user)

        self.add_workflow(
            user, "hello-world", "example-assets/workflows/hello-world.cwl"
        )

        other_user = self.get_user("user2")

        self.client.force_authenticate(other_user)
        list_url = reverse("workflows:workflow-list", args=[other_user.username])
        list_resp = self.client.get(list_url)
        assert len(list_resp.json()) == 0

    def test_workflow_detail(self) -> None:
        user = self.get_user("user1")
        self.client.force_authenticate(user)
        self.add_workflow(
            user, "hello-world", "example-assets/workflows/hello-world.cwl"
        )

        detail_url = reverse(
            "workflows:workflow-detail", args=[user.username, "hello-world"]
        )
        detail_resp = self.client.get(detail_url)
        assert detail_resp.status_code == status.HTTP_200_OK
        details = detail_resp.json()
        assert details["name"] == "hello-world"

    def test_workflow_file(self) -> None:
        user = self.get_user("user1")
        self.client.force_authenticate(user)

        self.add_workflow(
            user, "hello-world", "example-assets/workflows/hello-world.cwl"
        )

        file_url = reverse(
            "workflows:workflow-file", args=[user.username, "hello-world"]
        )
        file_response: FileResponse = self.client.get(file_url)
        file_str = b""
        for chunk in file_response.streaming_content:
            file_str += chunk
        with open("example-assets/workflows/hello-world.cwl", "rb") as workflow_file:
            assert file_str == workflow_file.read()

    def test_create_duplicate_workflow(self) -> None:
        user = self.get_user("user1")
        self.client.force_authenticate(user)

        self.add_workflow(
            user, "hello-world", "example-assets/workflows/hello-world.cwl"
        )

        create_url = reverse("workflows:workflow-list", args=[user.username])
        with open("example-assets/workflows/hello-world.cwl", "r") as workflow_file:
            response = self.client.post(
                create_url,
                data={
                    "name": "hello-world",
                    "file": workflow_file,
                },
            )
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_update_workflow_file(self) -> None:
        user = self.get_user("user1")
        self.client.force_authenticate(user)
        self.add_workflow(
            user, "hello-world", "example-assets/workflows/hello-world.cwl"
        )

        file_url = reverse(
            "workflows:workflow-file", args=[user.username, "hello-world"]
        )
        file_response: FileResponse = self.client.get(file_url)
        file_str = b""
        for chunk in file_response.streaming_content:
            file_str += chunk
        with open("example-assets/workflows/hello-world.cwl", "rb") as workflow_file:
            assert file_str == workflow_file.read()

        update_url = reverse(
            "workflows:workflow-file", args=[user.username, "hello-world"]
        )
        with open("example-assets/workflows/cdo.cwl", "r") as updated_file:
            resp = self.client.put(
                update_url,
                data={
                    "file": updated_file,
                },
            )
            assert resp.status_code == status.HTTP_204_NO_CONTENT

        file_url = reverse(
            "workflows:workflow-file", args=[user.username, "hello-world"]
        )
        file_response = self.client.get(file_url)
        file_str = b""
        for chunk in file_response.streaming_content:
            file_str += chunk
        with open("example-assets/workflows/cdo.cwl", "rb") as workflow_file:
            assert file_str == workflow_file.read()

    def get_user(self, name: str) -> User:
        """Convenience method to get a user by username and ensure it exists or panic
        to reduce boilerplate in the tests
        """
        user = User.objects.filter(username=name).first()
        assert not user is None
        return user

    def add_workflow(self, user: User, name: str, workflow_filename: str) -> None:
        """Adds the workflow file indicated to the system as belonging to the given user
        and panic if this fails
        """
        create_url = reverse("workflows:workflow-list", args=[user.username])
        with open(workflow_filename, "r") as workflow_file:
            response = self.client.post(
                create_url,
                data={
                    "name": name,
                    "file": workflow_file,
                },
            )
        assert response.status_code == status.HTTP_201_CREATED
