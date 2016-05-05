from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.overseer import views

urlpatterns = [
    url(r'^$', login_required(views.Index.as_view()), name='index'),
    url(r'^upload_data/$', login_required(views.UploadJsonDataView.as_view()), name='submit-file'),
    url(r'^upload_raw_data/$', login_required(views.UploadRawDataView.as_view()), name='submit-raw-file'),
    url(r'^get_matches/$', views.get_matches, name="get_matches"),
    url(r'^matchstrings_form_submit/$', views.matchstrings_form_submit, name="matchstrings_form_submit"),
]