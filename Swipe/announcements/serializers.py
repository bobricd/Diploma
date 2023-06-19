from rest_framework import serializers

from Swipe.announcements.models import Announcement, Image, Application


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, use_url=True)

    class Meta:
        model = Image
        fields = ('id', 'image')


class AnnouncementBaseSerializer(serializers.ModelSerializer):
    # images = ImageSerializer(many=True, read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        if data['area'] <= data['kitchen_area']:
            raise serializers.ValidationError("The kitchen area should be smaller than the main area")
        return data

    class Meta:
        model = Announcement
        fields = ('id', 'images', 'address', 'residential_complex', 'foundation_document', 'destination',
                  'number_rooms', 'layout', 'condition', 'area', 'kitchen_area', 'has_balcony', 'heating_type',
                  'payment_option', 'agent_commission', 'communication_method', 'description', 'price', 'owner',
                  'date_created')


class AnnouncementCrateSerializer(AnnouncementBaseSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(write_only=True),
        write_only=True
    )

    def create(self, validated_data):
        images = validated_data.pop('images')
        announcement = super().create(validated_data)
        if images:
            for image in images:
                Image.objects.create(announcement=announcement, image=image)
        return announcement


class AnnouncementUpdateSerializer(AnnouncementBaseSerializer):
    new_images = serializers.ListField(
        child=serializers.ImageField(write_only=True),
        write_only=True
    )

    def update(self, instance, validated_data):
        new_images = validated_data.pop('new_images')
        images = validated_data.pop('images')
        announcement = super().update(instance, validated_data)
        announcement.images.exclude(id__in=[img.id for img in images]).delete()
        if new_images:
            for image in new_images:
                Image.objects.create(announcement=instance, image=image)
        return announcement

    class Meta:
        model = Announcement
        fields = ('id', 'images', 'new_images', 'address', 'residential_complex', 'foundation_document', 'destination',
                  'number_rooms', 'layout', 'condition', 'area', 'kitchen_area', 'has_balcony', 'heating_type',
                  'payment_option', 'agent_commission', 'communication_method', 'description', 'price', 'owner',
                  'date_created')


class AnnouncementDetailSerializer(AnnouncementBaseSerializer):
    images = ImageSerializer(many=True, read_only=True)


class AnnouncementListSerializer(AnnouncementBaseSerializer):
    # pass
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Announcement
        fields = (
            'id', 'images', 'address', 'foundation_document', 'destination', 'number_rooms', 'layout', 'condition',
            'area', 'kitchen_area', 'has_balcony', 'heating_type', 'payment_option', 'agent_commission',
            'communication_method', 'description', 'price', 'owner', 'promotion_type')


class AnnouncementModerateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('id', 'images', 'address', 'number_rooms',
                  'area', 'price', 'date_created')


class AnnouncementModerateSerializer(serializers.ModelSerializer):
    is_moderate = serializers.HiddenField(default=True, initial=True)

    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
        fields['is_moderate'].read_only = False
        fields['approved'].read_only = False
        fields['moderate_message'].read_only = False
        fields['moderate_message'].required = False
        return fields

    def validate(self, attrs):
        if attrs['approved']:
            attrs['moderate_message'] = ''
            return attrs
        if not attrs.get('moderate_message'):
            raise serializers.ValidationError('Moderate message is empty')
        return attrs

    class Meta:
        model = Announcement
        fields = ('images', 'address', 'residential_complex', 'foundation_document', 'destination', 'number_rooms',
                  'layout', 'condition', 'area', 'kitchen_area', 'has_balcony', 'heating_type', 'payment_option',
                  'agent_commission', 'communication_method', 'description', 'price', 'is_moderate',
                  'approved', 'moderate_message', 'date_created')


class ApplicationConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('floor', 'riser')


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        exclude = ('residential_complex',)


class AnnouncementPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('promotion_type',)
