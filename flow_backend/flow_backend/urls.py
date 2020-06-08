"""flow_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import app.apis as apis
from app import api_user
from app.views import *

router = routers.DefaultRouter()
router.register(r'graph', GraphViewSet)
router.register(r'node_template', NodeTemplateViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('user/token/', obtain_jwt_token, name='token_obtain_pair'),
    path('user/token/refresh/', refresh_jwt_token, name='token_refresh'),
    path('user/register', api_user.create),
    path('user/login', api_user.CustomAuthToken.as_view()),
    path('admin/', admin.site.urls),
    path('is_preview_valid', apis.is_preview_valid),
    path('preview_csv', apis.preview_csv),
    path('preview_echarts', apis.preview_echarts),
    path('upload_json', apis.handle_output),
    path('upload_file', UploadFileView.as_view()),
    path('script_manage', ScriptView.as_view()),
    path('create_node', apis.create_node),
    path('project_file_list', apis.project_file_list),
    path('is_filename_valid', apis.is_filename_valid),
    path('run_node', apis.run_node),
    path('run_project', apis.run_project)
]
