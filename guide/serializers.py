from rest_framework import serializers

from .models import Guide, GuideItem, GuideVersion


class GuideVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideVersion


class GuideVersionTitleSerializer(GuideVersionSerializer):
    class Meta(GuideVersionSerializer.Meta):
        fields = ['id', 'title', 'date_created']


class ListGuideSerializer(serializers.ModelSerializer):
    versions = serializers.SerializerMethodField('get_version')

    @staticmethod
    def get_version(obj):
        versions = obj.guide_version.filter(date_created__gte=obj.filter_date)
        return GuideVersionTitleSerializer(instance=versions, many=True).data

    class Meta:
        model = Guide
        fields = ['id', 'name', 'short_name', 'versions']
