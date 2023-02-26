from django.urls import path
from . import views

urlpatterns = [
    # path('mishal/', views.members, name='members'),
    # path('data/', views.my_view, name='data'),
    # path('ReadXML/', views.ReadXML, name='ReadXML'),
    # path('upload_xml/', views.upload_xml, name='upload_xml'),
    path('', views.pc, name='pc'),
    # path('dropdown_view/', views.dropdown_view, name='dropdown_view'),
]