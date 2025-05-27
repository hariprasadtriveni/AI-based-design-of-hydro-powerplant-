from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('generate/', views.generate_design, name='generate_design'),
    path('civil/', views.civil_structure, name='civil_structure'),
    path('hydroelectric/', views.hydroelectric_system, name='hydroelectric_system'),
    path('mechanical/', views.mechanical_components, name='mechanical_components'),
]
