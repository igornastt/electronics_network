from django.db import transaction, IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from products.models import Product
from products.serializers import ProductSmallSerializer, ProductCreateSerializer
from factory.models import Factory
from contacts.models import Contact
from contacts.serializers import ContactSerializer
from networks_electronics.serializers.main_network_serializers import MainNetworkBaseSerializer


class FactorySerializer(serializers.ModelSerializer):
    """
    Основной сериализатор с информацией о связанных объектах (main_network, contact, products).
    """
    main_network = MainNetworkBaseSerializer(read_only=True)
    contact = ContactSerializer(read_only=True)
    products = ProductSmallSerializer(many=True, read_only=True)

    class Meta:
        model = Factory
        fields = ('id', 'main_network', 'name', 'contact', 'products', 'created_at', 'is_active')


class FactoryCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания объектов модели Factory.

    transaction.atomic() используется для предотвращения каких-либо воздействий на базу данных,
    если только все действия в переопределенном методе create() не будут выполнены успешно.
    """
    contact = ContactSerializer(many=False, required=True)
    new_products = ProductCreateSerializer(many=True, required=False)
    product_ids_to_add = serializers.ListField(required=False)

    class Meta:
        model = Factory
        fields = ('id', 'name', 'main_network', 'contact', 'new_products', 'product_ids_to_add',)

    def create(self, validated_data):
        with transaction.atomic():
            contacts_data = validated_data.pop('contact')
            new_products_data = validated_data.pop('new_products', [])
            prod_ids_list = validated_data.pop('product_ids_to_add', [])

            contacts = Contact.objects.create(**contacts_data)
            contacts.save()
            factory = Factory.objects.create(**validated_data, contact=contacts)

            for product in new_products_data:
                factory.products.create(**product)

            for product_id in prod_ids_list:
                try:
                    prod_to_add = get_object_or_404(Product, pk=product_id)
                    factory.products.add(prod_to_add)
                except Http404:
                    raise ValidationError(f'Продукт с id "{product_id}" не найден')

            return factory


class FactoryUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления объектов модели Factory.

    transaction.atomic() используется для предотвращения каких-либо воздействий на базу данных,
    если только все действия в переопределенном методе updated() не будут выполнены успешно.
    """
    name = serializers.CharField(required=False)
    contact_id = serializers.IntegerField(required=False)
    product_ids_to_add = serializers.ListField(child=serializers.IntegerField(), required=False)
    product_ids_to_remove = serializers.ListSerializer(child=serializers.IntegerField(), required=False)

    class Meta:
        model = Factory
        fields = (
            'id', 'name', 'contact_id', 'product_ids_to_add', 'product_ids_to_remove', 'is_active',
        )

    def update(self, factory, validated_data):
        with transaction.atomic():
            contact_data = validated_data.pop('contact_id', None)
            if contact_data:
                try:
                    new_contacts = get_object_or_404(Contact, pk=contact_data)
                    factory.contact_info = new_contacts
                except Http404:
                    raise serializers.ValidationError(f'Контактная информация с id "{contact_data}" не найдена')

            prod_ids_to_add_data = validated_data.pop('product_ids_to_add', [])
            for p_id in prod_ids_to_add_data:
                try:
                    prod_to_add = get_object_or_404(Product, pk=p_id)
                    factory.products.add(prod_to_add)
                except Http404:
                    raise serializers.ValidationError(f'Продукт с id "{p_id}" не найден')

            prod_ids_to_remove_data = validated_data.pop('product_ids_to_remove', [])
            for p_id in prod_ids_to_remove_data:
                try:
                    prod_to_remove = get_object_or_404(Product, pk=p_id)
                    if prod_to_remove not in factory.products.all():
                        raise ValidationError(f"Продукт {p_id} не связан с {factory}")
                    factory.products.remove(prod_to_remove)
                except Http404:
                    raise serializers.ValidationError(f'Продукт с id "{p_id}" не найден')

            for attr, val in validated_data.items():
                setattr(factory, attr, val)

            try:
                factory.save()
            except IntegrityError:
                raise serializers.ValidationError(
                    f'Контакт с id "{contact_data}" уже связан с другим объектом.')
            return factory
