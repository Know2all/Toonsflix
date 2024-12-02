from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Cartoon)
admin.site.register(Video)
admin.site.register(Tag)