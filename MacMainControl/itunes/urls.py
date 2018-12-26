from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list),
    path('cat/<int:script_id>/', views.get_content, name='get script content'),
    path('execute/<int:script_id>/', views.execute_script, name='execute'),
    path('init_data/', views.insert_script, name='insert'),
    path('execute_dp/<int:script_id>/', views.execute_script_dp),
]