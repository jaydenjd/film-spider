from rest_framework import serializers

from .models import MovieInfoModel


class MeiziSerializer(serializers.ModelSerializer):
 # ModelSerializer和Django中ModelForm功能相似
 # Serializer和Django中Form功能相似
 class Meta:
     model = MovieInfoModel
     # 和"__all__"等价
     fields = ('movie_id', 'name', 'enm', 'img', 'videourl','dra')


