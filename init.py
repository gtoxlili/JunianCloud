# -*- coding: utf-8 -*-

import pymysql
import yaml
with open("configuration.yaml", "r", encoding="utf-8") as f:
    dataMapsd = yaml.safe_load(f)

if dataMapsd["configuration"]["Storage"] == "mysql":
    try:
        connsx = pymysql.connect(host=dataMapsd["configuration"]["mysql"]["host"], user=dataMapsd["configuration"]["mysql"]["user"], passwd=dataMapsd["configuration"]
                                ["mysql"]["passwd"], port=dataMapsd["configuration"]["mysql"]["port"], charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        print("mysql is connected")
        cursor = connsx.cursor()
        sql = "CREATE DATABASE IF NOT EXISTS jncloud"
        cursor.execute(sql)
        print("Database created")
        sql23 = "USE jncloud"
        cursor.execute(sql23)
        sql_2 = '''CREATE TABLE IF NOT EXISTS `tuchuan` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `md5` VARCHAR(255) NOT NULL,
        `name` VARCHAR(255) NOT NULL,
        `date` VARCHAR(255) NOT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        cursor.execute(sql_2)
        print("Data table created")
        cursor.close()
        connsx.close()
    except:
        print("Database connection error, please try again later (Also run ` init.py ` separately)")
else:
    pass
