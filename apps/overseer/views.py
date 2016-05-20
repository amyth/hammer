from ordereddict import OrderedDict

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
from apps.overseer.models import InstituteType

from lib.utils import jsonresponse

import json


class Index(TemplateView):
    """
    Renders the index view template
    """

    SEARCH_FIELD = 'name'
    SEARCH_TYPE = 'icontains'

    template_name = 'overseer/index.html'
    typemap = OrderedDict()
    typemap['matches'] = {'model':NormalizedInstitute, 'filters': {'cummulative_matches__gt': 0}, 'order': '-cummulative_matches'}
    typemap['reverse matches'] = {'model':UnnormalizedInstitute, 'filters': {'no_of_matches__gt': 0},  'order':'-frequency'}
    typemap['approved matches'] = {'model':NormalizedInstitute, 'filters': {'no_of_approved_matches__gt': 0},  'order': '-no_of_approved_matches'}
    typemap['unmatched'] = {'model':UnnormalizedInstitute, 'filters':{'status': 0},  'order':'-frequency'}


    def get_context_data(self, **kwargs):

        ## get user group of user
        user_group = 0
        r = self.request.user.groups.all()[0].id

        if r == 2:
            user_group = 2
        else:
            user_group = 1

        ## add paginated institute objects to the context

        page_no = self.request.GET.get('page', 1)
        
        context = super(Index, self).get_context_data(**kwargs)
        context['upload_form'] = UploadJsonDataForm

        ## getting the searched query if any

        list_type = self.request.GET.get('type', 'matches')
        searched_string = self.request.GET.get('searched', None)
                

        _type = self.typemap.get(list_type)

        model = _type.get('model')
        filters = _type.get('filters')
        order = _type.get('order')

        ## setting value of filters, in case there is a search query

        if searched_string:
            search_filter = "%s__%s" % (self.SEARCH_FIELD, self.SEARCH_TYPE)
            search_filters = {search_filter: searched_string}
            if list_type == 'unmatched':
                search_filters.update(filters)

            ## update the filters with search search_filters
            filters = search_filters

        if filters and order:
            results = model.objects.order_by(order).filter(**filters)
        elif filters:
            results = model.objects.filter(**filters)
        else:
            results = model.objects.all()
        

        norm_list = 0

        if list_type == 'matches':
            norm_list = 1
        elif list_type == 'approved matches':
            norm_list = 2
        elif list_type == 'reverse matches':
            norm_list = 3
        else:
            norm_list = 4

        inst_types = InstituteType.objects.all()

        p = Paginator(results, settings.PAGINATION_STEP)
        context['page'] = p.page(page_no)
        context['paginator'] = p
        context['tabtypes'] = self.typemap.keys()
        context['norm_list'] = norm_list
        context['user_group'] = user_group
        context['inst_types'] = inst_types

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



## To get the details of a normalised institute

def get_normalized_details(request):
    string_id = request.GET.get('s')
    try:
        details = []
        institute = NormalizedInstitute.objects.get(id=string_id)        

        details.append(institute.id)
        details.append(institute.name)
        details.append(institute.city)
        details.append(institute.state)
        details.append(institute.country)
        details.append(institute.established)


    except (NormalizedInstitute.DoesNotExist, Exception) as err:
        #TODO: Log the error
        details = []
    return jsonresponse(details)




def get_reverse_matches(request):
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


def get_discarded(request):
    
    string_id = request.GET.get('s')

    try:
        discarded = NormalizedInstitute.objects.get(id=string_id).get_discarded_matches()

    except (NormalizedInstitute.DoesNotExist, Exception) as err:
        #TODO: Log the error
        discarded = []
    return jsonresponse(discarded)


def get_skipped(request):
    
    string_id = request.GET.get('s')

    try:
        skipped = NormalizedInstitute.objects.get(id=string_id).get_skipped_matches()

    except (NormalizedInstitute.DoesNotExist, Exception) as err:
        #TODO: Log the error
        skipped = []
    return jsonresponse(skipped)


def matchstrings_form_submit(request):
    if request.method == 'GET':

        content = request.GET

        for key, value in content.items():
            m_id = key
            m_val = value

            match_obj = InstituteMatches.objects.get(id=m_id)

            match_obj.status = m_val
            
            normalized_obj = NormalizedInstitute.objects.get(id = match_obj.normalized_inst.pk)
            unnormalized_obj = UnnormalizedInstitute.objects.get(id = match_obj.unnormalized_inst.pk)

            normalized_obj.no_of_matches = normalized_obj.no_of_matches - 1
            normalized_obj.cummulative_matches = normalized_obj.cummulative_matches - unnormalized_obj.frequency
            unnormalized_obj.no_of_matches = unnormalized_obj.no_of_matches - 1
            unnormalized_obj.save()
            
            m_val = int(m_val)

            if m_val == 2:
            
                normalized_obj.no_of_approved_matches = normalized_obj.no_of_approved_matches + 1
                matches_list = InstituteMatches.objects.filter(
                    Q(unnormalized_inst_id = unnormalized_obj.id) & ~Q(id = m_id))

                for match in matches_list:

                    if match.status == 1:
                        norm_obj = NormalizedInstitute.objects.get(pk = match.normalized_inst.pk)
                        
                        norm_obj.no_of_matches = norm_obj.no_of_matches - 1
                        norm_obj.cummulative_matches = norm_obj.cummulative_matches - unnormalized_obj.frequency
                        unnormalized_obj.no_of_matches = unnormalized_obj.no_of_matches - 1
                        norm_obj.save()
                        unnormalized_obj.save()
                    
                    match.status = 5
                    match.save()        


            normalized_obj.save()
            match_obj.save()

        return HttpResponse(
             json.dumps({'status': 'True'})
        )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"})
        )


