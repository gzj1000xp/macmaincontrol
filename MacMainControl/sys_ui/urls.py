from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('list/', list),
    path('cat/<int:script_id>/', get_content, name='get script content'),
    path('execute/<int:script_id>/', execute_script, name='execute script'),
]