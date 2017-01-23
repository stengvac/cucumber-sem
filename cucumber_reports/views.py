from django.shortcuts import get_object_or_404, render
from django import template
from django.views import generic
from . import dao

register = template.Library()


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class ReportsOverView(generic.ListView):
    """Represent view for reports overview"""
    template_name = 'reports/overview'
    context_object_name = 'latest_builds'

    def get_queryset(self):
        """For each project (specified by its name) show last n build runs and its results"""
        return dao.find_n_build_runs(5)


class BuildDetailView(generic.DetailView):
    """Represent view for build detail"""
    template_name = 'reports/build_detail'
    context_object_name = 'build'
    name = None
    number = None

    def get_queryset(self):
        """Build detail obtained from build name and number"""
        return dao.find_build_run(self.name, self.number)


class FeatureReportView(generic.DetailView):
    """Represent view for feature report"""
    template_name = 'reports/feature_detail'
    context_object_name = 'feature'
    build_name = None
    build_number = None
    feature_name = None

    def get_queryset(self):
        """Retrieve feature report from build and its name"""
        return dao.find_feature(self.build_name, self.build_number, self.feature_name)


@register.filter
def iterate(col, ind):
    return col[int(ind)]
