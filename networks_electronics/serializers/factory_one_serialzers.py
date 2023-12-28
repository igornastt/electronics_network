from rest_framework import serializers

from factory.models import Factory


class FactoryBaseSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора для отображения краткой информации, лишь id и имя.
    """
    class Meta:
        model = Factory
        fields = ('id', 'name',)
