import pymysql


MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'film_spider'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_PORT = 3306

def exc_sql():
    host = MYSQL_HOST
    database = MYSQL_DATABASE
    user = MYSQL_USER
    password = MYSQL_PASSWORD
    port = MYSQL_PORT
    db = pymysql.connect(host=host, user=user, password=password, db=database, port=port, charset='utf8mb4')
    cursor = db.cursor()
    query_sql = "SELECT content FROM film_spider.maoyan_movie_comments"
    cursor.execute(query_sql)
    # result = cursor.fetchall()
    result = cursor.fetchall()
    db.close()
    return result
if __name__ == '__main__':
    result = exc_sql()
    movie_id_list = [movie_id[0] for movie_id in result]
    # for i in exc_sql():
    #     print(i[0])
    print(movie_id_list)
