"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
#This file contains all the url paths for the application, including API paths

#---LIBRARIES----------------------------------------------------------------------------------------------------------------
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', include('project.urls')),   #include all urls in the project/urls.py file aswell
    path('admin/', admin.site.urls),     #include the admin page for the super user to access
    path('api-auth/', include('rest_framework.urls')),   #include a url to authenticate user's via API's
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),    #Generate/authenticate the API cookie
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   #Refresh the API cookie
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    #add/get all files of any type into the media folder