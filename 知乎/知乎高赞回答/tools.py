#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @Time    : 2020-09-08 15:26
#  @Author  : July
import pymysql


def save_to_mysql(table_name, data):
    """
    保存数据熬mysql，需要事先建好数据库和表
    :param table_name:表名
    :param data:保存的数据，格式：[{},{},{}]
    :return:
    """
    db = pymysql.connect(host="118.89.90.148", port=3307, user="root", password="123456", db="zhihu")
    cursor = db.cursor()
    keys = ', '.join(data[0].keys())
    values = ', '.join(['%s'] * len(data[0]))
    sql = 'INSERT INTO {} ({}) VALUES ({})'.format(table_name, keys, values)
    try:
        cursor.executemany(sql, map(lambda x: list(x), [i.values() for i in data]))
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    db.close()