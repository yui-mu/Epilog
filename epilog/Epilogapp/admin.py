from django.contrib import admin
from .models import Product, Ingredient, Concern, Favorite

admin.site.register(Product)
admin.site.register(Ingredient)
admin.site.register(Concern)
admin.site.register(Favorite) 
# Register your models here.
