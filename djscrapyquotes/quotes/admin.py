from django.contrib import admin
from .models import Quotes

# admin.site.register(Quotes)


@admin.register(Quotes)
class HeroAdmin(admin.ModelAdmin):
    change_list_template = "change_list.html"
