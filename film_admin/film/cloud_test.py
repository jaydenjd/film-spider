# coding=utf-8
import pymysql

# 导入jieba模块，用于中文分词
import jieba
# 导入matplotlib，用于生成2D图形
import matplotlib.pyplot as plt
# 导入wordcount，用于制作词云图
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


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


class WordTest(object):
    def __init__(self):
        self.host = DATABASES['default']['HOST']
        self.user = DATABASES['default']['USER']
        self.password = DATABASES['default']['PASSWORD']
        self.database = DATABASES['default']['NAME']
        self.port = DATABASES['default']['PORT']
        self.movie_id = 410629

    def exc_sql(self, sql):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database, port=self.port,
                             charset='utf8mb4')
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result

    def getComments(self):


        # 获取所有评论
        query_sql = "SELECT content FROM film_spider.maoyan_movie_comments"
        result = self.exc_sql(query_sql)
        comments = [movie_id[0] for movie_id in result]
        print(comments)
        return comments

    def cloud(self):
        # 设置分词
        comments = self.getComments()
        print(str(comments))
        comment_after_split = jieba.cut(str(comments), cut_all=False)  # 非全模式分词，cut_all=false
        words = " ".join(comment_after_split)  # 以空格进行拼接
        print(type(words))
        print(''.join(words))
        # print(words)

        # 设置屏蔽词
        stopwords = STOPWORDS.copy()
        stopwords.add("电影")
        stopwords.add("一部")
        stopwords.add("一个")
        stopwords.add("没有")
        stopwords.add("什么")
        stopwords.add("有点")
        stopwords.add("这部")
        stopwords.add("这个")
        stopwords.add("不是")
        stopwords.add("真的")
        stopwords.add("感觉")
        stopwords.add("觉得")
        stopwords.add("还是")
        stopwords.add("但是")
        stopwords.add("就是")
        stopwords.add("他们")
        stopwords.add("可能")
        stopwords.add("应该")
        stopwords.add("怎么")
        stopwords.add("大家")


        # 导入背景图
        bg_image = plt.imread('g.jpg')
        # font = '/System/Library/Assets/com_apple_MobileAsset_Font5/6bb29eea6a5b99f3100a5e3f862e6457103557de.asset/AssetData/Hannotate.ttc'
        font = '/System/Library/Assets/com_apple_MobileAsset_Font5/4cecce0dd640f147de4d0e4155a97d3cdf47971e.asset/AssetData/Xingkai.ttc'
        # 设置词云参数，参数分别表示：画布宽高、背景颜色、背景图形状、字体、屏蔽词、最大词的字体大小
        wc = WordCloud(width=1024, height=768, background_color='white', mask=bg_image, font_path=font,
                       stopwords=stopwords, max_font_size=400, random_state=50)
        # 将分词后数据传入云图
        wc.generate_from_text(words)
        plt.imshow(wc)
        plt.axis('off')  # 不显示坐标轴
        plt.show()
        # 保存结果到本地
        wc.to_file('myecharts/词云图.jpg')

if __name__ == '__main__':

    WordTest().cloud()
