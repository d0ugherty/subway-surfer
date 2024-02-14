from django.contrib import admin
from django.urls import path, include
from subway_surfer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('train_info/', views.train_info, name='train_info'),
    path('arrivals/<str:station>/',views.load_arrivals, name='load_arrivals'),
    path('update_arrivals_table/<str:table_id>/', views.update_arrivals_table, name='update_arrivals_table'),
    path('fare_calculator/', views.fare_calculator, name='fare_calculator'),
    path('next_to_arrive/<str:station>/', views.next_to_arrive, name='next_to_arrive'),
    path('update_next_to_arrive/<str:station>/', views.update_next_to_arrive, name ='update_next_to_arrive'),
    path('map/', views.map_page_view, name='render_map'),
    path('api/', include([
        path('map_markers/<str:agency>/', views.map_markers, name='map_markers'),
    ]))
]
