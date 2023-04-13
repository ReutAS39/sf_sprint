from rest_framework import viewsets, mixins


from pereval.models import PerevalAdded
from pereval.serializers import PerevalSerializer


class SubmitData(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalSerializer
