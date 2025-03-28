from django.contrib import admin
from pereval.models import *


class PerevalAdmin(admin.ModelAdmin):
    list_display = ('id', 'beauty_title', 'title', 'other_titles', 'add_time', 'user', 'coords', 'difficulty', 'connect', 'status')


class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'data', 'date_added')


class CoordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'height')


class DifficultyAdmin(admin.ModelAdmin):
    list_display = ('id', 'mark')


class PerevalAddedimagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'perevaladded', 'images', 'images_id')


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'fam', 'name', 'otc', 'phone')


admin.site.register(PerevalAdded, PerevalAdmin)
admin.site.register(Coords, CoordsAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Difficulty, DifficultyAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(PerevaladdedImages, PerevalAddedimagesAdmin)
