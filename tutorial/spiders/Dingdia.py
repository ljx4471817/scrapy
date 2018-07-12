import scrapy
import re
from scrapy.http import Request
from tutorial.mysqlpipelines.__init__ import close_connect
from bs4 import BeautifulSoup
from tutorial.items import DingdianItem

class DingdiaSpider(scrapy.Spider):
    name='Dingdian' # 唯一,这只蜘蛛的名字
    allowed_domains = ['x23us.com'] #爬取的范围
    bash_url = 'https://www.x23us.com/class/'
    bashurl='.html'
    def start_requests(self):
        for i in range(1,11):
            url = self.bash_url+str(i)+'_1'+self.bashurl # 拼接各类小说的下载地址
            #解析一级目录地址
            print(help(Request))
            yield Request(url,self.parse)
        #yield Request('http://www.x23us.com/quanben/1', self.parse)#全本小说地址,格式与上述不一,独立出来写

    def parse(self, response):
        max_num = BeautifulSoup(response.text, 'lxml').find_all(class_='last')[0].text #每类小说的最大页数
        if str(response.url).startswith('https://www.x23us.com/class'):
            bashurl = str(response.url)[:-7]
            for num in range(1,int(max_num)+1):
                url = bashurl+'_'+str(num)+self.bashurl
                # 解析二级目录地址,提取目标内容
                yield Request(url,callback=self.get_name)
        else:
            # 全本小说的地址
            bashurl =str(response.url)[:-1]
            #for num
    #获得小说名及简介地址
    def get_name(self,response):
        tds = BeautifulSoup(response.text, 'lxml').find_all(bgcolor="#FFFFFF")
        for i in tds:
            novelname=i.find_all('a')[1].get_text()#小说名
            novelurl=i.find('a')['href']#小说简介页面
            yield Request(novelurl,callback=self.getchapterurl,meta={'name':novelname,'url':novelurl})
    #获得目标数据
    def getchapterurl(self,response):
        html=BeautifulSoup(response.text,'lxml')#页面源码
        item=DingdianItem()
        item['name']=str(response.meta['name'])#小说名
        item['novelurl']=response.meta['url']#小说简介页面地址
        item['category'] = html.find(bgcolor="#E4E4E4").find('a').text #小说种类
        author=html.find(bgcolor="#E4E4E4").find_all('td')[1].text #作者
        item['author'] = str(author).replace('\xa0','') #作者
        bash_url = html.find(class_="read")['href'] #小说章节页面地址
        item['serialurl']=bash_url #小说地址
        item['name_id']=str(bash_url)[-6:-1].replace('/','') #小说编号
        item['serialstatus']=re.findall('<th>文章状态</th><td>&nbsp;(.*?)</td>',response.text)[0]#连载状态
        item['serialnumber']=re.findall('<th>全文长度</th><td>&nbsp;(.*?)</td>',response.text)[0]#全文长度
        return item #出现return item后,自动运行pipelines

    # 导入2类相关数据时,需要执行下方类似语句
    #     yield item
    #     yield Request(url=bash_url, callback=self.get_chapter, meta={'name_id': name_id})
    #
    # def get_chapter(self, response):
    #     urls = re.findall(r'<td class="L"><a href="(.*?)">(.*?)</a></td>', response.text)
    #     num = 0
    #     for url in urls:
    #         num = num + 1
    #         chapterurl = response.url + url[0]
    #         chaptername = url[1]
    #         rets = Sql.sclect_chapter(chapterurl)
    #         if rets[0] == 1:
    #             print('章节已经存在了')
    #             return False
    #         else:
    #             yield Request(chapterurl, callback=self.get_chaptercontent, meta={'num': num,
    #                                                                               'name_id': response.meta['name_id'],
    #                                                                               'chaptername': chaptername,
    #                                                                               'chapterurl': chapterurl
    #                                                                               })
    # def get_chaptercontent(self, response):
    #     item = DcontentItem()
    #     item['num'] = response.meta['num']
    #     item['id_name'] = response.meta['name_id']
    #     item['chaptername'] = str(response.meta['chaptername']).replace('\xa0', '')
    #     item['chapterurl'] = response.meta['chapterurl']
    #     content = BeautifulSoup(response.text, 'lxml').find('dd', id='contents').get_text()
    #     item['chaptercontent'] = str(content).replace('\xa0', '')
    #     yield item
