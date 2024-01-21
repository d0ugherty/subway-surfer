"""
URL configuration for subway_surfer project.

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
from django.urls import path
from subway_surfer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('arrivals/<str:station>/',views.load_arrivals, name='load_arrivals'),
    path('update_arrivals_table/<str:table_id>/', views.update_arrivals_table, name='update_arrivals_table'),
    path('fare_calculator/', views.fare_calculator, name='fare_calculator'),
    path('next_to_arrive/', views.next_to_arrive, name='next_to_arrive')
    #path('map/', views.render_map, name='map')
]
