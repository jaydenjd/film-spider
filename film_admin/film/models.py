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
    movie_name = models.CharField(max_length=50, verbose_name='电影名称')
    movie_type = models.CharField(max_length=50, verbose_name='电影类型')
    movie_region = models.CharField(max_length=50, verbose_name='电影地区')
    movie_lang = models.CharField(max_length=20, verbose_name='电影语言')
    movie_score = models.FloatField(verbose_name='电影评分')
    movie_release_time = models.CharField(max_length=30, verbose_name='电影上映时间')
    movie_videourl = models.CharField(max_length=100, verbose_name='电影宣传视频')
    movie_dra = models.CharField(max_length=300, verbose_name='电影简介')
    # movie_info = models.CharField(max_length=1000, verbose_name='电影信息')
    # add_date = models.DateTimeField(auto_now_add=True, verbose_name="创建日期")
    # mod_date = models.DateTimeField(auto_now=True, verbose_name="修改日期")

    class Meta:
        db_table = 'movie_info'
        verbose_name = '电影基本信息表'
        verbose_name_plural = "电影基本信息表"
    # movie_videourl = models.CharField(max_length=200, default='')
    # movie_distributions = models.CharField(max_length=200, default='')


class CommentsModel(models.Model):
    # movie_id = models.ForeignKey(MovieInfoModel, on_delete=models.CASCADE)
    comment_id = models.IntegerField(primary_key=True)  # 评论id
    movie_id = models.IntegerField()  # 评论id
    nickName = models.CharField(max_length=50, verbose_name='昵称')
    gender = models.IntegerField(verbose_name='性别')
    cityName = models.CharField(max_length=10, verbose_name='所在城市')
    score = models.FloatField(verbose_name='评分')
    content = models.CharField(max_length=500, verbose_name='评论')
    start_time = models.CharField(max_length=30, verbose_name='评论时间')
    # comments = models.CharField(max_length=1000, verbose_name='评论信息')

    class Meta:
        db_table = 'comments'
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