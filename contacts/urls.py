from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework import routers, schemas
from rest_framework_swagger import renderers
from .views import ContactViewSet, SkillViewSet
from .views import ContactListView, ContactDetailView, ContactFormView
from . import views

app_name = 'contacts'

# Apps views
apps_urls = [
    path('contacts/', ContactListView.as_view(), name='contact-list-view'),
    path('contacts/add/', ContactFormView.as_view(), name='contact-add-view'),
    path('contacts/<int:contact_id>/', ContactDetailView.as_view(), name='contact-detail-view'),
]

# Authentication views
auth_urls = [
    path('signup/', views.signup, name='signup'), #views.SignUp.as_view()
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),
]

# Rest API views
router = routers.DefaultRouter()
router.register('contacts', ContactViewSet, base_name='contacts')
router.register('skills', SkillViewSet, base_name='skills')

# Swagger API documentation
schema_view = schemas.get_schema_view(title='API schema', renderer_classes=[renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])

urlpatterns = [
    path('', include(apps_urls)),
    path('accounts/', include(auth_urls)),
    path('api/schema/', schema_view, name="docs"),
    path('api/', include(router.urls)),
]