from django.db import transaction, IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from products.models import Product
from products.serializers import ProductCreateSerializer, ProductSmallSerializer
from contacts.models import Contact
from contacts.serializers import ContactSerializer
from networks_electronics.models.main_network_models import MainNetwork


class MainNetworkBaseSerializer(serializers.ModelSerializer):
    """
    Базовый класс сериализатора с краткой информацией: только id и имя.
    """

    class Meta:
        model = MainNetwork
        fields = ('id', 'name',)


class MainNetworkSerializer(serializers.ModelSerializer):
    """
    Класс сериализатара с полной информацией, используется для CRUD.
    """
    contact_info = ContactSerializer(read_only=True)
    products = ProductSmallSerializer(many=True, read_only=True)

    class Meta:
        model = MainNetwork
        fields = ('id', 'name', 'contact', 'products', 'created_at', 'is_active')


class MainNetworkCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания объектов модели MainNetwork.

    transaction.atomic() используется для предотвращения каких-либо воздействий на базу данных,
    если только все действия в переопределенном методе create() не будут выполнены успешно

    """
    contact = ContactSerializer(many=False, required=True)
    new_products = ProductCreateSerializer(many=True, required=False)
    product_ids_to_add = serializers.ListField(required=False)

    class Meta:
        model = MainNetwork
        fields = ('id', 'name', 'contact', 'new_products', 'product_ids_to_add',)

    def create(self, validated_data):
        with transaction.atomic():
            contacts_data = validated_data.pop('contact')
            new_products_data = validated_data.pop('new_products', [])
            prod_ids_list = validated_data.pop('product_ids_to_add', [])

            contacts = Contact.objects.create(**contacts_data)
            contacts.save()
            main_network = MainNetwork.objects.create(**validated_data, contact=contacts)

            for product in new_products_data:
                main_network.products.create(**product)

            for product_id in prod_ids_list:
                try:
                    prod_to_add = get_object_or_404(Product, pk=product_id)
                    main_network.products.add(prod_to_add)
                except Http404:
                    raise serializers.ValidationError(f'Продукт с id "{product_id}" не найден')

            return main_network


class MainNetworkUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления объектов модели MainNetwork.
    transaction.atomic() используется для предотвращения каких-либо воздействий на базу данных,
    если только все действия в переопределенном методе updated() не будут выполнены успешно.
    """
    name = serializers.CharField(required=False)
    contact_id = serializers.IntegerField(required=False)
    product_ids_to_add = serializers.ListField(child=serializers.IntegerField(), required=False)
    product_ids_to_remove = serializers.ListSerializer(child=serializers.IntegerField(), required=False)

    class Meta:
        model = MainNetwork
        fields = (
            'id', 'name', 'contact_id', 'product_ids_to_add', 'product_ids_to_remove', 'is_active',
        )

    def update(self, main_network, validated_data):
        with transaction.atomic():
            contact_data = validated_data.pop('contact_id', None)
            if contact_data:
                try:
                    new_contacts = get_object_or_404(Contact, pk=contact_data)
                    main_network.contact_info = new_contacts
                except Http404:
                    raise serializers.ValidationError(f'Контакт с id "{contact_data}" не найден')

            prod_ids_to_add_data = validated_data.pop('product_ids_to_add', [])
            for p_id in prod_ids_to_add_data:
                try:
                    prod_to_add = get_object_or_404(Product, pk=p_id)
                    main_network.products.add(prod_to_add)
                except Http404:
                    raise serializers.ValidationError(f'Продукт с id "{p_id}" не найден')

            prod_ids_to_remove_data = validated_data.pop('product_ids_to_remove', [])
            for p_id in prod_ids_to_remove_data:
                try:
                    prod_to_remove = get_object_or_404(Product, pk=p_id)
                    if prod_to_remove not in main_network.products.all():
                        raise serializers.ValidationError(f"Продукт {p_id} не связан с {main_network}")
                    main_network.products.remove(prod_to_remove)
                except Http404:
                    raise serializers.ValidationError(f'Продукт с id "{p_id}" не найден')

            for attr, val in validated_data.items():
                setattr(main_network, attr, val)

            try:
                main_network.save()
            except IntegrityError:
                raise serializers.ValidationError(
                    f'Контакт с id "{contact_data}" уже связан с другим объектом.')
            return main_network
