from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'overview', views.ReportsOverView.as_view(), name='reports_overview'),
    url(r'build/(?P<name>[\w]+)/(?P<number>[\w]+)/$', views.BuildDetailView.as_view(), name='reports_build_detail'),
    url(r'feature/(?P<build_name>[\w-]+)/(?P<build_number>[\w-]+)/(?P<feature>[\w|\W]+)/$',
        views.FeatureReportView.as_view(), name='reports_feature_detail')
]