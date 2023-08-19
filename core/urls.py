from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users app and its sub-apps
    path('users/', include('app.users.urls')),
    # path('users/doctor/', include('app.users.doctor.urls')),
    # path('users/patient/', include('app.users.patient.urls')),
    # path('users/super_user/', include('app.users.super_user.urls')),

    # # Medical services and their sub-apps
    # path('medical_services/counseling/', include('app.medical_services.counseling.urls')),
    # path('medical_services/group_therapy/', include('app.medical_services.group_therapy.urls')),
    # path('medical_services/knowledge_cafe/', include('app.medical_services.knowledge_cafe.urls')),
    # path('medical_services/nutritionist/', include('app.medical_services.nutritionist.urls')),
    # path('medical_services/social_worker/', include('app.medical_services.social_worker.urls')),
    # path('medical_services/spiritual_therapy_specialist/', include('app.medical_services.spiritual_therapy_specialist.urls')),
    # path('medical_services/sports_physiology_specialist/', include('app.medical_services.sports_physiology_specialist.urls')),

    # Assuming DRF YASG or similar is used for API documentation based on the file structure
    # path('docs/', include('drf_yasg.urls')),
]

