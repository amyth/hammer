from django.views.generic.base import TemplateView


class Index(TemplateView):
    """
    Renders the index view template
    """

    template_name = 'overseer/index.html'
