''' Django notification urls file '''
# -*- coding: utf-8 -*-
from distutils.version import StrictVersion  # pylint: disable=no-name-in-module,import-error

from django import get_version

from . import views

if StrictVersion(get_version()) >= StrictVersion('2.0'):
    from django.urls import re_path as pattern
else:
    from django.conf.urls import url as pattern


urlpatterns = [
    pattern(r'^mark-all-as-read/$', views.mark_all_as_read, name='mark_all_as_read'),
    pattern(r'^mark-all-as-unread/$', views.mark_all_as_unread, name='mark_all_as_unread'),
    pattern(r'^mark-as-read/(?P<notification_id>\d+)/$', views.mark_as_read, name='mark_as_read'),
    pattern(r'^mark-as-unread/(?P<notification_id>\d+)/$', views.mark_as_unread, name='mark_as_unread'),
    pattern(r'^delete/(?P<notification_id>\d+)/$', views.delete, name='delete'),
    pattern(r'^unread_count/$', views.live_unread_notification_count, name='live_unread_notification_count'),
    pattern(r'^all_count/$', views.live_all_notification_count, name='live_all_notification_count'),
    pattern(r'^unread_list/$', views.live_unread_notification_list, name='live_unread_notification_list'),
    pattern(r'^all_list/', views.live_all_notification_list, name='live_all_notification_list'),
]

app_name = 'notifications'
