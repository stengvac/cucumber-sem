from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect

from django.views import generic
from . import dao

class IndexView(generic.TemplateView):
    template_name = 'index.html'


class ReportsOverView(generic.ListView):
    template_name = 'reports/overview'
    context_object_name = 'latest_builds'

    def get_queryset(self):
        """
        For each project (specified by its name) show last n build runs and its results
        """
        return dao.find_n_build_runs(5)
