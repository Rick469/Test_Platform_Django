"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from sign import views, test_tools
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin', admin.site.urls),
    url(r'^api/list/filter', views.api_list_filter),
    url(r'^api/list/', views.api_list),
    url(r'^api/add/save/', views.api_add_save),
    url(r'^api/add$', views.api_add),
    url(r'^api/edit/', views.api_edit),
    url(r'^api_detail/', views.api_detail),
    url(r'^run_test/', views.run_test),
    url(r'^case/list/filter/', views.case_list_filter),
    url(r'^case/list/', views.case_list),
    url(r'^case/add/save/', views.case_add_save),
    url(r'^case/add/', views.case_add),
    url(r'^case/edit/', views.case_edit),
    url(r'^schedule/add/', views.schedule_add),
    url(r'^schedule/list/filter/', views.schedule_list_filter),
    url(r'^schedule/list/', views.schedule_list),
    url(r'^schedule/delete/', views.schedule_delete),
    url(r'^schedule/run/', views.schedule_run),
    url(r'^dependency/list/filter/', views.deependency_list_filter),
    url(r'^dependency/list/', views.deependency_list),
    url(r'^api/report/', views.api_report),
    url(r'^test_tools/', views.test_tools),
    url(r'^tools_button/', views.tools_button),
]
