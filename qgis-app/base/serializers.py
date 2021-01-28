from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField


class ResourceBaseSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.ReadOnlyField(source='get_creator_name')

    class Meta:
        fields = ['url',
                  'id',
                  'name',
                  'creator',
                  'upload_date',
                  'download_count',
                  'description']


class ResourceThumbnailBaseSerializer(ResourceBaseSerializer):

    class Meta:
        fields = ResourceBaseSerializer.Meta.fields + ['thumbnail',
                                                       'thumbnail_image']

    # A thumbnail image, sorl options and read-only
    thumbnail = HyperlinkedSorlImageField(
        '128x128',
        options={"crop": "center"},
        source='thumbnail_image',
        read_only=True
    )

    # A larger version of the image, allows writing
    thumbnail_image = HyperlinkedSorlImageField('1024')

