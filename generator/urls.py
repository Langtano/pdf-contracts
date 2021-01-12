from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url
from . import views

router = DefaultRouter()
router.trailing_slash = '/?'
router.register(r'generate_pdf', views.GeneratePdfViewSet, basename='generate_pdf')
app_name = 'generator'

urlpatterns = [
    url(r'', include(router.urls))
]
