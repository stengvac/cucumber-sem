from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect

from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class ReportsOverView(generic.ListView):
    template_name = 'reports/overview'

