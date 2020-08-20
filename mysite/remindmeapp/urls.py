from django.urls import include, path
from . import views

urlpatterns = [
    path('get-response/', views.get_response, name='get-response'),
    path('logging/', views.logging, name='logging'),
]