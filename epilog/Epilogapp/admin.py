from django.contrib import admin
from .models import Product, Ingredient, Concern, Favorite, Message, SkinType
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('カスタム項目', {'fields': ('nickname', 'is_advisor')}),
    )

admin.site.register(Product)
admin.site.register(Ingredient)
admin.site.register(Concern)
admin.site.register(SkinType)
admin.site.register(Favorite) 
admin.site.register(Message)
admin.site.register(CustomUser, CustomUserAdmin)
# Register your models here.