def makeapproved_form_submit(request):
    if request.method == 'GET':

        content = request.GET

        for key, value in content.items():
            m_id = key
            m_val = int(value)

            match_obj = InstituteMatches.objects.get(id=m_id)

            match_obj.status = m_val
            
            normalized_obj = NormalizedInstitute.objects.get(id = match_obj.normalized_inst.pk)
            unnormalized_obj = UnnormalizedInstitute.objects.get(id = match_obj.unnormalized_inst.pk)

            normalized_obj.no_of_approved_matches = normalized_obj.no_of_approved_matches + 1

            matches_list = InstituteMatches.objects.filter(
                Q(unnormalized_inst_id = unnormalized_obj.id) & ~Q(id = m_id))

            for match in matches_list:

                if match.status == 1:
                    
                    norm_obj = NormalizedInstitute.objects.get(pk = match.normalized_inst.pk)
                    
                    norm_obj.no_of_matches = norm_obj.no_of_matches - 1
                    norm_obj.cummulative_matches = norm_obj.cummulative_matches - unnormalized_obj.frequency
                    unnormalized_obj.no_of_matches = unnormalized_obj.no_of_matches - 1
                    match.status = 5
                    
                    norm_obj.save()
                    unnormalized_obj.save()
                        
                elif match.status == 3:
                    match.status = 5

                match.save()

            normalized_obj.save()
            match_obj.save()

        return HttpResponse(
             json.dumps({'status': 'True'})
        )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"})
        )



def makealias_form_submit(request):
    if request.method == 'GET':

        content = request.GET

        for key, value in content.items():
            m_id = key
            m_val = int(value)

            match_obj = InstituteMatches.objects.get(id=m_id)
            
            unnormalized_obj = UnnormalizedInstitute.objects.get(id = match_obj.unnormalized_inst.pk)
            normalized_obj = NormalizedInstitute.objects.get(id = match_obj.normalized_inst.pk)

            if m_val == 3:
                match_obj.status = 1
                normalized_obj.no_of_matches = normalized_obj.no_of_matches + 1
                normalized_obj.cummulative_matches = normalized_obj.cummulative_matches + unnormalized_obj.frequency
                normalized_obj.no_of_approved_matches = normalized_obj.no_of_approved_matches - 1
                unnormalized_obj.no_of_matches = unnormalized_obj.no_of_matches + 1

                matches_list = InstituteMatches.objects.filter(
                    Q(unnormalized_inst_id = match_obj.unnormalized_inst.pk) & ~Q(id = m_id))

                for match in matches_list:    
                    
                    norm_obj = NormalizedInstitute.objects.get(id = match.normalized_inst.pk)

                    norm_obj.no_of_matches = norm_obj.no_of_matches + 1
                    norm_obj.cummulative_matches = norm_obj.cummulative_matches + unnormalized_obj.frequency
                    unnormalized_obj.no_of_matches = unnormalized_obj.no_of_matches + 1
                    match.status = 1

                    norm_obj.save()
                    match.save()
                    unnormalized_obj.save()

                normalized_obj.save()
                match_obj.save()


            elif m_val == 2:
                
                models.InstituteAlias.objects.create(
                    normalized_institute = normalized_obj,
                    ins_alias = unnormalized_obj.name)

                normalized_obj.no_of_aliases = normalized_obj.no_of_aliases + 1
                normalized_obj.no_of_approved_matches = normalized_obj.no_of_approved_matches - 1
                normalized_obj.save()            

                InstituteMatches.objects.filter(unnormalized_inst_id = match_obj.unnormalized_inst.pk).delete()
                UnnormalizedInstitute.objects.filter(id = match_obj.unnormalized_inst.pk).delete() 

        return HttpResponse(
             json.dumps({'status': 'True'})
        )

    else:
        
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"})
        )


def addnew_inst_form_submit(request):
    if request.method == 'POST':

        content = request.POST
        print content

        institute_type = InstituteType.objects.get(name = content['inst_type'])

        models.NormalizedInstitute.objects.create(
                name = content['inst_name'],
                city = content['city'],
                state = content['state'],
                country = content['country'],
                established = content['est'],
                type_of_institute = institute_type,
                misc = content['extra_info'])

        return HttpResponse(
             json.dumps({'status': 'True'})
        )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"})
        )


def addnew_alias_form_submit(request):
    if request.method == 'POST':

        content = request.POST
        print content

        norm_obj = NormalizedInstitute.objects.get(id=content['inst_id'])
        print norm_obj

        models.InstituteAlias.objects.create(
                normalized_institute = norm_obj,
                ins_alias = content['alias-name'])

        return HttpResponse(
             json.dumps({'status': 'True'})
        )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"})
        )
