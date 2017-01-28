from django.shortcuts import get_object_or_404, render
from django.views import generic
from . import dao
from django_pandas.io import read_frame
from . import view_models
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


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
    template_name = 'reports/feature_detail.html'
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


def render_steps_passed_img(request, name):
    """For given project name retrieve all its build runs and create graph with steps passed over all these runs."""
    runs = dao.development_over_time(name)
    numbers = []
    steps_passed = []
    for run in runs:
        numbers.append(run.metadata.number)
        steps_passed.append(run.steps_passed)

    fig = Figure()
    canvas = FigureCanvas(fig)

    ax = fig.add_subplot(111)
    fig.gca().set_color_cycle(['green', 'red', 'grey'])
    ax.plot(numbers, steps_passed)

    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
