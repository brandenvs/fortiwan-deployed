from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('authentication.urls')),   
    path('fortiwan-dashboard/', include('fortiwan_dashboard.urls')),    
    path('fortiwan-monitor/', include('fortiwan_monitor.urls')),
    path('fortiwan-config/', include('fortiwan_config.urls')),
    path('fortiwan-log/', include('fortiwan_log.urls')),
    path('fortiwan-services/', include('fortiwan_services.urls')),
    path('admin/', admin.site.urls),  
]
