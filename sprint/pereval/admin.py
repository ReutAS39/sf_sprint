from django.contrib import admin
from pereval.models import *


class PerevalAdmin(admin.ModelAdmin):
    list_display = ('id', 'beauty_title', 'title', 'other_titles', 'add_time', 'user', 'coords', 'level', 'connect', 'status')


class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'data', 'date_added')


class CoordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'height')


class LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'winter', 'summer', 'autumn', 'spring')


class PerevalAddedimagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'perevaladded', 'images', 'images_id')


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'fam', 'name', 'otc', 'phone')


admin.site.register(PerevalAdded, PerevalAdmin)
admin.site.register(Coords, CoordsAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(PerevaladdedImages, PerevalAddedimagesAdmin)
