from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'overview', views.ReportsOverView.as_view(), name='reports_overview'),
    url(r'build', views.ReportsOverView.as_view(), name='reports_build_detail'),
    url(r'feature', views.ReportsOverView.as_view(), name='reports_feature_detail')
]