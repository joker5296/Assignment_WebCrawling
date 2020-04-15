# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector

class AssignmentWebcrawlerPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()
    
    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = '5296',
            database = 'reuters'
        )
        self.curr = self.conn.cursor()
    
    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS reuters_tb""")
        self.curr.execute("""CREATE TABLE reuters_tb(
                        img_link text,
                        title text,
                        summary text,
                        time_of_publish text,
                        web_link text
        )""")
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        self.curr.execute("""INSERT INTO reuters_tb VALUES(%s, %s, %s, %s, %s) """, (
            item['img_link'],
            item['title'],
            item['summary'],
            item['time_of_publish'],
            item['web_link']
        ))
        self.conn.commit()
