from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from apps.generic.views import LoginRequiredMixin
from apps.overseer.forms import UploadJsonDataForm
from apps.overseer.models import Institute


class Index(TemplateView):
    """
    Renders the index view template
    """

    template_name = 'overseer/index.html'
    typemap = {
        'normalized': {'is_normalized': True},
        'unnormalized': {'is_normalized': False},
        'fresh': {}
    }

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['upload_form'] = UploadJsonDataForm

        ## add paginated institute objects to the context
        page_no = self.request.GET.get('page', 1)
        list_type = self.request.GET.get('type', 'normalized')
        institutes = Institute.objects.filter(**self.typemap.get(list_type))

        if list_type == 'fresh':
            institutes = [i for i in institutes if not i.has_match]
        elif list_type == 'unnormalized':
            institutes = [i for i in institutes if i.has_match]

        p = Paginator(institutes, settings.PAGINATION_STEP)
        context['page'] = p.page(page_no)
        context['paginator'] = p
        context['tabtypes'] = self.typemap.keys()

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
