from django.contrib import admin
from core.models import Category, Creator, Card

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
   list_display = ('name', 'slug')

@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
   list_display = ('name', 'slug')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
   list_display = ('question', 'answer', 'creator', 'date_added', 'display_category', 'display_correctly_answered_by')

