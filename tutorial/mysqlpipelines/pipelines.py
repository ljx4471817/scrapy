from twisted.internet.threads import deferToThread
from tutorial.items import *
from .__init__ import *

class TutorialPipeline(object):



    def process_item(self, item, spider):
        if isinstance(item, DingdianItem):
            name_id = item['name_id']
            ret = select_name(name_id) #strap是异步下载,可能下载重复
            if ret:
                print('开始插入')
                insert(item)
            else:
                print('已经存在了')
                pass
        print('全部下载成功!')

        # 导入2类相关数据时,需要执行下方类似语句
        # if isinstance(item, DcontentItem):
        #     url = item['chapterurl']
        #     name_id = item['id_name']
        #     num_id = item['num']
        #     xs_chaptername = item['chaptername']
        #     xs_content = item['chaptercontent']
        #     Sql.insert_dd_chaptername(xs_chaptername, xs_content, name_id, num_id, url)
        #     print('小说存储完毕')
        #     return item