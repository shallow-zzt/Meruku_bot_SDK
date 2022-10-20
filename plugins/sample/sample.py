import sqlite3
import re
import api
import time,datetime
from importlib import import_module

class test_class:
    #用于回复内容的函数只需要两个变量data和message
    #data为完整信息的字典，message为触发指令时回复的消息
    #推荐使用split函数来分割回复消息的内容，形成多个参数
    def test(data, message):
        #获取data中的发送者信息并发送
        api.MsgUser(data).send('success')
        return
    def poke(data, message):
        api.MsgUser(data).send('不许戳我，痛死了')
        return
        
class batch_class:
    #发送合并消息示例，使用batch_send发送
    #待发送信息应为列表格式
    def test(data, message):
        #获取data中的发送者信息并发送
        test_list=['我叫绿艾','我可是在艾原采药的小女孩呢','听说幽若之海有人在呼唤我……','我想知道这是不是真的','今天的我很高兴哪']
        api.MsgUser(data).batch_send(test_list)
        return

class auto_class:
    #周期检测事件
    #推荐使用while True和time.sleep（）实现周期性检测
    def test():
        while True:
            #周期检测事件，使用auto_send_msg发送消息，需要指定群号或qq号
            api = import_module('api')
            x = datetime.datetime.now()
            api.auto_send_msg(str(x), qq=1609259939)
            time.sleep(600)
        return

class plugin_load:
    #关键词触发事件使用函数api.match_update()
    #msg_type为匹配方式，详情见api.py中match_map中预设type名称
    #fun触发指令后，待执行函数
    
    #以下参数，若事件类型非私聊或群聊消息，请不要写
    #key为关键词，根据关键词和匹配类型决定是否触发
    #match为匹配类型，正则reg，完全uni，前缀pre，模糊inc，默认完全uni
    #priority为优先级，数值越小越优先，默认为0
    #block为是否阻塞，为True会在匹配关键词后，中断该回复后续关键词匹配，默认为True
    #非私聊或群聊消息强制为False
    
    #周期性事件使用auto_event(),开启额外线程
    def __init__(self):
        api.match_update(msg_type='private_message', fun=test_class.test, key='test', match='uni')
        api.match_update(msg_type='group_message', fun=test_class.test, key='test', match='uni')
        api.match_update(msg_type='private_message', fun=batch_class.test, key='test2', match='uni')
        api.match_update(msg_type='group_message', fun=batch_class.test, key='test2', match='uni')
        api.match_update(msg_type='poke_event', fun=test_class.poke)
        api.auto_event(fun=auto_class.test)
        return

if __name__ != "__main__":
    plugin_load()