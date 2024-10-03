# 保存爬取的数据
import pymysql
import requests
from doubanbookspider.util import Util

"""数据库操作"""


class DBHelper:

    def __init__(self, filepath):
        self.filepath = filepath  # 文件保存路径
        pymysql.version_info = (1, 4, 13, "final", 0)  # 必须有这个不然会报版本不对错误
        pymysql.install_as_MySQLdb()  # 使用pymysql代替mysqldb连接数据库
        # 建立数据库连接
        self.conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="Ll20010312@",
            db="simpleonlinebookcfrspython"
        )
        # 通过 cursor() 创建游标对象，并让查询结果以字典格式输出
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):  # 对象资源被释放时触发，在对象即将被删除时的最后操作
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def select_db(self, sql):
        """查询"""
        # 使用 execute() 执行sql
        self.cur.execute(sql)
        # 使用 fetchall() 获取查询结果
        data = self.cur.fetchall()
        return data

    def execute_db(self, sql):
        """更新/插入/删除"""
        try:
            # 使用 execute() 执行sql
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
        except Exception as e:
            print("操作出现错误：{}".format(e))
            # 回滚所有更改
            self.conn.rollback()

    def findType(self, typename):
        """查找或者保存图书类型"""
        select_sql_temp = "select * from type where typename = '%s'" % typename
        result = self.select_db(select_sql_temp)
        if result is None or len(result) == 0:
            insert_sql_temp = "insert into type (typename) values('%s')" % typename
            self.execute_db(insert_sql_temp)
        else:
            print("类型：%s  已存在数据库中！" % typename)
        result = self.select_db(select_sql_temp)
        return result[0]

    def findItem(self, itemname, typeid, image, content):
        """查找或者保存图书"""
        select_sql_temp = "select * from item where itemname = '%s'" % itemname
        result = self.select_db(select_sql_temp)
        if result is None or len(result) == 0:
            # 保存图书封面到项目中
            r = requests.get(image)
            image = Util().getCurrentTimeRandom() + '.jpg'
            with open(self.filepath + image, 'wb') as f:
                f.write(r.content)
            insert_sql_temp = "insert into item (itemname," \
                              "typeid,image,content,createtime) values('%s',%s,'%s','%s','%s')" % (
                                  itemname, typeid, image, content, Util().getCurrentTime())
            self.execute_db(insert_sql_temp)
        else:
            print("图书：%s  已存在数据库中！" % itemname)

    def findItemEx(self, itemname):
        """查找图书"""
        select_sql_temp = "select * from item where itemname = '%s'" % itemname
        return self.select_db(select_sql_temp)

    def saveItem(self, item):
        """查找或者保存图书"""
        select_sql_temp = "select * from item where itemname = '%s'" % item["itemname"]
        result = self.select_db(select_sql_temp)
        if result is None or len(result) == 0:
            # 保存图书封面到项目中
            r = requests.get(item["image"])
            image = Util().getCurrentTimeRandom() + '.jpg'
            with open(self.filepath + image, 'wb') as f:
                f.write(r.content)
            insert_sql_temp = "insert into item (itemname," \
                              "typeid,image,content,createtime) values('%s',%s,'%s','%s','%s')" % (
                                  item["itemname"], item["type"].get("id"), image, item["content"], Util().getCurrentTime())
            self.execute_db(insert_sql_temp)
        else:
            print("图书：%s  已存在数据库中！" % item["itemname"])


if __name__ == '__main__':
    # 测试连接
    db = DBHelper("")
    select_sql = 'SELECT * FROM type'
    data = db.select_db(select_sql)
    for type_temp in data:
        print('self.bookTypeList.append("%s")' % type_temp["typename"])
