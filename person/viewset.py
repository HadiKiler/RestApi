from rest_framework import viewsets
from .models import Person
from .serializer import PersonSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class PersonViewSet(viewsets.ModelViewSet):
    '''
    get -> list -> Queryset
    get -> retrieve -> Product Instance Detail View
    post -> create -> New Instance
    put -> Update
    patch -> Partial Update
    delete -> destroy
    '''
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        obj = get_object_or_404(Person, pk=pk)
        data = PersonSerializer(obj, many=False).data
        return Response(data)
