from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.overseer import views


urlpatterns = [
    url(r'^$', login_required(views.Index.as_view()), name='index'),
    url(r'^upload_data/$', login_required(views.UploadJsonDataView.as_view()), name='submit-file'),
    url(r'^upload_raw_data/$', login_required(views.UploadRawDataView.as_view()), name='submit-raw-file'),
    url(r'^get_matches/$', views.get_matches, name="get_matches"),
    url(r'^get_approved_matches/$', views.get_approved_matches, name="get_approved_matches"),
    url(r'^get_reverse_matches/$', views.get_reverse_matches, name="get_reverse_matches"),
    url(r'^get_normalized_details/$', views.get_normalized_details, name="get_normalized_details"),
    url(r'^get_aliases/$', views.get_aliases, name="get_aliases"),
    url(r'^get_discarded/$', views.get_discarded, name="get_discarded"),
    url(r'^get_skipped/$', views.get_skipped, name="get_skipped"),
    url(r'^matchstrings_form_submit/$', views.matchstrings_form_submit, name="matchstrings_form_submit"),
    url(r'^makealias_form_submit/$', views.makealias_form_submit, name="makealias_form_submit"),
    url(r'^makeapproved_form_submit/$', views.makeapproved_form_submit, name="makeapproved_form_submit"),
    url(r'^addnew_inst_form_submit/$', views.addnew_inst_form_submit, name="addnew_inst_form_submit"),
    url(r'^addnew_alias_form_submit/$', views.addnew_alias_form_submit, name="addnew_alias_form_submit")
    
]