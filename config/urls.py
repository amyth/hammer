"""
Hammer URL Configuration
"""


from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
	## App urls
    url(r'^', include('apps.accounts.urls', namespace='accounts')),
    url(r'^', include('apps.overseer.urls', namespace='overseer')),

    ## Admin urls
    url(r'^manage/', admin.site.urls),
]
