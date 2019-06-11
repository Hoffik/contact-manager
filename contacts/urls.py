from django.urls import path, include
from rest_framework import routers, serializers, viewsets, schemas
from rest_framework_swagger import renderers
# from rest_framework_swagger.views import get_swagger_view
from .models import Contact, Skill

#serializer.py
class ContactSerializer(serializers.HyperlinkedModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ('id', 'firstname', 'lastname', 'fullname', 'email',)

    def get_fullname(self, obj):
        return obj.firstname + " " + obj.lastname

class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', 'level',)

#view.py
class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view or edit contacts.

    retrieve:
        Return a contact instance.

    list:
        Return all contacts, ordered by most recently joined.

    create:
        Create a new contact.

    delete:
        Remove an existing contact.

    partial_update:
        Update one or more fields on an existing contact.

    update:
        Update a contact.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class SkillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view or edit skills.

    retrieve:
        Return a skill instance.

    list:
        Return all skills, ordered by most recently joined.

    create:
        Create a new skill.

    delete:
        Remove an existing skill.

    partial_update:
        Update one or more fields on an existing skill.

    update:
        Update a skill.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

#view.py

app_name = 'contacts'

router = routers.DefaultRouter()
router.register('contacts', ContactViewSet)
router.register('skills', SkillViewSet)

# schema_view = get_swagger_view(title='Pastebin API')
schema_view = schemas.get_schema_view(title='API schema', renderer_classes=[renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])

urlpatterns = [
    # path('api_schema/', schema_view, name='swagger-schema'),
    path('', schema_view, name="docs"),
    path('api/', include(router.urls)),
]