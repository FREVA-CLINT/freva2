import logging

from django.contrib.auth.models import AnonymousUser, User
from rest_framework.exceptions import NotAuthenticated
from rest_framework.request import Request


def authed_user(request: Request) -> User:
    match request.user:
        case User() as user:
            return user
        case AnonymousUser():
            raise NotAuthenticated()
        case _ as unknown_user_type:
            logging.error(
                "User logged in as an unexpected user type", unknown_user_type
            )
            raise NotAuthenticated()
