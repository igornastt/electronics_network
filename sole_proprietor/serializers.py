from django.db import transaction, IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from contacts.serializers import ContactSerializer
from networks_electronics.serializers import FactoryBaseSerializer
from products.models import Product
from products.serializers import ProductCreateSerializer, ProductSmallSerializer
from networks_electronics.serializers.main_network_serializers import MainNetworkBaseSerializer
from networks_electronics.serializers.retail_network_serializers import RetailNetSupplierSerializer
from sole_proprietor.models import SoleProprietor
from contacts.models import Contact


class SoleProprietorSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели SoleProprietor с информацией о связанных объектах:
    main_network, contact, factory_supplier, retail_network_supplier, products.
    """
    contact = ContactSerializer(read_only=True)
    factory_supplier = FactoryBaseSerializer(read_only=True)
    retail_network_supplier = RetailNetSupplierSerializer(read_only=True)
    main_network = MainNetworkBaseSerializer(read_only=True)
    products = ProductSmallSerializer(many=True, read_only=True)

    class Meta:
        model = SoleProprietor
        fields = ('id', 'main_network', 'name', 'contact', 'products', 'factory_supplier',
                  'retail_network_supplier', 'debt_to_supplier', 'created_at', 'is_active')


class SoleProprietorCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания объектов модели SoleProprietor.
    transaction.atomic() используется для предотвращения каких-либо воздействий на базу данных,
    если только все действия в переопределенном методе create() не будут выполнены успешно
    """
    contact = ContactSerializer(many=False, required=True)
    new_products = ProductCreateSerializer(many=True, required=False)
    product_ids_to_add = serializers.ListSerializer(child=serializers.IntegerField(), required=False)

    class Meta:
        model = SoleProprietor
        fields = (
            'id', 'main_network', 'name', 'contact', 'new_products', 'product_ids_to_add', 'factory_supplier',
            'retail_network_supplier',)

    def create(self, validated_data):
        with transaction.atomic():
            contact_data = validated_data.pop('contact')
            new_products_data = validated_data.pop('new_products', [])
            product_ids_to_add_data = validated_data.pop('product_ids_to_add', [])
            contacts = Contact(**contact_data)
            contacts.save()
            sole_proprietor = SoleProprietor.objects.create(**validated_data, contact_info=contacts)

            for product in new_products_data:
                sole_proprietor.products.create(**product)

            for product_id in product_ids_to_add_data:
                try:
                    product = get_object_or_404(Product, pk=product_id)
                    sole_proprietor.products.add(product)
                except Http404:
                    raise serializers.ValidationError(f'Продукт с id "{product_id}" не найден')

            return sole_proprietor


class SoleProprietorUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления объектов модели SoleProprietor.
    transaction.atomic() используется для предотвращения каких-либо воздействий на базу данных,
    если только все действия в переопределенном методе updated() не будут выполнены успешно.
    """
    name = serializers.CharField(required=False)
    contact_id = serializers.IntegerField(required=False)
    product_ids_to_add = serializers.ListSerializer(child=serializers.IntegerField(), required=False)
    product_ids_to_remove = serializers.ListSerializer(child=serializers.IntegerField(), required=False)

    class Meta:
        model = SoleProprietor
        fields = ('name', 'contact_id', 'product_ids_to_add', 'product_ids_to_remove', 'factory_supplier',
                  'retail_network_supplier', 'is_active',)

    def update(self, sole_proprietor, validated_data):
        with transaction.atomic():
            contact_data = validated_data.pop('contact_id', None)
            if contact_data:
                try:
                    new_contacts = get_object_or_404(Contact, pk=contact_data)
                    sole_proprietor.contact = new_contacts
                except Http404:
                    raise serializers.ValidationError(f'Контактная информация с id "{contact_data}" не найдена')

            prod_ids_to_add_data = validated_data.pop('product_ids_to_add', [])
            for product_id in prod_ids_to_add_data:
                try:
                    prod_to_add = get_object_or_404(Product, pk=product_id)
                    sole_proprietor.products.add(prod_to_add)
                except Http404:
                    raise serializers.ValidationError(f'Продукт с id "{product_id}" не найден')

            prod_ids_to_remove_data = validated_data.pop('product_ids_to_remove', [])
            for product_id in prod_ids_to_remove_data:
                try:
                    prod_to_remove = get_object_or_404(Product, pk=product_id)
                    if prod_to_remove not in sole_proprietor.products.all():
                        raise serializers.ValidationError(
                            f"Продукт {product_id} не связан с {sole_proprietor}")
                    sole_proprietor.products.remove(prod_to_remove)
                except Http404:
                    raise serializers.ValidationError(f'Продукт с id "{product_id}" не найден')

            for attr, val in validated_data.items():
                setattr(sole_proprietor, attr, val)

            try:
                sole_proprietor.save()
            except IntegrityError:
                raise serializers.ValidationError(
                    f'Контакт с id "{contact_data}" уже связан с другим объектом.')
            return sole_proprietor
