from django.db import models

# import mongoengine


class RequestInfoModel(models.Model):
    movie_id = models.CharField(max_length=20, primary_key=True)
    movie_name = models.CharField(max_length=200, verbose_name='电影名称')
    request_date = models.DateTimeField('date published')

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

    class Meta:
        db_table = 'movie_info'
        verbose_name = '电影基本信息表'
        verbose_name_plural = "电影基本信息表"


class CommentsModel(models.Model):
    comment_id = models.IntegerField(primary_key=True, verbose_name='评论id')
    movie = models.ForeignKey(MovieInfoModel, on_delete=models.CASCADE)
    nickName = models.CharField(max_length=50, verbose_name='昵称')
    gender = models.IntegerField(verbose_name='性别')
    cityName = models.CharField(max_length=10, verbose_name='所在城市')
    score = models.FloatField(verbose_name='评分')
    content = models.CharField(max_length=500, verbose_name='评论')
    start_time = models.CharField(max_length=30, verbose_name='评论时间')

    class Meta:
        db_table = 'movie_comments'
        verbose_name = '影评表'
        verbose_name_plural = "影评表"

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