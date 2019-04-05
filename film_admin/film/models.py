import datetime

import django.utils.timezone as timezone

from django.db import models

class RequestInfoModel(models.Model):
    movie_id = models.IntegerField(primary_key=True, verbose_name='电影id')
    movie_name = models.CharField(max_length=50, verbose_name='电影名称')
    region = models.CharField(verbose_name='地区', max_length=10, choices=(('china', '国内'), ('foreign', '国外')),
                              default='china')
    request_date = models.DateTimeField(verbose_name='请求时间', default=timezone.now)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now=True)

    class Meta:
        db_table = 'request_info'
        verbose_name = '请求信息表'
        verbose_name_plural = "请求信息表"


class MovieInfoModel(models.Model):
    movie_id = models.IntegerField(primary_key=True, verbose_name='电影id')
    name = models.CharField(max_length=50, verbose_name='电影名称')
    enm = models.CharField(max_length=50, verbose_name='电影英文名')
    type = models.CharField(max_length=50, verbose_name='电影类型')
    region = models.CharField(max_length=50, verbose_name='电影地区')
    lang = models.CharField(max_length=20, verbose_name='电影语言')
    score = models.FloatField(verbose_name='电影评分')
    release_time = models.CharField(max_length=30, verbose_name='电影上映时间')
    img = models.CharField(max_length=100, verbose_name='电影海报')
    videourl = models.CharField(max_length=100, verbose_name='电影宣传视频')
    dra = models.CharField(max_length=300, verbose_name='电影简介')
    info = models.CharField(max_length=1000, verbose_name='电影信息')

    def __str__(self):
        return (self.name, self.enm).__str__()  # python3写法

    class Meta:
        db_table = 'movie_info'
        verbose_name = '电影基本信息表'
        verbose_name_plural = "电影基本信息表"


class CommentsModel(models.Model):
    comment_id = models.IntegerField(primary_key=True, verbose_name='评论id')
    movie = models.ForeignKey(MovieInfoModel, on_delete=models.CASCADE)
    nickName = models.CharField(max_length=50, verbose_name='昵称')
    gender = models.CharField(max_length=10, verbose_name='性别')
    cityName = models.CharField(max_length=10, verbose_name='所在城市')
    score = models.FloatField(verbose_name='评分')
    content = models.CharField(max_length=500, verbose_name='评论内容')
    date = models.CharField(max_length=30, verbose_name='评论日期')
    time = models.CharField(max_length=30, verbose_name='评论时间')
    source_url = models.CharField(max_length=200, verbose_name='数据来源')

    # start_time = models.CharField(max_length=30, verbose_name='评论时间')

    class Meta:
        db_table = 'movie_comments'
        verbose_name = '影评表'
        verbose_name_plural = "影评表"

#
# class MaoyanRequestInfo(models.Model):
#     movie_id = models.IntegerField(primary_key=True, verbose_name='电影id')
#     movie_name = models.CharField(max_length=50, verbose_name='电影名称')
#     region = models.CharField(verbose_name='地区', max_length=10, choices=(('china', '国内'), ('foreign', '国外')),default='china')
#     request_date = models.DateTimeField(verbose_name='请求时间', default=timezone.now)
#     create_date = models.DateTimeField(verbose_name='创建时间', auto_now=True)
#
#     class Meta:
#         db_table = 'maoyan_movie_request'
#         verbose_name = '猫眼电影爬虫请求表'
#         verbose_name_plural = "猫眼电影爬虫请求表"
#
# class MovieInfoModel(models.Model):
#     movie_id = models.IntegerField(primary_key=True, verbose_name='电影id')
#     name = models.CharField(max_length=50, verbose_name='电影名称')
#     enm = models.CharField(max_length=50, verbose_name='电影英文名')
#     type = models.CharField(max_length=50, verbose_name='电影类型')
#     region = models.CharField(max_length=50, verbose_name='电影地区')
#     lang = models.CharField(max_length=20, verbose_name='电影语言')
#     score = models.FloatField(verbose_name='电影评分')
#     release_time = models.CharField(max_length=30, verbose_name='电影上映时间')
#     img = models.CharField(max_length=100, verbose_name='电影海报')
#     videourl = models.CharField(max_length=100, verbose_name='电影宣传视频')
#     dra = models.CharField(max_length=300, verbose_name='电影简介')
#     # info = models.CharField(max_length=1000, verbose_name='电影信息')
#
#     def __str__(self):
#         return (self.name, self.enm).__str__()  # python3写法
#
#     class Meta:
#         db_table = 'movie_info'
#         verbose_name = '电影基本信息表'
#         verbose_name_plural = "电影基本信息表"
#
#
# class CommentsModel(models.Model):
#     comment_id = models.IntegerField(primary_key=True, verbose_name='评论id')
#     movie = models.ForeignKey(MovieInfoModel, on_delete=models.CASCADE)
#     nickName = models.CharField(max_length=50, verbose_name='昵称')
#     gender = models.CharField(max_length=10, verbose_name='性别')
#     cityName = models.CharField(max_length=10, verbose_name='所在城市')
#     score = models.FloatField(verbose_name='评分')
#     content = models.CharField(max_length=500, verbose_name='评论内容')
#     date = models.CharField(max_length=30, verbose_name='评论日期')
#     time = models.CharField(max_length=30, verbose_name='评论时间')
#     source_url = models.CharField(max_length=200, verbose_name='数据来源')
#
#     # start_time = models.CharField(max_length=30, verbose_name='评论时间')
#
#     class Meta:
#         db_table = 'movie_comments'
#         verbose_name = '影评表'
#         verbose_name_plural = "影评表"



