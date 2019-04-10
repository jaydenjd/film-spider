

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DoubanMovieComments',
            fields=[
                ('uuid', models.IntegerField(verbose_name='电影uuid')),
                ('comment_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='评论id')),
                ('nickName', models.CharField(max_length=50, verbose_name='昵称')),
                ('gender', models.CharField(max_length=10, verbose_name='性别')),
                ('cityName', models.CharField(max_length=10, verbose_name='所在城市')),
                ('score', models.FloatField(verbose_name='评分')),
                ('data_from', models.CharField(max_length=200, verbose_name='数据来源')),
                ('date', models.CharField(max_length=30, verbose_name='评论日期')),
                ('time', models.CharField(max_length=30, verbose_name='评论时间')),
                ('content', models.CharField(max_length=500, verbose_name='评论内容')),
                ('source_url', models.URLField(verbose_name='数据链接')),
            ],
            options={
                'verbose_name': '豆瓣影评表',
                'verbose_name_plural': '豆瓣影评表',
                'db_table': 'douban_movie_comments',
            },
        ),
        migrations.CreateModel(
            name='DoubanMovieInfo',
            fields=[
                ('uuid', models.IntegerField(unique=True, verbose_name='电影uuid')),
                ('movie_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='电影id')),
                ('name', models.CharField(max_length=50, verbose_name='电影名称')),
                ('enm', models.CharField(max_length=50, verbose_name='电影英文名')),
                ('type', models.CharField(max_length=50, verbose_name='电影类型')),
                ('region', models.CharField(max_length=50, verbose_name='电影地区')),
                ('lang', models.CharField(max_length=20, verbose_name='电影语言')),
                ('durations', models.CharField(max_length=20, verbose_name='时长')),
                ('score', models.FloatField(verbose_name='电影评分')),
                ('pubdate', models.CharField(max_length=20, verbose_name='电影上映时间')),
                ('data_from', models.CharField(max_length=10, verbose_name='数据来源')),
                ('img', models.URLField(max_length=500, verbose_name='电影海报')),
                ('videourl', models.URLField(max_length=500, verbose_name='电影预告片')),
                ('directors', models.CharField(max_length=3000, verbose_name='导演信息')),
                ('actors', models.CharField(max_length=3000, verbose_name='导演信息')),
                ('writers', models.CharField(max_length=3000, verbose_name='编剧信息')),
                ('dra', models.CharField(max_length=3000, verbose_name='电影简介')),
            ],
            options={
                'verbose_name': '豆瓣电影基本信息表',
                'verbose_name_plural': '豆瓣电影基本信息表',
                'db_table': 'douban_movie_info',
            },
        ),
        migrations.CreateModel(
            name='DoubanMovieRequest',
            fields=[
                ('movie_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='电影id')),
                ('movie_name', models.CharField(max_length=50, verbose_name='电影名称')),
                ('region', models.CharField(choices=[('china', '国内'), ('foreign', '国外')], default='china', max_length=10, verbose_name='地区')),
                ('request_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='请求时间')),
                ('create_date', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '豆瓣电影爬虫请求表',
                'verbose_name_plural': '豆瓣电影爬虫请求表',
                'db_table': 'douban_movie_request',
            },
        ),
        migrations.CreateModel(
            name='MaoyanMovieComments',
            fields=[
                ('uuid', models.IntegerField(verbose_name='电影uuid')),
                ('comment_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='评论id')),
                ('nickName', models.CharField(max_length=50, verbose_name='昵称')),
                ('gender', models.CharField(max_length=10, verbose_name='性别')),
                ('cityName', models.CharField(max_length=10, verbose_name='所在城市')),
                ('score', models.FloatField(verbose_name='评分')),
                ('data_from', models.CharField(max_length=200, verbose_name='数据来源')),
                ('date', models.CharField(max_length=30, verbose_name='评论日期')),
                ('time', models.CharField(max_length=30, verbose_name='评论时间')),
                ('content', models.CharField(max_length=500, verbose_name='评论内容')),
                ('source_url', models.URLField(verbose_name='数据链接')),
            ],
            options={
                'verbose_name': '猫眼影评表',
                'verbose_name_plural': '猫眼影评表',
                'db_table': 'maoyan_movie_comments',
            },
        ),
        migrations.CreateModel(
            name='MaoyanMovieInfo',
            fields=[
                ('uuid', models.IntegerField(unique=True, verbose_name='电影uuid')),
                ('movie_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='电影id')),
                ('name', models.CharField(max_length=50, verbose_name='电影名称')),
                ('enm', models.CharField(max_length=50, verbose_name='电影英文名')),
                ('type', models.CharField(max_length=50, verbose_name='电影类型')),
                ('region', models.CharField(max_length=50, verbose_name='电影地区')),
                ('lang', models.CharField(max_length=20, verbose_name='电影语言')),
                ('durations', models.CharField(max_length=20, verbose_name='时长')),
                ('score', models.FloatField(verbose_name='电影评分')),
                ('pubdate', models.CharField(max_length=20, verbose_name='电影上映时间')),
                ('data_from', models.CharField(max_length=10, verbose_name='数据来源')),
                ('img', models.URLField(max_length=500, verbose_name='电影海报')),
                ('videourl', models.URLField(max_length=500, verbose_name='电影预告片')),
                ('directors', models.CharField(max_length=3000, verbose_name='导演信息')),
                ('actors', models.CharField(max_length=3000, verbose_name='导演信息')),
                ('writers', models.CharField(max_length=3000, verbose_name='编剧信息')),
                ('dra', models.CharField(max_length=3000, verbose_name='电影简介')),
            ],
            options={
                'verbose_name': '猫眼电影基本信息表',
                'verbose_name_plural': '猫眼电影基本信息表',
                'db_table': 'maoyan_movie_info',
            },
        ),
        migrations.CreateModel(
            name='MaoyanMovieRequest',
            fields=[
                ('movie_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='电影id')),
                ('movie_name', models.CharField(max_length=50, verbose_name='电影名称')),
                ('region', models.CharField(choices=[('china', '国内'), ('foreign', '国外')], default='china', max_length=10, verbose_name='地区')),
                ('request_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='请求时间')),
                ('create_date', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '猫眼爬虫请求表',
                'verbose_name_plural': '猫眼爬虫请求表',
                'db_table': 'maoyan_movie_request',
            },
        ),
        migrations.AddField(
            model_name='maoyanmoviecomments',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='film.MaoyanMovieInfo'),
        ),
        migrations.AddField(
            model_name='doubanmoviecomments',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='film.DoubanMovieInfo'),
        ),
    ]
