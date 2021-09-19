from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from django.urls import reverse
from django.utils.html import format_html

from .models import Guide, GuideItem, GuideVersion


class GuideVersionFormSet(BaseInlineFormSet):
    def clean(self):
        for form in self.forms:
            if not form.is_valid():
                return
            # Делаю проверку кол-ва добавленных форм
            if len(self.forms) > 1:
                if form not in self.initial_forms:
                    # Если форма не была ранее создана
                    # Делаю проверку версии, ести ли уже такая версия в справочнике
                    if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                        title = form.cleaned_data.get('title')
                        if title:
                            if GuideVersion.objects.filter(title=title, guide_id=self.instance).exists():
                                raise ValidationError(f'Справочник с версией {title} уже существует')

                        date_created = form.cleaned_data.get('date_created')
                        if date_created:
                            if GuideVersion.objects.filter(date_created=date_created, guide_id=self.instance).exists():
                                raise ValidationError(f'Справочник с такой датой {date_created} уже существует')

                else:
                    # Если форма была ранее создана
                    # Делаю проверку версии, ести ли уже такая версия в справочнике
                    if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                        title = form.cleaned_data.get('title')
                        if title:
                            if title != form.initial.get('title'):
                                if GuideVersion.objects.filter(title=title, guide_id=self.instance).exists():
                                    raise ValidationError(f'Справочник с версией {title} уже существует')

                        date_created = form.cleaned_data.get('date_created')
                        if date_created:
                            if date_created != form.initial.get('date_created'):
                                if GuideVersion.objects.filter(
                                        date_created=date_created, guide_id=self.instance).exists():
                                    raise ValidationError(f'Справочник с такой датой {date_created} уже существует')


class GuideVersionTabularInline(admin.TabularInline):
    model = GuideVersion
    fields = ['title', 'date_created', 'add_button']
    readonly_fields = ('add_button',)
    formset = GuideVersionFormSet
    extra = 0

    @admin.display(description='Добавить элемент')
    def add_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Добавить</a><p class="help">{}</p>',
            reverse('admin:guide_guideversion_change', args=[obj.pk]),
            'Можно только после сохранения формы'
        )


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
