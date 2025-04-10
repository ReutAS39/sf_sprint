from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pereval.models import PerevalAdded
from pereval.serializers import PerevalSerializer


class PerevalAdd(APIView):
    @extend_schema(
        summary="Добавить перевал",
        description="Добавление перевала",
        request=PerevalSerializer,
        responses={
            200: OpenApiResponse(response=PerevalSerializer, description="Перевал успешно создан"),
            400: OpenApiResponse(description="Ошибки валидации"),
            500: OpenApiResponse(description="Ошибка при выполнении операции")
        }
    )
    def post(self, request):
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            pereval = serializer.save()
            return Response(data={"status": 200, "message": None, 'id':  pereval.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PerevalDetail(APIView):
    @extend_schema(
        summary="Получение информации о перевале",
        description="Возвращает информацию о перевале по его ID.",
        responses={
            200: OpenApiResponse(response=PerevalSerializer, description="Информация о перевале"),
            404: OpenApiResponse(description="Перевал не найден")
        }
    )
    def get(self, request, id):
        try:
            pereval = PerevalAdded.objects.get(id=id)
        except PerevalAdded.DoesNotExist:
            return Response({"error": "Перевал не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PerevalSerializer(pereval)
        return Response(serializer.data)


class PerevalUpdate(APIView):
    @extend_schema(
        summary="Отредактировать запись перевала",
        description="Редакция записи перевала",
        request=PerevalSerializer,
        responses={
            201: OpenApiResponse(response=PerevalSerializer, description="Запись успешно отредактирована"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
    def patch(self, request, id):
        try:
            pereval = PerevalAdded.objects.get(id=id)
        except PerevalAdded.DoesNotExist:
            return Response({"error": "Перевал не найден"}, status=status.HTTP_404_NOT_FOUND)
        if pereval.status != 'new':
            return Response({'state': 0, 'message': f'Данные не могут быть отредактированы. Статус записи -{pereval.status}'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = PerevalSerializer(pereval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'state': 1, 'message': 'Данные успешно отредактированы', "Перевал": serializer.data},
                            status.HTTP_200_OK)
        return Response({'state': 0, 'message': 'Данные не могут быть отредактированы'},
                        status=status.HTTP_400_BAD_REQUEST)


class PerevalList(APIView):
    @extend_schema(
        summary="Получение информации обо всех перевалах",
        description="Возвращает список всех перевалов.",
        responses={
            200: OpenApiResponse(response=PerevalSerializer(many=True), description="Список всех перевалов")
        }
    )
    def get(self, request, email):
        perevals = PerevalAdded.objects.filter(user__email=email)
        serializer = PerevalSerializer(perevals, many=True)
        return Response(serializer.data)
