from rest_framework import serializers

from .models import Guide, GuideItem, GuideVersion


class GuideVersionSerializer(serializers.ModelSerializer):
    """
    Сериализатор версий справочника
    """
    class Meta:
        model = GuideVersion
        fields = ['id', 'title', 'date_created']


class ListGuideSerializer(serializers.ModelSerializer):
    """
    Сериализатор списка справочников
    """
    versions = serializers.SerializerMethodField('get_version')

    @staticmethod
    def get_version(obj):
        # Проверкак наличия аттрибуиа filter_date
        if hasattr(obj, 'filter_date'):
            # Фильтрация версий справочника
            versions = obj.guide_version.filter(date_created__gte=obj.filter_date)
        else:
            versions = obj.guide_version.all()
        return GuideVersionSerializer(instance=versions, many=True).data

    class Meta:
        model = Guide
        fields = ['id', 'name', 'short_name', 'description', 'versions']


class ListGuideItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор списка элементов справочника
    """
    class Meta:
        model = GuideItem
        fields = ['code_item', 'value_item']
