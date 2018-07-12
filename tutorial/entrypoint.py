from scrapy.cmdline import execute

#相当于在当前目录的命令行中执行:scrapy crawl Dingdian
#参数 Dingdian 是spiders.Dingdia.py中定义的name
execute(['scrapy', 'crawl', 'Dingdian'])