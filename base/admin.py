from django.contrib import admin
from .models import Room, Message, Topic
# Register your models here.


#class RoomAdmin(admin.ModelAdmin):
    #fields = ['name', 'created', 'updated']


admin.site.register(Room, ),
admin.site.register(Message),
admin.site.register(Topic),
