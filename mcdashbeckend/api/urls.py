from django.urls import path
from django.urls.resolvers import URLPattern
from .views import registerNewUser, listUpcomingShifts
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register', registerNewUser, name='registerNewUser'),
    path('list-upcoming-shifts', listUpcomingShifts, name='listUpcomingShifts'),
    path('api-token-auth', obtain_auth_token),

]