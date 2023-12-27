from rest_framework import viewsets, mixins
from .models import Person
from .serializer import PersonSerializer


class ProductViewSet(viewsets.ModelViewSet):
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