# class MaoyanRequestInfo(models.Model):
#     movie_id = models.IntegerField(primary_key=True, verbose_name='电影id')
#     movie_name = models.CharField(max_length=50, verbose_name='电影名称')
#     region = models.CharField(verbose_name='地区', max_length=10, choices=(('china', '国内'), ('foreign', '国外')),
#                               default='china')
#     request_date = models.DateTimeField(verbose_name='请求时间', default=timezone.now)
#     create_date = models.DateTimeField(verbose_name='创建时间', auto_now=True)
#     # data_source = models.CharField(verbose_name='数据来源', max_length=10, choices=(('maoyan', '猫眼'), ('douban', '豆瓣')),
#     #                           default='maoyan')
#
#     class Meta:
#         db_table = 'maoyan_movie_request'
#         verbose_name = '猫眼电影爬虫请求表'
#         verbose_name_plural = "猫眼电影爬虫请求表"
#
#
# class MaoyanMovieInfo(models.Model):
#     # uuid = models.CharField(max_length=200,verbose_name='电影uuid', unique=True)
#     movie_id = models.IntegerField(primary_key=True, verbose_name='猫眼电影id')
#     name = models.CharField(max_length=50, verbose_name='电影名称')
#     enm = models.CharField(max_length=50, verbose_name='电影又名')
#     type = models.CharField(max_length=50, verbose_name='电影类型')
#     region = models.CharField(max_length=50, verbose_name='电影地区')
#     lang = models.CharField(max_length=20, verbose_name='电影语言')
#     durations = models.CharField(max_length=20, verbose_name='时长')
#     score = models.FloatField(verbose_name='电影评分')
#     pubdate = models.CharField(max_length=30, verbose_name='电影上映时间')
#     img = models.CharField(max_length=100, verbose_name='电影海报')
#     videourl = models.CharField(max_length=100, verbose_name='电影宣传视频')
#     dra = models.CharField(max_length=300, verbose_name='电影简介')
#     # info = models.CharField(max_length=1000, verbose_name='电影信息')
#
#     def __str__(self):
#         return (self.name, self.enm).__str__()  # python3写法
#
#     class Meta:
#         db_table = 'maoyan_movie_info'
#         verbose_name = '猫眼电影基本信息表'
#         verbose_name_plural = "猫眼电影基本信息表"
#
#
# class MaoyanCommentsModel(models.Model):
#     # uuid = models.CharField(max_length=200, verbose_name='电影uuid')
#     comment_id = models.IntegerField(primary_key=True, verbose_name='评论id')
#     movie = models.ForeignKey(MaoyanMovieInfo, on_delete=models.CASCADE)
#     nickName = models.CharField(max_length=50, verbose_name='昵称')
#     gender = models.CharField(max_length=10, verbose_name='性别')
#     cityName = models.CharField(max_length=10, verbose_name='所在城市')
#     score = models.FloatField(verbose_name='评分')
#     content = models.CharField(max_length=500, verbose_name='评论内容')
#     date = models.CharField(max_length=30, verbose_name='评论日期')
#     time = models.CharField(max_length=30, verbose_name='评论时间')
#     data_from = models.CharField(max_length=200, verbose_name='数据来源')
#     source_url = models.CharField(max_length=200, verbose_name='数据链接')
#
#     # start_time = models.CharField(max_length=30, verbose_name='评论时间')
#
#     class Meta:
#         db_table = 'maoyan_movie_comments'
#         verbose_name = '猫眼影评表'
#         verbose_name_plural = "猫眼影评表"
#
#
# class DoubanRequestInfo(models.Model):
#     movie_id = models.IntegerField(primary_key=True, verbose_name='电影id')
#     movie_name = models.CharField(max_length=50, verbose_name='电影名称')
#     region = models.CharField(verbose_name='地区', max_length=10, choices=(('china', '国内'), ('foreign', '国外')),
#                               default='china')
#     request_date = models.DateTimeField(verbose_name='请求时间', default=timezone.now)
#     create_date = models.DateTimeField(verbose_name='创建时间', auto_now=True)
#     # data_from = models.CharField(max_length=200, verbose_name='数据来源',choices=('douban', '豆瓣'),default='douban')
#
#     class Meta:
#         db_table = 'douban_movie_request'
#         verbose_name = '豆瓣电影爬虫请求表'
#         verbose_name_plural = "豆瓣电影爬虫请求表"
#
#
#
# class DoubanMovieInfo(models.Model):
#     uuid = models.CharField(max_length=200, verbose_name='电影uuid', unique=True)
#     movie_id = models.IntegerField(primary_key=True, verbose_name='豆瓣电影id')
#     name = models.CharField(max_length=50, verbose_name='电影名称')
#     enm = models.CharField(max_length=50, verbose_name='电影又名')
#     type = models.CharField(max_length=50, verbose_name='电影类型')
#     region = models.CharField(max_length=50, verbose_name='电影地区')
#     lang = models.CharField(max_length=20, verbose_name='电影语言')
#     durations = models.CharField(max_length=20, verbose_name='时长')
#     score = models.FloatField(verbose_name='电影评分')
#     pubdate = models.CharField(max_length=30, verbose_name='电影上映时间')
#     img = models.CharField(max_length=100, verbose_name='电影海报')
#     videourl = models.CharField(max_length=100, verbose_name='电影宣传视频')
#     dra = models.CharField(max_length=300, verbose_name='电影简介')
#
#     def __str__(self):
#         return (self.name, self.enm).__str__()  # python3写法
#
#     class Meta:
#         db_table = 'douban_movie_info'
#         verbose_name = '豆瓣电影基本信息表'
#         verbose_name_plural = "豆瓣电影基本信息表"
#
# class DoubanCommentsModel(models.Model):
#     uuid = models.CharField(max_length=200, verbose_name='电影uuid', unique=True)
#     comment_id = models.IntegerField(primary_key=True, verbose_name='评论id')
#     movie = models.ForeignKey(DoubanMovieInfo, on_delete=models.CASCADE)
#     nickName = models.CharField(max_length=50, verbose_name='昵称')
#     gender = models.CharField(max_length=10, verbose_name='性别')
#     cityName = models.CharField(max_length=10, verbose_name='所在城市')
#     score = models.FloatField(verbose_name='评分')
#     content = models.CharField(max_length=500, verbose_name='评论内容')
#     date = models.CharField(max_length=30, verbose_name='评论日期')
#     data_from = models.CharField(max_length=200, verbose_name='数据来源')
#     source_url = models.CharField(max_length=200, verbose_name='数据链接')
#
#     class Meta:
#         db_table = 'douban_movie_comments'
#         verbose_name = '豆瓣影评表'
#         verbose_name_plural = "豆瓣影评表"


    # start_time = models.CharField(max_length=30, verbose_name='评论时间')
# class MovieCommentsModel(mongoengine.Document):
#
#     movie_id = mongoengine.StringField(max_length=20, primary_key=True)  # 电影id
#     comment_id = mongoengine.StringField(max_length=16)  # 评论id
#     content = mongoengine.StringField(max_length=16)  # 评论内容
#     cityName = mongoengine.StringField(max_length=16)  # 评论者所在城市
#     nickName = mongoengine.StringField(max_length=16)  # 评论者昵称
#     gender = mongoengine.StringField(max_length=16)  # 评论者性别
#     start_time = mongoengine.StringField(max_length=16)  # 评论时间
#     score = mongoengine.FloatField()    # 评分
