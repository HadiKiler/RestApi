from django.forms.models import model_to_dict
from person.models import Person
from person.serializer import PersonSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


# this is home
@api_view(['GET'])
def api_home(request, *args, **kwargs):
    obj = Person.objects.all().order_by("?").first()
    data = {}
    if obj:
        # data['name'] = obj.name
        # data['gender'] = obj.gender
        # data['context'] = obj.context
        data = PersonSerializer(obj, many=False).data
        return Response(data)



def me():
    pass
