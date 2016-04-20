from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from apps.generic.views import LoginRequiredMixin
from apps.overseer.forms import UploadJsonDataForm


class Index(TemplateView):
    """
    Renders the index view template
    """

    template_name = 'overseer/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['upload_form'] = UploadJsonDataForm

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

