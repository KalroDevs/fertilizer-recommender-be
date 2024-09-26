from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('kfrs_api', views.ApprovalsView)
urlpatterns = [
	# path('form/', views.kfrs_form, name='kfrs_form'),
    # path('api/', include(router.urls)),
    # path('status/', views.approvereject),
    path('', views.fertilizer_recommendation, name='fertilizer_recommendation'),
 
] 
