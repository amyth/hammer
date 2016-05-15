from django.db.models import Q
from django.conf import settings
from django.contrib import messages

from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_protect

from apps.overseer import models
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
        'matches': {'model':NormalizedInstitute, 'filters': {'cummulative_matches__gt': 0}, 'order': '-cummulative_matches'},
        'approved matches': {'model':NormalizedInstitute, 'filters': {'no_of_approved_matches__gt': 0},  'order': '-no_of_approved_matches'},
        'reverse matches': {'model':UnnormalizedInstitute, 'filters': {'no_of_matches__gt': 0},  'order':'-frequency'},
        'unmatched': {'model':UnnormalizedInstitute, 'filters':{'no_of_matches': 0},  'order':'-frequency'},
    }


    def get_context_data(self, **kwargs):
        norm_list = 0
        user_group = 0
        r = self.request.user.groups.all()[0].id

        if r == 2:
            user_group = 2
        else:
            user_group = 1

        ## add paginated institute objects to the context

        page_no = self.request.GET.get('page', 1)
        
        searched_query = self.request.GET
        list_type = self.request.GET.get('type', 'matches')
        searched_string = self.request.GET.get('searched', ' ')

        print "list_type = ", list_type
        print "searched_string = ", searched_string
                
        context = super(Index, self).get_context_data(**kwargs)
        context['upload_form'] = UploadJsonDataForm

        flag = 0

        if len(searched_query) > 1:
            flag = 1

        _type = self.typemap.get(list_type)

        model = _type.get('model')
        filters = _type.get('filters')
        order = _type.get('order')

        if flag == 1:
            if list_type == 'matches':
                results = model.objects.order_by(order).filter(name__icontains= searched_string)
                # print "flag is equal to 1"
            elif list_type == 'approved matches':
                results = model.objects.order_by(order).filter(Q(name__icontains= searched_string ) & Q(no_of_approved_matches__gt = 0))
            elif list_type == 'reverse matches':
                results = model.objects.order_by(order).filter(Q(name__icontains= searched_string ) & Q(no_of_matches__gt = 0))
            else:
                results = model.objects.order_by(order).filter(name__icontains= searched_string )

        elif filters and order:
            results = model.objects.order_by(order).filter(**filters)
        elif filters:
            results = model.objects.filter(**filters)
        else:
            results = model.objects.all()
        
        if list_type == 'matches':
            norm_list = 1
        elif list_type == 'approved matches':
            norm_list = 2
        elif list_type == 'reverse matches':
            norm_list = 3
        else:
            norm_list = 4

        p = Paginator(results, settings.PAGINATION_STEP)
        context['page'] = p.page(page_no)
        context['paginator'] = p
        context['tabtypes'] = self.typemap.keys()
        context['norm_list'] = norm_list
        context['user_group'] = user_group

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

    except (NormalizedInstitute.DoesNotExist, Exception) as err:
        #TODO: Log the error
        matches = []
    return jsonresponse(matches)


def get_normalized_matches(request):
    string_id = request.GET.get('s')
    try:
        matches = UnnormalizedInstitute.objects.get(id=string_id).get_matches()

    except (UnnormalizedInstitute.DoesNotExist, Exception) as err:
        #TODO: Log the error
        matches = []
    return jsonresponse(matches)



def get_approved_matches(request):
    
    string_id = request.GET.get('s')

    try:
        appr_matches = NormalizedInstitute.objects.get(id=string_id).get_approved_matches()

    except (NormalizedInstitute.DoesNotExist, Exception) as err:
        #TODO: Log the error
        appr_matches = []
    return jsonresponse(appr_matches)

def get_aliases(request):
    
    string_id = request.GET.get('s')

    try:
        aliases = NormalizedInstitute.objects.get(id=string_id).get_approved_aliases()

    except (NormalizedInstitute.DoesNotExist, Exception) as err:
        #TODO: Log the error
        aliases = []
    return jsonresponse(aliases)


def matchstrings_form_submit(request):
    if request.method == 'GET':

        content = request.GET

        for key, value in content.items():
            m_id = key
            m_val = value

            match_obj = InstituteMatches.objects.get(id=m_id)

            match_obj.status = m_val;
            
            normalized_obj = NormalizedInstitute.objects.get(pk = match_obj.normalized_inst.pk)
            unnormalized_obj = UnnormalizedInstitute.objects.get(pk = match_obj.unnormalized_inst.pk)

            normalized_obj.no_of_matches = normalized_obj.no_of_matches - 1;
            normalized_obj.cummulative_matches = normalized_obj.cummulative_matches - unnormalized_obj.frequency

            m_val = int(m_val)

            if m_val == 2:
                normalized_obj.no_of_approved_matches = normalized_obj.no_of_approved_matches + 1;

            normalized_obj.save()
            match_obj.save()

        return HttpResponse(
             json.dumps({'status': 'True'})
        )

    else:
        print "no hello"
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"})
        )


def makealias_form_submit(request):
    if request.method == 'GET':

        content = request.GET

        for key, value in content.items():
            m_id = key
            m_val = value

            match_obj = InstituteMatches.objects.get(id=m_id)

            alias_id = match_obj.unnormalized_inst.id
            alias_name = match_obj.unnormalized_inst.name
            norm_ins = match_obj.normalized_inst
            norm_ins_id = match_obj.normalized_inst.id

            models.InstituteAlias.objects.create(
                normalized_institute= norm_ins,
                ins_alias= alias_name)

            normalized_obj = NormalizedInstitute.objects.get(pk = norm_ins_id)
            normalized_obj.no_of_aliases = normalized_obj.no_of_aliases + 1;
            normalized_obj.save()            

            objs_to_del = InstituteMatches.objects.filter(unnormalized_inst_id = alias_id)

            for obj in objs_to_del:
                norm_id = obj.normalized_inst.id
                norm_object = NormalizedInstitute.objects.get(pk = norm_id)

                if obj.status == 1:
                    norm_object.no_of_matches = norm_object.no_of_matches - 1

                elif obj.status == 2:
                    norm_object.no_of_approved_matches = norm_object.no_of_approved_matches - 1

                norm_object.save()

            InstituteMatches.objects.filter(unnormalized_inst_id = alias_id).delete()
            UnnormalizedInstitute.objects.filter(pk = alias_id).delete() 

        return HttpResponse(
             json.dumps({'status': 'True'})
        )

    else:
        print "no hello"
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"})
        )


def addnew_inst_form_submit(request):
    if request.method == 'POST':

        content = request.POST
        print content
        print content['inst_name']
        print content['city']
        print content['state']
        print content['country']
        print content['est']
        print content['extra_info']

        # models.NormalizedInstitute.objects.create(
        #         name = content['inst_name'],
        #         city = content['city'],
        #         state = content['state'],
        #         country = content['country'],
        #         established = content['est'],
        #         misc = content['extra_info'])


        return HttpResponse(
             json.dumps({'status': 'True'})
        )

    else:
        print "no hello"
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"})
        )

# def search_form_submit(request):
#     if request.method == 'POST':

#         content = request.POST
#         # print "content", content
#         searched_string = content['search-text']
#         print "searched_string_funct", searched_string

#         return HttpResponse(
#              json.dumps({'status': 'True'})
#         )

#     else:
#         print "no hello"
#         return HttpResponse(
#             json.dumps({"nothing to see": "this isn't happening"})
#         )