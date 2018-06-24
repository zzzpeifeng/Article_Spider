# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import codecs
import json
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ArticleSpiderPipeline(object):
    # 处理item
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 方法一：自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    # 处理item
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 方法二：调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    # 处理item
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for state, value in results:
                item_file_path = value["path"]
            item["front_image_path"] = item_file_path
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', 'root', 'article_spider', charset='utf8',
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = '''
        insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,comment_nums,fav_nums,praise_nums,tags,content) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        '''
        self.cursor.execute(insert_sql, (
            item['title'], item['create_time'], item['url'], item['url_object_id'], item['front_img_url'],
            item['comment_num'], item['fav_num'], item['praise_num'], item['tags'], item['content']))
        # self.cursor.execute(insert_sql, (
        #     'title', 'create_time', 'url', "2", "123",
        #     "123", "321", "321", "333",
        #     "111"))
        self.conn.commit()
        return item


class MysqlTwistedPipeline(object):
    #标准异步处理流程
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)  # 处理异常

    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)

    # 只需要修改
    def do_insert(self, cursor, item):
        insert_sql = '''
        insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,comment_nums,fav_nums,praise_nums,tags) values(%s,%s,%s,%s,%s,%s,%s,%s,%s);
        '''
        cursor.execute(insert_sql, (
            item['title'], item['create_time'], item['url'], item['url_object_id'], item['front_img_url'],
            item['comment_num'], item['fav_num'], item['praise_num'], item['tags']))
