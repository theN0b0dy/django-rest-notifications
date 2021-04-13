# -*- coding: utf-8 -*-
''' Django Notifications example views '''
from django.shortcuts import get_object_or_404
from notifications import settings
from notifications.models import Notification
from notifications.utils import id2slug, slug2id
from notifications.settings import get_config
from django.views.decorators.cache import never_cache

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.utils.module_loading import import_string



NotificationSerializer = import_string(settings.get_config()['SERIALIZER_CLASS'])

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_all_as_read(request):
    request.user.notifications.mark_all_as_read()

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_all_as_unread(request):
    request.user.notifications.mark_all_as_unread()

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_as_read(request, notification_id=None):

    notification = get_object_or_404(
        Notification, recipient=request.user, id=notification_id)
    notification.mark_as_read()

    return Response(status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_as_unread(request, notification_id=None):

    notification = get_object_or_404(
        Notification, recipient=request.user, id=notification_id)
    notification.mark_as_unread()

    return Response(status=status.HTTP_200_OK)



@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request, notification_id=None):

    notification = get_object_or_404(
        Notification, recipient=request.user, id=notification_id)

    if settings.get_config()['SOFT_DELETE']:
        notification.deleted = True
        notification.save()
    else:
        notification.delete()

    return Response(status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@never_cache
def live_unread_notification_count(request):
    data = {
        'unread_count': request.user.notifications.unread().count(),
    }
    return Response(data=data, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@never_cache
def live_unread_notification_list(request):
    ''' Return a json with a unread notification list '''
    default_num_to_fetch = get_config()['NUM_TO_FETCH']
    try:
        # If they don't specify, make it 5.
        num_to_fetch = request.GET.get('max', default_num_to_fetch)
        num_to_fetch = int(num_to_fetch)
        if not (1 <= num_to_fetch <= 100):
            num_to_fetch = default_num_to_fetch
    except ValueError:  # If casting to an int fails.
        num_to_fetch = default_num_to_fetch

    unread_list = []
    notification = request.user.notifications
    serializer = NotificationSerializer(notification, many=True)

    data = {
        'unread_count': request.user.notifications.unread().count(),
        'unread_list': serializer.data
    }
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@never_cache
def live_all_notification_list(request):
    ''' Return a json with a unread notification list '''
    default_num_to_fetch = get_config()['NUM_TO_FETCH']
    try:
        # If they don't specify, make it 5.
        num_to_fetch = request.GET.get('max', default_num_to_fetch)
        num_to_fetch = int(num_to_fetch)
        if not (1 <= num_to_fetch <= 100):
            num_to_fetch = default_num_to_fetch
    except ValueError:  # If casting to an int fails.
        num_to_fetch = default_num_to_fetch

    all_list = []
    notification = request.user.notifications
    serializer = NotificationSerializer(notification, many=True)

    data = {
        'all_count': request.user.notifications.count(),
        'all_list': serializer.data
    }
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def live_all_notification_count(request):
    data = {
        'all_count': request.user.notifications.count(),
    }
    return Response(data=data, status=status.HTTP_200_OK)
