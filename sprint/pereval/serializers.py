from rest_framework import serializers

from pereval.models import PerevalAdded, Coords, Level, Users, Images, PerevaladdedImages


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        verbose_name = 'Координаты'
        exclude = ('id',)


class LevelSerialize(serializers.ModelSerializer):
    class Meta:
        model = Level
        exclude = ('id',)


class ImagesSerializer(serializers.ModelSerializer):
    data = serializers.URLField()

    class Meta:
        model = Images
        fields = ('data', 'title')
        verbose_name = 'Изображение'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('email', 'phone', 'fam', 'name', 'otc',)
        verbose_name = 'Пользователь'


class PerevalSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    coords = CoordsSerializer()
    level = LevelSerialize()
    images = ImagesSerializer(many=True)

    class Meta:
        model = PerevalAdded
        exclude = ('id', 'status')

    def create(self, validated_data):
        users_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        image_data = validated_data.pop('images')
        levels_data = validated_data.pop('level')
        user = Users.objects.create(**users_data)
        coords = Coords.objects.create(**coords_data)
        level = Level.objects.create(**levels_data)
        pereval = PerevalAdded.objects.create(user=user, coords=coords, level=level, **validated_data)
        for img in image_data:
            image = Images.objects.create(**img)
            PerevaladdedImages.objects.create(images=image, perevaladded=pereval)
        return pereval
