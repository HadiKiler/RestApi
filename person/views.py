from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from person.models import Person
from person.serializer import PersonSerializer
from rest_framework.decorators import api_view


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
