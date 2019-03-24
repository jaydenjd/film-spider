import datetime
from datetime import timezone

from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import RequestInfoModel, MovieInfoModel


class RequestInfoModelAdmin(admin.ModelAdmin):
    list_display = ('movie_id', 'movie_name', 'region', 'request_date', 'create_date')
    search_fields = ['movie_name', 'movie_id']
    list_filter = ['region', 'request_date']
    ordering = ['-request_date', ]
    list_per_page = 20


class MovieInfoModelAdmin(admin.ModelAdmin):
    fields = ['movie_id', 'name', 'enm', 'type', 'region', 'lang', 'score', 'release_time', 'img', 'videourl', ]
    list_display = ('movie_id', 'name', 'enm','type', 'region', 'lang', 'score', 'release_time', 'img', 'videourl',)
    search_fields = ['name', 'movie_id']
    list_filter = ['movie_id']


admin.site.site_header = "电影爬虫后台"
admin.site.register(RequestInfoModel, RequestInfoModelAdmin)
admin.site.register(MovieInfoModel, MovieInfoModelAdmin)
