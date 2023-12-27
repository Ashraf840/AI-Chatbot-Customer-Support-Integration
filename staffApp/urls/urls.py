from django.urls import path, include

app_name = "staffApp"

urlpatterns = [
    path("cso-workload/", include(('staffApp.urls.staff_workload.cso_workload_urls', 'app_name'), namespace="CsoWorkload")),
    # TMS API
    path("api/", include(('staffApp.api.api_urls', 'app_name'), namespace="StaffAppAPI")),
]
