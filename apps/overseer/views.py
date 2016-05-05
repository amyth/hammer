from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_protect


from apps.generic.views import LoginRequiredMixin
from apps.overseer.forms import UploadJsonDataForm
from apps.overseer.forms import UploadRawDataForm
from apps.overseer.models import NormalizedInstitute
from apps.overseer.models import InstituteAlias
from apps.overseer.models import InstituteMatches
from apps.overseer.models import UnnormalizedInstitute

from lib.utils import jsonresponse

import json


class Index(TemplateView):
    """
    Renders the index view template
    """

    template_name = 'overseer/index.html'
    typemap = {
        'normalized institutes': {'model':NormalizedInstitute, 'filters': None},
        'approved matches': {'model':InstituteMatches, 'filters': {'status': 2}},
        'unnormalized': {'model':UnnormalizedInstitute, 'filters':{'status':1}}
    }

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['upload_form'] = UploadJsonDataForm

        ## add paginated institute objects to the context

        page_no = self.request.GET.get('page', 1)
        list_type = self.request.GET.get('type', 'normalized institutes')
        _type = self.typemap.get(list_type)
        model = _type.get('model')
        filters = _type.get('filters')
        if filters:
            results = model.objects.filter(**filters)
        else:
            results = model.objects.all()
        
        #normalized_institutes = NormalizedInstitute.objects.all()
        # normalized_institutes = NormalizedInstitute.objects.filter(**self.typemap.get(list_type))
        
        if list_type == 'normalized institutes':
            results = sorted(results, key=lambda x: x.no_of_matches, reverse=True)
            results = [i for i in results if i.has_match]

        # if list_type == 'fresh':
        #     institutes = [i for i in institutes if not i.has_match]
        # elif list_type == 'unnormalized':
        #     institutes = [i for i in institutes if i.has_match]

        p = Paginator(results, settings.PAGINATION_STEP)
        context['page'] = p.page(page_no)
        context['paginator'] = p
        context['tabtypes'] = self.typemap.keys()         ##to be corrected as typemap is no more required

        return context


class UploadJsonDataView(FormView):

    template_name = 'overseer/index.html'
    form_class = UploadJsonDataForm
    success_url = reverse_lazy('overseer:index')
    
    def get_context_data(self, **kwargs): 
        context = super(UploadJsonDataView, self).get_context_data(**kwargs) 
        context['upload_form'] = context['form']
        
        del context['form']

        return context

    def form_valid(self, form, *args, **kwargs):
        form.save_data()
        messages.success(self.request, 'File successfully uploaded. We '\
                'are processing the file and changes will be visible in a '\
                'few minutes.')
        return super(UploadJsonDataView, self).form_valid(form)


class UploadRawDataView(FormView):

    template_name = 'overseer/index.html'
    form_class = UploadRawDataForm
    success_url = reverse_lazy('overseer:index')

    def get_context_data(self, **kwargs):
        context = super(UploadRawDataView, self).get_context_data(**kwargs)
        context['upload_raw_form'] = context['raw_form']
        print "here" , context 
        del context['form']

        return context

    def form_valid(self, form, *args, **kwargs):
        form.save_data()
        messages.success(self.request, 'File successfully uploaded. We '\
                'are processing the file and changes will be visible in a '\
                'few minutes.')
        return super(UploadRawDataView, self).form_valid(form)





def get_matches(request):
    string_id = request.GET.get('s')
    try:
        matches = NormalizedInstitute.objects.get(id=string_id).get_matches()
        print matches
    except (NormalizedInstitute.DoesNotExist, Exception) as err:
        #TODO: Log the error
        matches = []
    return jsonresponse(matches)


def matchstrings_form_submit(request):
    if request.method == 'GET':

        content = request.GET
        # print content

        for key in content.keys():
            m_id , m_val = key.split('_')
            # print "i = ", m_id 
            # print "v = ", m_val
            match_obj = InstituteMatches.objects.get(id=m_id)
            print match_obj.unnormalized_inst
            print "o_status = ", match_obj.status
            match_obj.status = m_val;
            print "n_status = ", match_obj.status 
            match_obj.save()

        return HttpResponse(
             json.dumps({'status': 'True'})
        )

    else:
        print "no hello"
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"})
        )
