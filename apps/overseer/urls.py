from django.conf.urls import url

from apps.overseer import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
]
