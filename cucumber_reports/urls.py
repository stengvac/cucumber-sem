from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    #Reports
    url(r'reports/overview', views.ReportsOverView.as_view(), name='reports_overview'),
    url(r'reports/build/(?P<name>[\w]+)/(?P<number>[\w]+)/$', views.BuildDetailView.as_view(), name='reports_build_detail'),
    url(r'reports/feature/(?P<build_name>[\w-]+)/(?P<build_number>[\w-]+)/(?P<feature>[\w|\W]+)/$',
        views.FeatureReportView.as_view(), name='reports_feature_detail'),

    #Statistics
    url(r'statistics/img/temp.png$', views.render_img, name='img'),
    url(r'statistics/build/(?P<name>[\w]+)/(?P<number>[\w]+)/$', views.BuildRunStatisticsView.as_view(), name='statistics_build'),
    url(r'statistics/overall/(?P<name>[\w]+)$', views.StatisticBuildOverTimeView.as_view(), name='statistics_overall'),
    url(r'statistics/overview$', views.StatisticsBuildOverviewView.as_view(), name='statistics_overview'),
]