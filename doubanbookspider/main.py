from doubanbookspider.bookspider import BookSpider

bookCount = 2  # 每种图书类型下爬取的图书数量，排查已经爬取的图书
imagePath = "D:\\Files\\project\\SimpleOnlineBookCFRSPython1.0\\SimpleOnlineBookCFRSPython1.0" \
            "\\SimpleOnlineBookCFRSPython\\media\\"  # 图书图片保存地址
# 实例化爬虫对象
spider = BookSpider(bookCount, imagePath)
spider.catchData()
