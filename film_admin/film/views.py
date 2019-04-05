import pymysql
from django.shortcuts import render

# Create your views here.
from django.db import connection
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from pyecharts import Bar, Pie
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# from film_admin.film.serializers import MeiziSerializer
from .models import *

REMOTE_HOST = "https://pyecharts.github.io/assets/js"
DATABASES = {
    'NAME': 'film_spider',
    'USER': 'root',
    'HOST': 'localhost',
    'PASSWORD': 'root',
    'PORT': 3306,

}

class IndexView(generic.ListView):
    template_name = 'film/index.html'
    context_object_name = 'movies'

    def get_queryset(self):
        '''return the last five published questions'''
        # return Question.objects.order_by('-pub_date')[:5]
        # return MaoyanMovieInfo.objects.order_by('-movie_id')
        return MovieInfoModel.objects.order_by('-movie_id')

# class DetailView(generic.DetailView):
#     model = MovieInfoModel
#     template_name = 'film/detail.html'
#
#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return MovieInfoModel.objects.order_by('-movie_id')

class ResultsView(generic.DetailView):

    # model = MaoyanMovieInfo
    model = MovieInfoModel
    template_name = 'film/result.html'
    def __init__(self, pk):
        self.pk = pk


def get_queryset(request, pk):
    template = loader.get_template('film/result.html')
    pk = pk
    b = bar(pk)
    context = dict(
        myechart=b.render_embed(),
        host=REMOTE_HOST,
        script_list=b.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))

def exc_sql(sql):
    db = pymysql.connect(host=DATABASES['HOST'], user=DATABASES['USER'], password=DATABASES['PASSWORD'], port=DATABASES['PORT'])
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def result(request, pk):
    template = loader.get_template('film/result.html')
    b = bar(pk)
    context = dict(
        myechart=b.render_embed(),
        host=REMOTE_HOST,
        script_list=b.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))


def bar(pk):
    query_sql = "SELECT score,COUNT(score) as s FROM film_spider.movie_comments WHERE movie_id={} GROUP BY score order by score ".format(pk)
    data_list = exc_sql(query_sql)
    x=[i[0] for i in data_list]
    y=[i[1] for i in data_list]
    bar=Bar("评分柱状图",width=1000,height=700)
    bar.add("数据来源："+'猫眼电影',x, y, type="effectScatter", border_color="#ffffff", symbol_size=2,
            is_label_show=True, label_text_color="#0000FF", label_pos="inside", symbol_color="yellow",
            bar_normal_color="#006edd", bar_emphasis_color="#0000ff")
    return bar


def score_pie():
    query_sql = "SELECT score,COUNT(score) as s FROM film_spider.movie_comments WHERE movie_id=248906 GROUP BY score"
    data_list = exc_sql(query_sql)
    attr = []
    value = []
    for i, j in data_list:
        attr.append(i)
        value.append(j)

    pie = Pie("饼状图", "评分表", title_pos='left', width=1500)
    pie.add("评分表", attr, value, center=[25, 50], is_random=True, is_legend_show=False,is_label_show=True)
    # pie.add("蒸发量", columns, data2, center=[75, 50], is_legend_show=False, is_label_show=True)
    # pie.render('myecharts/score_pie.html')
    return pie

