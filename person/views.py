from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from person.models import Person, Profile
from person.serializer import PersonSerializer
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters



def show(request):
    query = Profile.objects.prefetch_related('person').all()
    return render(request, 'main.html', {'name': 'Mosh', 'query': query})


@api_view(['GET', 'POST', "PUT", "DELETE"])
def person_alt_view(request, pk=None, *args, **kwargs):
    method = request.method  # کد دستی

    if method == "GET":
        if pk is not None:
            # detail view
            obj = get_object_or_404(Person, pk=pk)
            data = PersonSerializer(obj, many=False).data
            return Response(data)
        # list view
        queryset = Person.objects.all()
        data = PersonSerializer(queryset, many=True).data
        return Response(data)

    elif method == "POST":
        # create an item
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data.get('name')
            context = serializer.validated_data.get('context') or None
            if context is None:
                context = "no context"
            serializer.save(context=context)
            return Response(serializer.data)
        return Response({"invalid": "not good data"}, status=400)

    elif method == "PUT":
        if pk is not None:
            obj = get_object_or_404(Person, pk=pk)
            serializer = PersonSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                obj.name = serializer.validated_data.get('name')
                obj.gender = serializer.validated_data.get('gender')
                obj.context = serializer.validated_data.get('context')
                data = serializer.data
                return Response(data)
        return Response({"invalid": "pk not find."}, status=400)

    elif method == "DELETE":
        if pk is not None:
            obj = get_object_or_404(Person, pk=pk).delete()
            return Response(obj, status=400)
        return Response({"invalid": "pk not find."}, status=400)


# ============================================================================
from rest_framework import generics


# ============================== this is for django_filter method-2
class PersonFilter(filters.FilterSet):
    class Meta:
        model = Person
        fields = {
            'name': ['exact'],
            'number': ['exact'],
            'context': ['exact'],
        }
# ============================== this is for django_filter method-2


class PersonSearch(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    # ============================== this is for django_filter method-2 این همون متد یک هست فقط به عنوان کلاس ساخته شده وقابلیت شخصی سازی بیشتری داره
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PersonFilter
    # ============================== this is for django_filter method-2

    # ============================== this is for django_filter method-1 میتونی به ازای هر فیلد یک پارامتر داخل یو ار ال برایش پرکنی و هر پارامتر مربوط به فیلد خودشه
    # filter_backends = [filters.DjangoFilterBackend] #  http://localhost:8000/api/person/search/?number=1234
    # filterset_fields = ['name', 'number', 'gender', 'context']
    # ============================== this is for django_filter method-1

    # ****************************** this is for rest_framework به این صورت کار میکنه که ی چیزی به پارامتر سرچ تو یو ار ال میدی و توی تمام فیلد ها دنبالش میگرده
    # filter_backends = [rest_filters.SearchFilter] # http://localhost:8000/api/person/search/?search=1234
    # search_fields = ('number',)
    # ****************************** this is for rest_framework


class PersonDetailsView(generics.RetrieveAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonListCreateView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


# ============================================================================
from rest_framework import generics, mixins


class PersonMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView):

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):  # HTTP -> get
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     # serializer.save(user=self.request.user)
    #     title = serializer.validated_data.get('title')
    #     content = serializer.validated_data.get('content') or None
    #     if content is None:
    #         content = "this is a single view doing cool stuff"
    #     serializer.save(content=content)
# ============================================================================
