from django.contrib import admin

# Register your models here.

from .models import MainMenu
from .models import Book

# register with the admin interface
admin.site.register(MainMenu)
admin.site.register(Book)



