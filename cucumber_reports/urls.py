from django.conf.urls import url, handler404, handler500
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    #Reports
    url(r'reports/overview', views.ReportsOverView.as_view(), name='reports_overview'),
    url(r'reports/build/(?P<name>[\w|\W]+)/(?P<number>[\w|\W]+)/$', views.BuildDetailReportView.as_view(), name='reports_build_detail'),
    url(r'reports/feature/(?P<build_name>[\w|\W]+)/(?P<build_number>[\w|\W]+)/(?P<feature>[\w|\W]+)/$',
        views.FeatureReportView.as_view(), name='reports_feature_detail'),

    #Statistics
    url(r'statistics/img/steps/(?P<name>[\w|\W]+)/temp.png$', views.render_steps_passed_img, name='steps_development'),
    url(r'statistics/img/features/(?P<name>[\w|\W]+)/temp.png$', views.render_features_passed_img, name='features_development'),
    url(r'statistics/build/(?P<name>[\w|\W]+)/(?P<number>[\w|\W]+)/$', views.BuildRunStatisticsView.as_view(), name='statistics_build'),
    url(r'statistics/overall/(?P<name>[\w|\W]+)$', views.StatisticsBuildOverTimeView.as_view(), name='statistics_overall'),
    url(r'statistics/overview$', views.StatisticsBuildOverviewView.as_view(), name='statistics_overview'),

]

# Errors
handler404 = 'cucumber_reports.views.http_error404'
handler500 = 'cucumber_reports.views.http_error500'