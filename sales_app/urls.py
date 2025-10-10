from django.urls import path
from . import views

app_name = 'sales_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('save-to-xml/', views.save_to_xml, name='save_to_xml'),
    path('upload-xml/', views.upload_xml, name='upload_xml'),
]