from django.shortcuts import render, render_to_response
from django.views import generic
from . import dao
from . import view_models
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from django.template import RequestContext
import numpy

class IndexView(generic.TemplateView):
    """Index view render only static template."""
    template_name = 'index.html'


class ReportsOverView(generic.ListView):
    """
    Back end of reports section welcome page.

    template_name - template used to render output
    queryset - field with models objects
    context_object_name - name of context object in template
    """
    template_name = 'reports/overview.html'
    queryset = dao.find_n_build_runs(5)
    context_object_name = 'latest_builds'

    def get_queryset(self):
        """Build detail obtained from build name and number"""
        return self.queryset


class BuildDetailReportView(generic.TemplateView):
    """
    Represent view for build detail report.

    template_name - template used to render output
    queryset - field with models objects
    context_object_name - name of context object in template
    name - name of build run/project
    number - sequential number of build execution
    """
    template_name = 'reports/build_detail.html'
    context_object_name = 'build'
    name = None
    number = None

    def get_context_data(self, **kwargs):
        """Create context with defined object name for template rendering"""
        context = super(BuildDetailReportView, self).get_context_data(**kwargs)
        context[self.context_object_name] = self.get_queryset()

        return context

    def get_queryset(self):
        """Obtain query set for given args."""
        return dao.find_build_run(self.name, self.number)

    def dispatch(self, request, *args, **kwargs):
        """From provided args obtain url parameters and set them info name and number fields"""
        self.name = kwargs.get('name')
        self.number = kwargs.get('number')

        return super(BuildDetailReportView, self).dispatch(request, args, kwargs)


class FeatureReportView(generic.TemplateView):
    """
    Feature report backing view.

    template_name - template used to render output
    queryset - field with models objects
    context_object_name - name of context object in template
    build_name - name of build run/project which contains requested feature
    build_number - sequential number of build execution
    feature_name - name of feature within specified build
    """
    template_name = 'reports/feature_report.html'
    context_object_name = 'feature'
    build_name = None
    build_number = None
    feature_name = None

    def get_queryset(self):
        """Retrieve feature report from build and its name"""
        return dao.find_feature(self.build_name, self.build_number, self.feature_name)

    def get_context_data(self, **kwargs):
        """Create context with context object"""
        context = super(FeatureReportView, self).get_context_data(**kwargs)
        context[self.context_object_name] = self.get_queryset()

        return context

    def dispatch(self, request, *args, **kwargs):
        """From provided args obtain url parameters and set them info build_name, build_number and feature and fields"""
        self.build_name = kwargs.get('build_name')
        self.build_number = kwargs.get('build_number')
        self.feature_name = kwargs.get('feature')

        return super(FeatureReportView, self).dispatch(request, args, kwargs)


class StatisticsBuildOverTimeView(generic.TemplateView):
    """
    Backend for project builds in time development.

    template_name - template used to render output
    name - name of build run/project
    context_object_name - name of object with data inside template
    """
    template_name = 'statistics/build_over_time.html'
    name = None
    context_object_name = 'build_name'

    def get_context_data(self, **kwargs):
        """Obtain context from args and add data object to context with context_objects_name as its name."""
        context = super(StatisticsBuildOverTimeView, self).get_context_data(**kwargs)
        context[self.context_object_name] = self.name

        return context

    def dispatch(self, request, *args, **kwargs):
        """From provided args obtain url parameters and set them into name field"""
        self.name = kwargs.get('name')

        return super(StatisticsBuildOverTimeView, self).dispatch(request, args, kwargs)


class BuildRunStatisticsView(generic.TemplateView):
    """
    Backend for build execution statistics.

    template_name - template used to render output
    name - name of build run/project
    number - sequential number of build execution
    context_object_name - name of object with data inside template
    """
    template_name = 'statistics/build_statistics.html'
    name = None
    number = None
    context_object_name = 'build'

    def get_context_data(self, **kwargs):
        """Obtain context from args and add data object to context with context_objects_name as its name."""
        context = super(BuildRunStatisticsView, self).get_context_data(**kwargs)
        context[self.context_object_name] = self.get_queryset()

        return context

    def get_queryset(self):
        """Obtain query set to present."""
        return dao.build_run_statistics(self.name, self.number)

    def dispatch(self, request, *args, **kwargs):
        """From provided args obtain url parameters and set them into name and number fields"""
        self.name = kwargs.get('name')
        self.number = kwargs.get('number')

        return super(BuildRunStatisticsView, self).dispatch(request, args, kwargs)


class StatisticsBuildOverviewView(generic.ListView):
    """
      Backend for build execution statistics.

      template_name - template used to render output
       context_object_name - name of object with data inside template
      """
    template_name = 'statistics/overview_allbuild.html'
    queryset = dao.find_n_build_runs(5)
    context_object_name = 'builds'

    def get_queryset(self):
        return self.queryset


def create_bar(runs, executions_passed, executions_total, ylabel, legend):
    build_numbers = []
    for run in runs:
        build_numbers.append(run.metadata.number)
    build_numbers = numpy.array(build_numbers)

    fig = Figure()
    canvas = FigureCanvas(fig)
    width = 0.2
    ax = fig.add_subplot(111)
    passed = ax.bar(build_numbers, executions_passed, width, color='green')
    all = ax.bar(build_numbers + width, executions_total, width, color='grey')
    ax.set_ylabel(ylabel)
    ax.set_xlabel( 'Build numbers')
    ax.set_xticks(build_numbers + width / 2)
    ax.set_xticklabels(build_numbers)
    ax.legend((passed[0], all[0]), legend)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)

    return response


def render_steps_passed_img(request, name):
    """
    For given project name retrieve all its build runs and create graph with steps passed over all these runs.

    :param request to process
    :param name of build to create statistics from
    :return https response with image of obtained data
    """
    runs = dao.development_over_time(name)
    steps_passed = []
    steps = []

    for run in runs:
        steps_passed.append(run.steps_passed)
        steps.append(run.step_runs)

    return create_bar(runs, steps_passed, steps,'Step count', ('Passed steps', 'All steps'))


def render_features_passed_img(request, name):
    """
    For given project name retrieve all its build runs and create graph with featres passed over all these runs.

    :param request to process
    :param name of build to create statistics from
    :return https response with image of obtained data
    """
    runs = dao.development_over_time(name)
    features_passed = []
    features = []

    for run in runs:
        features_passed.append(run.features_passed)
        features.append(run.features_runs)

    return create_bar(runs, features_passed, features, 'Features count', ('Passed features', 'All features'))


def http_error404(request):
    """
    Handle 404 status code.

    :param request to process
    """
    return handle_error(request, 'errors/http404.html', 404)


def http_error500(request):
    """
    Handle 500 status code.

    :param request to process
    """
    return handle_error(request, 'errors/http500.html', 500)


def handle_error(request, template_path, status_code):
    """
    Handle http error.

    :param request - to process
    :param template_path - path to template
    :param status_code - for response
    """
    response = render_to_response(template_path, context_instance=RequestContext(request))
    response.status_code = status_code

    return response
