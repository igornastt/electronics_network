from rest_framework import serializers


class EmailValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_data = value.get(self.field)
        if tmp_data is not None and 'ru' not in tmp_data and 'com' not in tmp_data:
            raise serializers.ValidationError('Почтовый адрес должен ссылаться на почтовый хостинг ".ru" или ".com"')
