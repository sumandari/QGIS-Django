from rest_framework import serializers



class ResourceBaseSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='get_creator_name')

    class Meta:
        fields = ['id',
                  'name',
                  'creator',
                  'upload_date',
                  'download_count',
                  'description',
                  'thumbnail_image']