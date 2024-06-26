"""
URL configuration for webapps2024 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/webapps2024/', permanent=True)),
    path('webapps2024/', include('main.urls')),
    path('webapps2024/register/', include('register.urls')),
    path('webapps2024/payapp/', include('payapp.urls')),
    path('webapps2024/wallet/', include('walletapp.urls')),
    path('webapps2024/notification/', include('notificationapp.urls')),
    path('webapps2024/conversion/', include('conversionapp.urls')),
    path('webapps2024/admin/', include('adminapp.urls')),
    path('django-admin/', admin.site.urls),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)