from django.contrib import admin
from .models import STKUnit, STKCategory, STKStock, STKTake

admin.site.register(STKUnit)
admin.site.register(STKCategory)
admin.site.register(STKStock)
admin.site.register(STKTake)
