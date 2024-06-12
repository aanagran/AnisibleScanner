from django.contrib import admin
from django.urls import path,include
from scanner.views import ProbeCheck
from users.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('probe/',ProbeCheck.as_view()),
    path('login/',LoginView.as_view()),
    path('users/',include('users.urls')),
    path('cis/',include('cis.urls')),
]
