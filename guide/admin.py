from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Guide, GuideItem, GuideVersion


class GuideVersionTabularInline(admin.TabularInline):
    model = GuideVersion
    fields = ['title', 'date_created', 'add_button']
    readonly_fields = ('add_button',)
    extra = 0

    def add_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Добавить</a>',
            reverse('admin:guide_guideversion_change', args=[obj.pk])
        )

    def get_formset(self, request, obj=None, **kwargs):
        labels = {'add_button': 'Добавить элементы'}
        kwargs.update({'labels': labels})
        return super().get_formset(request, obj, **kwargs)


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'short_name']
    inlines = [GuideVersionTabularInline]


@admin.register(GuideItem)
class GuideItemAdmin(admin.ModelAdmin):
    pass


class GuideItemTabularInline(admin.TabularInline):
    model = GuideItem
    fields = ['code_item', 'value_item']
    extra = 0


@admin.register(GuideVersion)
class GuideVersionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    inlines = [GuideItemTabularInline]
