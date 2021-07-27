# -*- coding: utf-8 -*-
""" Django Notifications example views """
from django.shortcuts import get_object_or_404
from django.utils.module_loading import import_string
from django.views.decorators.cache import never_cache
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from notifications import settings
from notifications.models import Notification
from notifications.settings import get_config

from .pagination import MyPageNumberPagination

NotificationSerializer = import_string(settings.get_config()["SERIALIZER_CLASS"])


@api_view(["GET"])
@authentication_classes([JWTAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_all_as_read(request):
    request.user.notifications.mark_all_as_read()

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_all_as_unread(request):
    request.user.notifications.mark_all_as_unread()

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_as_read(request, notification_id=None):

    notification = get_object_or_404(
        Notification, recipient=request.user, id=notification_id
    )
    notification.mark_as_read()

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_as_unread(request, notification_id=None):

    notification = get_object_or_404(
        Notification, recipient=request.user, id=notification_id
    )
    notification.mark_as_unread()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request, notification_id=None):

    notification = get_object_or_404(
        Notification, recipient=request.user, id=notification_id
    )

    if settings.get_config()["SOFT_DELETE"]:
        notification.deleted = True
        notification.save()
    else:
        notification.delete()

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@never_cache
def live_unread_notification_count(request):
    data = {
        "unread_count": request.user.notifications.unread().count(),
    }
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@never_cache
def live_unread_notification_list(request):
    """Return a json with a unread notification list"""
    notification = request.user.notifications.unread()
    paginator = MyPageNumberPagination()
    paginated_notifications = paginator.paginate_queryset(notification, request)
    serializer = NotificationSerializer(paginated_notifications, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@authentication_classes([JWTAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@never_cache
def live_all_notification_list(request):
    """Return a json with a unread notification list"""
    notification = request.user.notifications.all()
    paginator = MyPageNumberPagination()
    paginated_notifications = paginator.paginate_queryset(notification, request)
    serializer = NotificationSerializer(paginated_notifications, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@authentication_classes([JWTAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def live_all_notification_count(request):
    data = {
        "all_count": request.user.notifications.count(),
    }
    return Response(data=data, status=status.HTTP_200_OK)
