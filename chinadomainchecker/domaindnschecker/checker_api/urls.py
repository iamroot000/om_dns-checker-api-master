from django.conf.urls import url
from . import views
from django.views import View

urlpatterns = [
	url(r'^$',views.checkerAPI.as_view(), name='show_info'),
	url(r'^access/$',views.AccessibleAPI.as_view(), name='access_status'),
]
