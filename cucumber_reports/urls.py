from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    #Reports
    url(r'reports/overview', views.ReportsOverView.as_view(), name='reports_overview'),
    url(r'reports/build/(?P<name>[\w]+)/(?P<number>[\w]+)/$', views.BuildDetailReportView.as_view(), name='reports_build_detail'),
    url(r'reports/feature/(?P<build_name>[\w-]+)/(?P<build_number>[\w|\W]+)/(?P<feature>[\w|\W]+)/$',
        views.FeatureReportView.as_view(), name='reports_feature_detail'),

    #Statistics
    url(r'statistics/img/(?P<name>[\w|\W]+)/temp.png$', views.render_steps_passed_img, name='img'),
    url(r'statistics/build/(?P<name>[\w|\W]+)/(?P<number>[\w|\W]+)/$', views.BuildRunStatisticsView.as_view(), name='statistics_build'),
    url(r'statistics/overall/(?P<name>[\w|\W]+)$', views.StatisticsBuildOverTimeView.as_view(), name='statistics_overall'),
    url(r'statistics/overview$', views.StatisticsBuildOverviewView.as_view(), name='statistics_overview'),
]