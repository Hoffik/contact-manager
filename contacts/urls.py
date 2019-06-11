from django.urls import path, include
from rest_framework import routers, schemas
from rest_framework_swagger import renderers
from .views import ContactViewSet, SkillViewSet

app_name = 'contacts'

router = routers.DefaultRouter()
router.register('contacts', ContactViewSet)
router.register('skills', SkillViewSet)

schema_view = schemas.get_schema_view(title='API schema', renderer_classes=[renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])

urlpatterns = [
    path('', schema_view, name="docs"),
    path('api/', include(router.urls)),
]