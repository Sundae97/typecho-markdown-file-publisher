import pymysql
import time

from pymysql.converters import escape_string


class TypechoDirectMysqlPublisher:
    def __init__(self, host, port, user, password, database, table_prefix):
        self.__table_prefix = table_prefix
        self.__categories_table_name = table_prefix + 'metas'
        self.__relationships_table_name = table_prefix + 'relationships'
        self.__contents_table_name = table_prefix + 'contents'
        self.__db = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        self.__init_categories()

    def __init_categories(self):
        cursor = self.__db.cursor()
        sql = "select mid,name from %s where type='%s'" % (self.__categories_table_name, 'category')
        cursor.execute(sql)
        results = cursor.fetchall()
        self.__exist_categories = []
        for item in results:
            self.__exist_categories.append({
                'mid': item[0],
                'name': item[1]
            })

    def __get_category_id(self, category_name):
        if len(self.__exist_categories) > 0:
            for item in self.__exist_categories:
                if item['name'] == category_name:
                    return item['mid']
        return -1

    def __add_category(self, category_name):
        cursor = self.__db.cursor()
        sql = "INSERT INTO %s " \
              "(`name`, `slug`, `type`, `description`, `count`, `order`, `parent`) " \
              "VALUES " \
              "('%s', '%s', 'category', '', 0, 1, 0)" % (self.__categories_table_name, category_name, category_name)
        cursor.execute(sql)
        mid = cursor.lastrowid
        self.__db.commit()
        self.__init_categories()
        return mid

    def __insert_relationship(self,cursor, cid, mid):
        insert_relationship_sql = "INSERT INTO %s" \
                                  "(`cid`, `mid`) " \
                                  "VALUES " \
                                  "(%d, %d)" % (self.__relationships_table_name, cid, mid)
        cursor.execute(insert_relationship_sql)

    def __update_category_count(self, cursor, mid):
        update_category_count_sql = "UPDATE %s SET `count`=`count`+1 WHERE mid=%d" % (self.__categories_table_name, mid)
        cursor.execute(update_category_count_sql)

    def publish_post(self, title, content, category):
        content = '<!--markdown-->' + content
        mid = self.__get_category_id(category)
        if mid < 0:
            mid = self.__add_category(category)

        now_time_int = int(time.time())
        cursor = self.__db.cursor()
        sql = "INSERT INTO %s " \
              "(`title`, `slug`, `created`, `modified`, `text`, `order`, `authorId`, `template`, `type`, `status`, `password`, `commentsNum`, `allowComment`, `allowPing`, `allowFeed`, `parent`) " \
              "VALUES " \
              "('%s', NULL , %d, %d, '%s', 0, 1, NULL, 'post', 'publish', NULL, 0, '1', '1', '1', 0)" \
              "" % (self.__contents_table_name, escape_string(title), now_time_int, now_time_int, escape_string(content))
        cursor.execute(sql)
        cid = cursor.lastrowid
        update_slug_sql = "UPDATE %s SET slug=%d WHERE cid=%d" % (self.__contents_table_name, cid, cid)
        cursor.execute(update_slug_sql)

        self.__insert_relationship(cursor, cid=cid, mid=mid)
        self.__update_category_count(cursor, mid)

        self.__db.commit()
        return cid
