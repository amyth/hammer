from django.views.generic.base import TemplateView

from apps.generic.views import LoginRequiredMixin


class Index(TemplateView):
    """
    Renders the index view template
    """

    template_name = 'overseer/index.html'
