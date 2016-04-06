"""
Hammer URL Configuration
"""


from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('apps.overseer.urls', namespace='overseer')),
]
