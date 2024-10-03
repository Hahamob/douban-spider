"""
豆瓣图书爬虫
原理：
首先爬取https://book.douban.com/tag/?view=type&icn=index-sorttags-all网址的网页数据，
该网页数据中有一级标签和二级标签，标签也就是图书类型
解析所有的一级标签和二级标签，一级标签没有链接地址，二级标签有链接地址
在爬取二级标签地址中的图书数据，二级标签地址如下
https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4
二级标签下的图书数据是分页显示
解析二级标签地址中的图书数据，得到20条图书数据的名称和图书详情链接地址，20条是固定设置
最后再爬取图书详情中的数据
通过控制每种二级类型的数量和每种二级类型下的图书数量来决定最终爬取的图书数量
"""
import random
import requests
from bs4 import BeautifulSoup
from doubanbookspider.dbhelper import DBHelper
from doubanbookspider.settings import User_Agents
from doubanbookspider.util import Util


class BookSpider(object):

    def __init__(self, bookCount, imagePath):
        # 基本的URL
        self.base_url = 'https://book.douban.com/tag/'
        # 全url=基本url+查询参数url+分页
        self.full_url = self.base_url + '{tag}?start={start}&type=T'
        # 从User-Agents中选择一个User-Agent
        self.headers = {'User-Agent': random.choice(User_Agents)}
        # 每种图书类型下爬取的图书数量，排除已经爬取的图书
        self.bookCount = bookCount
        pageSize = 20  # 每页查询数据条数，默认20
        # 初始化数据库链接
        self.dbHelper = DBHelper(imagePath)
        # 设置图书类型列表
        self.bookTypeList = list()
        self.bookTypeList.append("小说")
        self.bookTypeList.append("外国文学")
        self.bookTypeList.append("漫画")
        self.bookTypeList.append("推理")
        self.bookTypeList.append("历史")
        self.bookTypeList.append("心理学")
        self.bookTypeList.append("爱情")
        self.bookTypeList.append("成长")
        self.bookTypeList.append("经济学")
        self.bookTypeList.append("管理")
        self.bookTypeList.append("科普")
        self.bookTypeList.append("互联网")
        self.bookTypeList.append("文学")
        self.bookTypeList.append("经典")
        self.bookTypeList.append("中国文学")
        self.bookTypeList.append("绘本")
        self.bookTypeList.append("东野圭吾")
        self.bookTypeList.append("悬疑")
        self.bookTypeList.append("哲学")
        self.bookTypeList.append("社会学")
        self.bookTypeList.append("传记")
        self.bookTypeList.append("生活")
        self.bookTypeList.append("心理")
        self.bookTypeList.append("旅行")
        self.bookTypeList.append("经济")
        self.bookTypeList.append("商业")
        self.bookTypeList.append("金融")
        self.bookTypeList.append("科学")
        self.bookTypeList.append("编程")
        self.bookTypeList.append("交互设计")


    # 爬虫运行方法
    def catchData(self):
        print("***爬取豆瓣图书数据开始***")
        self.getBookTypes()
        print("***爬取豆瓣图书数据结束***")

    # 爬取图书类型
    def getBookTypes(self):
        try:
            # 遍历所有图书类型
            for typeName in self.bookTypeList:
                print("爬取图书类型：【%s" % typeName + "】开始")
                # 查询数据库中是否已存在当前图书类型，如果存在那么查询出来，不存在那么添加图书类型后查询出来
                type = self.dbHelper.findType(typeName)
                # 爬取图书列表
                self.getBooks(type)
                print("爬取图书类型：【%s" % typeName + "】结束")
        except Exception as ex:
            print(ex)

    # 爬取图书列表
    def getBooks(self, type):
        try:
            # https://book.douban.com/tag/小说?start=0&type=T
            # 分页查询当前图书类型下的图书，从第一页开始
            currentPage = 0
            # 临时变量，标记每页从第几条数据开始
            start = 0
            # 每种类型下爬取的图书数量，临时变量
            bookCountTemp = self.bookCount
            endFlag = False  # 每种类型下爬取电影结束标志
            # 遍历
            while True:
                # 每页20条数据
                start = currentPage * 20
                currentPage = currentPage + 1
                tag = type.get("typename")
                # 赋值图书列表链接查询参数
                fullUrlTemp = self.full_url.format(tag=tag, start=start)
                print("爬取图书类型：【%s" % type.get("typename") + "】第【" + str(currentPage) + "】页开始")
                print("链接地址：" + fullUrlTemp)
                # 反爬虫技术，所以不能一直爬取，休息一会
                Util().getRandomSleep()
                # 爬取数据
                resp = requests.get(fullUrlTemp, headers=self.headers)
                # 使用bs4模块解析html数据
                soup = BeautifulSoup(resp.text, 'lxml')
                # 解析出图书列表
                bookListDiv = soup.find(id="subject_list")
                bookList = bookListDiv.find_all("li",class_="subject-item")
                # 遍历图书列表
                for bookTemp in bookList:
                    # 图书数据标签
                    bookTag = bookTemp.find('div', class_="info").a
                    # 图书名称
                    bookName = bookTag.next.strip()
                    # 从数据库中查询图书名称判断是否存在
                    result = self.dbHelper.findItemEx(bookName)
                    if result is None or len(result) == 0:  # 数据库中不存在该图书
                        # 图书详情地址
                        bookUrl = bookTag["href"]
                        # 创建一个图书字典
                        book = dict()
                        book["type"] = type
                        book["url"] = bookUrl
                        book["itemname"] = bookName
                        # 爬取图书详情信息
                        self.getBookDetail(book)
                        # 控制爬取数量
                        bookCountTemp = bookCountTemp - 1
                        if bookCountTemp <= 0:
                            endFlag = True
                            break
                    else:
                        print("图书：%s  已存在数据库中！" % bookName)
                print("爬取图书类型：【%s" % type.get("typename") + "】第【" + str(currentPage) + "】页结束")
                if endFlag:
                    break
        except Exception as ex:
            print(ex)

    # 爬取图书详情信息
    def getBookDetail(self, book):
        try:
            print("爬取图书：" + book["itemname"] + "  开始")
            print("链接地址：" + book["url"])
            # 反爬虫技术，所以不能一直爬取，休息一会
            Util().getRandomSleep()
            # 爬取数据
            resp = requests.get(book["url"], headers=self.headers)
            # 解析html数据
            soup = BeautifulSoup(resp.text, "lxml")
            contentDiv = soup.find(id="content")
            # 图书图片
            imgDiv = contentDiv.find(id="mainpic").img
            imageUrl = imgDiv["src"]
            # 图书简介
            infoDiv = contentDiv.find(id="link-report")
            infoP = infoDiv.find("div",class_="intro").p
            content = infoP.get_text().strip()
            print("图片地址：" + imageUrl)
            print("图书简介：" + content)
            book["image"] = imageUrl
            book["content"] = content
            self.dbHelper.saveItem(book)
            print("爬取图书：" + book["itemname"] + "  结束")
        except Exception as ex:
            print(ex)
