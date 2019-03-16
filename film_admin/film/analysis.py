# from ..film_admin.settings import DATABASES
import pymysql
from pyecharts import Bar, Pie, Map, Style, Geo, Line

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'film_spider',
        'USER': 'root',
        'HOST': 'localhost',
        'PASSWORD': 'root',
        'PORT': 3306,
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

class Analysis(object):

    def __init__(self):
        self.host = DATABASES['default']['HOST']
        self.user = DATABASES['default']['USER']
        self.password = DATABASES['default']['PASSWORD']
        self.database = DATABASES['default']['NAME']
        self.port = DATABASES['default']['PORT']

    def exc_sql(self, sql):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database, port=self.port,
                             charset='utf8mb4')
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result

    # 分数饼图
    def score_pie(self):
        query_sql = "SELECT score,COUNT(score) as s FROM film_spider.movie_comments WHERE movie_id=341139 GROUP BY score"
        data_list = self.exc_sql(query_sql)
        attr = []
        value = []
        for i, j in data_list:
            attr.append(i)
            value.append(j)

        pie = Pie("饼状图", "评分表", title_pos='left', width=1500)
        pie.add("评分表", attr, value, center=[25, 50], is_random=True, is_legend_show=False,is_label_show=True)
        # pie.add("蒸发量", columns, data2, center=[75, 50], is_legend_show=False, is_label_show=True)
        pie.render('myecharts/score_pie.html')

    # 性别饼图
    def gender_pie(self):
        query_sql = "SELECT gender,COUNT(gender) as s FROM film_spider.movie_comments WHERE movie_id=341139 GROUP BY gender"
        data_list = self.exc_sql(query_sql)
        attr = []
        value = []
        for i, j in data_list:
            attr.append(i)
            value.append(j)
        pie = Pie("饼状图", "评分表", title_pos='left', width=1500)
        pie.add("性别", attr, value, center=[25, 50], radius=[30, 75], is_legend_show=False, is_label_show=True)
        pie.render('myecharts/gender_pie.html')
    # 评论日期分布折线图
    def line_date(self):
        query_sql = "SELECT date,COUNT(date) as s FROM film_spider.movie_comments WHERE movie_id=341139 GROUP BY date"
        data_list = self.exc_sql(query_sql)
        attr = []
        value = []
        for i, j in data_list:
            attr.append(i)
            value.append(j)
        # 普通折线图
        line = Line('折线图')
        line.add('评论日期', attr, value, mark_point=['min', 'max'], is_smooth=True)
        line.show_config()
        line.render('myecharts/line_date.html')


    # def city_map(self):
    #     query_sql = "SELECT cityName,COUNT(cityName) as s FROM film_spider.movie_comments WHERE movie_id=341139 GROUP BY cityName"
    #     data_list = self.exc_sql(query_sql)
    #     attr = []
    #     value = []
    #     for i, j in data_list:
    #         attr.append(i)
    #         value.append(j)
    #     map = Map("中国地图", '中国地图', width=1200, height=600)
    #     map.add("", attr, value, visual_range=[0, 50], maptype='china', is_visualmap=True,
    #             visual_text_color='#000')
    #     map.show_config()
    #     map.render('myecharts/city_map.html')
    #
    #     # 定义样式
    #     style = Style(
    #         title_color='#fff',
    #         title_pos='center',
    #         width=1200,
    #         height=600,
    #         background_color='#404a59'
    #     )
    #
    #     # 根据城市数据生成地理坐标图
    #     geo = Geo('《一出好戏》粉丝位置分布', '数据来源：猫眼-汤小洋采集', **style.init_style)
    #     geo.add('', attr, value, visual_range=[0, 3500],
    #             visual_text_color='#fff', symbol_size=15,
    #             is_visualmap=True, is_piecewise=True, visual_split_number=10)
    #     geo.render('myecharts/粉丝位置分布-地理坐标图.html')



if __name__ == '__main__':
    a = Analysis()
    a.score_pie()
    a.gender_pie()
    # a.city_map()
    a.line_date()


