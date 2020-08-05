from django.urls import include, path
#from rest_framework import routers
from . import views
#from .views import ReminderAPIView, reminder_list

#router = routers.DefaultRouter()
#router.register(r'reminders', views.ReminderViewSet)
#router.register(r'reminders', ReminderAPIView.as_view())

urlpatterns = [
    #path('reminders/',reminder_list),
    #path('', views.home, name='home'),
    #path('', include(router.urls)),
    #path('reminders/', ReminderAPIView.as_view()),
    #path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    path('get-response/', views.get_response, name='get-response'),
    #path('get-reminder/', views.push_response, name='get-reminder'),
]