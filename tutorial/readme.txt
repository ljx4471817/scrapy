零.安装srayp.
1.(未尝试)小白进阶之Scrapy第一篇 https://cuiqingcai.com/3472.html:
2.Pycharm中的scrapy安装教程 https://www.cnblogs.com/xiaoli2018/p/4566639.html,不需安装环境变量
3.Python3安装Scrapy的方法步骤,https://www.jb51.net/article/128885.htm,如果pycharm和原始的idel没有共用模块包( .\Python36\Lib\site-packages) ,可把原生site-packages中的模块复制到pycharm中

一.新建srapy项目:
1.CMD进入你需要放置项目的目录
2.scrapy startproject XXXXX             XXXXX代表你项目的名字

二.在items.py中,建立目标内容

三.在spiders包下建立爬虫主程序.'Dinddia.py',并编写相关爬虫代码.将目标内容提取存放在items中
tips1:
大多时候items中的目标内容并不在一个页面中,
所以使用from scrapy.http import Request 中的Request,使用yield Request(url,callback,meta={'key1':value1,'key2':value2})进行转发,即改变爬虫的爬取页面.
Request参数解释:
url:爬虫将爬取的地址
callback:回调函数,Request可自动获取resopnse并返回给回调函数.除第一个到parse之外,再次转发时可自定义回调函数,例:def 函数名XX(self,response):
meta:可存储需要的数据到下个页面中使用
tips2:因为items中的实体类继承了scrapy.Item. 所以return 或yield items时,自动将items数据传输到pipelines中!

四.将数据存储到数据库中
ps:需先在settings中指定使用的pipelines,详见settings
1.提前在数据库中创建库和表
2.在def process_item(self, item, spider):方法中执行python 连接数据库的操作.
3.数据库的初始连接和增删改查方法,我是放在了pipeline的init中,没有关闭方法,因为目前尝试的位置都会影响写入.不关闭目前看来也没什么影响.
