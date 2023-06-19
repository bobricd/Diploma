from django.db import IntegrityError
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import ValidationError

from Swipe.residential_complexes.models import ResidentialComplex, Advantage, Document, News, Image, Block, Section, \
    Floor, Riser


class RiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Riser
        fields = '__all__'


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'


class BlockSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get("request")
        try:
            residential_complex = ResidentialComplex.objects.get(builder=request.user)
            try:
                return Block.objects.create(residential_complex=residential_complex, **validated_data)
            except IntegrityError:
                raise ValidationError("Block with this name already exists")
        except ResidentialComplex.DoesNotExist:
            raise ValidationError("You don't have Residential Complex")

    class Meta:
        model = Block
        exclude = ('residential_complex',)


class AdvantageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advantage
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get("request")
        try:
            residential_complex = ResidentialComplex.objects.get(builder=request.user)
            return News.objects.create(residential_complex=residential_complex, **validated_data)
        except ResidentialComplex.DoesNotExist:
            raise ValidationError("You don't have Residential Complex")

    class Meta:
        model = News
        fields = ('date_created', 'title', 'text',)


class DocumentSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            residential_complex = request.user.residentialcomplex
            return Document.objects.create(residential_complex=residential_complex, **validated_data)
        else:
            raise ValueError("You don't have Residential Complex")

    class Meta:
        model = Document
        fields = ('file', 'is_excel')


class BaseImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, represent_in_base64=True)
    order = serializers.IntegerField(max_value=32767)

    class Meta:
        model = Image
        fields = ['image', 'order']


class ImageUpdateSerializer(BaseImageSerializer):
    class Meta:
        model = Image
        fields = ['image', 'order']


class ImageListSerializer(BaseImageSerializer):
    image = Base64ImageField(required=False, represent_in_base64=False)


class BaseResidentialComplexSerializer(serializers.ModelSerializer):
    advantages = serializers.PrimaryKeyRelatedField(queryset=Advantage.objects.all(), many=True, allow_empty=True,
                                                    required=False)
    documents = DocumentSerializer(many=True, read_only=True)
    news = NewsSerializer(many=True, read_only=True)
    images = BaseImageSerializer(many=True, read_only=True)

    class Meta:
        model = ResidentialComplex
        fields = (
            'id', 'advantages', 'images', 'news', 'documents', 'name', 'description', 'address', 'contact_first_name',
            'contact_last_name', 'contact_phone', 'contact_email', 'house_status', 'house_type', 'house_class',
            'construction', 'territory', 'communal_payments', 'ceiling_height', 'distance_to_sea')


class ResidentialComplexCreateSerializer(BaseResidentialComplexSerializer):
    images = BaseImageSerializer(many=True)

    # def validate(self, attrs):
    #     if self.context.get("request").user.residentialcomplex:
    #         raise serializers.ValidationError("You already have a residential complex")
    #     return attrs

    def create(self, validated_data):
        builder = self.context.get("request").user
        try:
            if ResidentialComplex.objects.get(builder=builder):
                raise ValidationError("You already have residential complex")
        except ResidentialComplex.DoesNotExist:
            pass
        images_data = validated_data.pop('images')
        validated_data['builder'] = builder
        residential_complex = super().create(validated_data)
        for image_data in images_data:
            Image.objects.create(residential_complex=residential_complex, **image_data)
        return residential_complex


class ResidentialComplexUpdateSerializer(BaseResidentialComplexSerializer):
    images = ImageUpdateSerializer(many=True)
    advantages = AdvantageSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        try:
            images_data = validated_data.pop('images')
        except KeyError:
            images_data = None
        residential_complex = super().update(instance, validated_data)
        if images_data:
            existing_images = {image.order: image for image in residential_complex.images.all()}
            new_images = []
            for image_data in images_data:
                order = image_data.get('order')
                image = existing_images.get(order)
                if image:
                    image.order = image_data.get('order')
                    image.image = image_data.get('image')
                    image.save()
                    existing_images.pop(order)
                else:
                    new_images.append(Image(residential_complex=instance, **image_data))
            try:
                Image.objects.bulk_create(new_images)
                Image.objects.filter(residential_complex=instance, order__in=existing_images.keys()).delete()
            except IntegrityError as e:
                raise ValidationError(detail=e)
        return residential_complex


class ResidentialComplexListSerializer(BaseResidentialComplexSerializer):
    images = ImageListSerializer(many=True)
    min_price = serializers.IntegerField(default=0)
    min_area = serializers.IntegerField(default=0)

    class Meta:
        model = ResidentialComplex
        fields = ('name', 'address', 'min_price', 'min_area', 'images')
