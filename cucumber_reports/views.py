from django.shortcuts import get_object_or_404, render
from django import template
from django.views import generic
from . import dao
from django_pandas.io import read_frame

register = template.Library()


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class ReportsOverView(generic.ListView):
    """Represent view for reports overview"""
    template_name = 'reports/overview.html'
    queryset = dao.find_n_build_runs(5)
    context_object_name = 'latest_builds'

    def get_queryset(self):
        """Build detail obtained from build name and number"""
        return self.queryset


class BuildDetailView(generic.TemplateView):
    """Represent view for build detail"""
    template_name = 'reports/build_detail.html'
    name = None
    number = None

    def get_context_data(self, **kwargs):
        context = super(BuildDetailView, self).get_context_data(**kwargs)
        context['build'] = self.get_queryset()

        return context

    def get_queryset(self):
        print(self.name)
        return dao.find_build_run(self.name, self.number)

    def dispatch(self, request, *args, **kwargs):
        self.name = kwargs.get('name')
        self.number = kwargs.get('number')
        print(self.number)

        return super(BuildDetailView, self).dispatch(request, args, kwargs)


class FeatureReportView(generic.DetailView):
    """Represent view for feature report"""
    template_name = 'reports/feature_detail.html'
    context_object_name = 'feature'
    build_name = None
    build_number = None
    feature_name = None

    def get_queryset(self):
        """Retrieve feature report from build and its name"""
        return dao.find_feature(self.build_name, self.build_number, self.feature_name)


class BuildOverTimeStatistics(generic.DetailView):
    template_name = 'statistics/build_over_time.html'
    context_object_name = 'builds'
    build_name = None

    def get_context_data(self, **kwargs):
        context = super(BuildOverTimeStatistics, self).get_context_data(**kwargs)
        builds = dao.development_over_time(self.build_name)
        df = read_frame(builds)

        context['features'] = df

        return context


@register.filter
def iterate(col, ind):
    return col[int(ind)]
