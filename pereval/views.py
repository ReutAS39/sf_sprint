from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from pereval.models import PerevalAdded
from pereval.serializers import PerevalSerializer


class SubmitData(
                mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet,
                mixins.UpdateModelMixin,
                mixins.ListModelMixin
                ):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalSerializer
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        email = self.request.query_params.get('user__email', None)
        pk = self.kwargs.get('pk')
        if email:
            return self.queryset.filter(user__email=email)
        elif pk:
            return self.queryset.filter(id=pk)
        return self.queryset.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):

        submit_data = self.get_object()

        if submit_data.status != 'new':
            return Response({'state': 0, 'message': 'Данные не могут быть отредактированы'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(submit_data, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'state': 1, 'message': 'Данные успешно отредактированы', "Перевал": serializer.data},
                        status=status.HTTP_204_NO_CONTENT)
