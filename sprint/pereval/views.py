from rest_framework import viewsets, mixins
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from pereval.models import PerevalAdded
from pereval.serializers import PerevalSerializer


class SubmitData(mixins.CreateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)