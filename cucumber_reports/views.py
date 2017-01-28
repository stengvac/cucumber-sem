from django.shortcuts import get_object_or_404, render
from django.views import generic
from . import dao
from django_pandas.io import read_frame
from . import view_models
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure




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
    context_object_name = 'build'
    name = None
    number = None
    model = view_models.BuildRunReport

    def get_context_data(self, **kwargs):
        context = super(BuildDetailView, self).get_context_data(**kwargs)
        context['build'] = self.get_queryset()

        return context

    def get_queryset(self):
        return dao.find_build_run(self.name, self.number)

    def dispatch(self, request, *args, **kwargs):
        self.name = kwargs.get('name')
        self.number = kwargs.get('number')

        return super(BuildDetailView, self).dispatch(request, args, kwargs)


class FeatureReportView(generic.TemplateView):
    """Represent view for feature report"""
    template_name = 'reports/feature_detail.html'
    build_name = None
    build_number = None
    feature_name = None

    def get_queryset(self):
        """Retrieve feature report from build and its name"""
        return dao.find_feature(self.build_name, self.build_number, self.feature_name)

    def get_context_data(self, **kwargs):
        context = super(FeatureReportView, self).get_context_data(**kwargs)
        context['feature'] = self.get_queryset()

        return context

    def dispatch(self, request, *args, **kwargs):
        self.build_name = kwargs.get('build_name')
        self.build_number = kwargs.get('build_number')
        self.feature_name = kwargs.get('feature')

        return super(FeatureReportView, self).dispatch(request, args, kwargs)


class BuildOverTimeStatisticsView(generic.TemplateView):
    template_name = 'statistics/build_over_time.html'
    build_name = None

    def get_context_data(self, **kwargs):
        context = super(BuildOverTimeStatisticsView, self).get_context_data(**kwargs)
        builds = self.get_queryset()
        df = read_frame(builds)
        #
        # graphic = cStringIO.StringIO()
        # canvas.print_png(graphic)
        # return render(request, 'graphic.html', {'graphic': graphic})

        context['stat'] = df.plot()

        return context

    def get_queryset(self):
        return dao.development_over_time(self.build_name)

    def dispatch(self, request, *args, **kwargs):
        self.build_name = kwargs.get('name')

        return super(BuildOverTimeStatisticsView, self).dispatch(request, args, kwargs)


class StatisticBuildOverTimeView(generic.TemplateView):
    template_name = 'statistics/build_over_time.html'
    name = None


    def get_context_data(self, **kwargs):
        context = super(StatisticBuildOverTimeView, self).get_context_data(**kwargs)
        context['name'] = self.name

        return context

    def dispatch(self, request, *args, **kwargs):
        self.name = kwargs.get('name')

        return super(StatisticBuildOverTimeView, self).dispatch(request, args, kwargs)



class BuildRunStatisticsView(generic.TemplateView):
    template_name = 'statistics/build_statistics.html'
    name = None
    number = None

    def get_context_data(self, **kwargs):
        context = super(BuildRunStatisticsView, self).get_context_data(**kwargs)
        context['build'] = self.get_queryset()

        return context

    def get_queryset(self):
        return dao.build_run_statistics(self.name, self.number)

    def dispatch(self, request, *args, **kwargs):
        self.name = kwargs.get('name')
        self.number = kwargs.get('number')

        return super(BuildRunStatisticsView, self).dispatch(request, args, kwargs)


class StatisticsBuildOverviewView(generic.ListView):
    template_name = 'statistics/overview_allbuild.html'
    queryset = dao.find_n_build_runs(5)
    context_object_name = 'builds'

    def get_queryset(self):
        return self.queryset


def render_img(request, name):
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
