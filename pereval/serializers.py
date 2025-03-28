from rest_framework import serializers

from pereval.models import PerevalAdded, Coords, Difficulty, Users, Images, PerevaladdedImages


class CoordsSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(min_value=-90.0, max_value=90.0)
    longitude = serializers.FloatField(min_value=-180.0, max_value= 180.0)
    height = serializers.IntegerField(max_value=9000)
    class Meta:
        model = Coords
        verbose_name = 'Координаты'
        exclude = ('id',)


class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        exclude = ('id',)


class ImagesSerializer(serializers.ModelSerializer):
    data = serializers.URLField()

    class Meta:
        model = Images
        fields = ('data', 'title')
        verbose_name = 'Изображение'


class UsersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = Users
        fields = ('email', 'phone', 'fam', 'name', 'otc',)
        verbose_name = 'Пользователь'


class PerevalSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    coords = CoordsSerializer()
    difficulty = DifficultySerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = PerevalAdded
        fields = '__all__'

    def create(self, validated_data):
        users_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        image_data = validated_data.pop('images')
        difficulty_data = validated_data.pop('difficulty')

        if Difficulty.objects.filter(**difficulty_data).exists():
            difficulty = Difficulty.objects.get(**difficulty_data)
        else:
            difficulty = Difficulty.objects.create(**difficulty_data)

        if Coords.objects.filter(**coords_data).exists():
            coords = Coords.objects.get(**coords_data)
        else:
            coords = Coords.objects.create(**coords_data)

        if Users.objects.filter(email=users_data['email']).exists():
            user = Users.objects.get(email=users_data['email'])
        else:
            user = Users.objects.create(**users_data)

        pereval = PerevalAdded.objects.create(user=user, coords=coords, difficulty=difficulty, **validated_data)
        for img in image_data:
            image = Images.objects.create(**img)
            PerevaladdedImages.objects.create(images=image, perevaladded=pereval)
        return pereval

    def update(self, instance, validated_data):

        coords_data = validated_data.pop('coords')
        image_data = validated_data.pop('images')
        difficulty_data = validated_data.pop('difficulty')
        coords = instance.coords
        difficulty = instance.difficulty
        print(coords_data)
        print(coords)
        for img in image_data:
            if Images.objects.filter(data=img['data'], title=img['title']).exists():
                continue
            else:
                image = Images.objects.create(**img)
                PerevaladdedImages.objects.create(images=image, perevaladded=instance)

        coords.latitude = coords_data.get('latitude', coords.latitude)
        coords.longitude = coords_data.get('longitude', coords.longitude)
        coords.height = coords_data.get('height', coords.height)
        coords.save()

        difficulty.winter = difficulty_data.get('winter', difficulty.winter)
        difficulty.summer = difficulty_data.get('summer', difficulty.summer)
        difficulty.audifficultytumn = difficulty_data.get('autumn', difficulty_data.autumn)
        difficulty.spring = difficulty_data.get('spring', difficulty.spring)
        if Difficulty.objects.filter(**difficulty_data).exists():
            instance.difficulty = Difficulty.objects.get(**difficulty_data)
            instance.difficulty.save()
        else:
            instance.difficulty = Difficulty.objects.create(**difficulty_data)
            instance.difficulty.save()

        instance.beauty_title = validated_data.get('beauty_title', instance.beauty_title)
        instance.title = validated_data.get('title', instance.title)
        instance.other_titles = validated_data.get('other_titles', instance.other_titles)
        instance.connect = validated_data.get("connect", instance.connect)
        instance.save()
        return instance
