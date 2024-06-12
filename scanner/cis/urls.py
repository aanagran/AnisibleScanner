from cis.views import HostConfigAPIView , HostAuditRedemAPIView , HostConnectionCheck
from django.urls import path

urlpatterns = [
    path('hostconfig/',HostConfigAPIView.as_view(),name='host-config'),
    path('hostconfig/operation/',HostAuditRedemAPIView.as_view(),name='host-config'),
    path('checkconnection/',HostConnectionCheck.as_view(),name='check-connection'),
]
