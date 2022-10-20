import json, api, re


match_map = api.get_match_map()


def unknown_event(data):
    pass
    
def default():
    pass

def flow_deal(data, command:str, flow):
    for obj in flow:
        key = obj['key']
        #进行正则匹配
        if obj['match'] == 'reg':
            #正则表达式匹配
            match_obj = re.match(key, command, re.M|re.I)
            #如果成功
            if match_obj:
                #调用函数
                #obj['function']为函数名
                obj['function'](data, command)
                if obj['block']:
                    break
                else:
                    continue
        #进行完全匹配
        if obj['match'] == 'uni' and command == key:
            obj['function'](data, command)
            if obj['block']:
                break
            else:
                continue
        #进行前缀匹配
        if obj['match'] == 'pre' and command.startswith(key):
            obj['function'](data, command)
            if obj['block']:
                break
            else:
                continue
        #进行模糊匹配
        if obj['match'] == 'inc' and key in command:
            obj['function'](data, command)
            if obj['block']:
                break
            else:
                continue
    return

def private_event(data):
    msg = str(data['message'])
    #循环匹配
    flow_deal(data, msg, match_map['private_message'])
    return

def group_event(data):
    msg = str(data['message'])
    #循环匹配
    flow_deal(data, msg, match_map['group_message'])
    return

def poke_event(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['poke_event'])
    return

def lucky_king_event(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['lucky_king_event'])
    return

def honor_event(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['honor_event'])
    return

def group_upload_event(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['group_upload'])
    return
    
def group_admin_event(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['group_admin'])
    return

def group_increase_event(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['group_increase'])
    return
    
def group_decrease_event(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['group_decrease'])
    return

def group_ban(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['group_ban'])
    return

def friend_add(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['friend_add'])
    return

def group_recall(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['group_recall'])
    return

def friend_recall(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['friend_recall'])
    return

def group_card(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['group_card'])
    return

def offline_file(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['offline_file'])
    return

def client_status(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['client_status'])
    return
    
def friend_request(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['friend_request'])
    return
    
def group_request(data):
    msg = 'event'
    #循环匹配
    flow_deal(data, msg, match_map['group_request'])
    return

def match_process(ori_data):
    if ori_data:
        data = json.loads(ori_data)
        if data['post_type'] == 'notice':
            if data['notice_type'] == 'notify':
                if data['sub_type'] == 'poke':
                    #戳一戳事件
                    poke_event(data)
                elif data['sub_type'] == 'lucky_king':
                    #运气王事件
                    lucky_king_event(data)
                elif data['sub_type'] == 'honor':
                    #群荣耀变化事件
                    honor_event(data)
                else:
                    unknown_event(data)
            elif data['notice_type'] == 'group_upload':
                #群文件上传事件
                group_upload_event(data)
            elif data['notice_type'] == 'group_admin':
                #群管理变动事件
                group_admin_event(data)
            elif data['notice_type'] == 'group_increase':
                #群成员增加事件
                group_increase_event(data)
            elif data['notice_type'] == 'group_decrease':
                #群成员减少事件
                group_decrease_event(data)
            elif data['notice_type'] == 'group_ban':
                #群成员禁言事件
                group_ban(data)
            elif data['notice_type'] == 'friend_add':
                #好友添加事件
                friend_add(data)
            elif data['notice_type'] == 'group_recall':
                #群撤回事件
                group_recall(data)
            elif data['notice_type'] == 'friend_recall':
                #好友撤回事件
                friend_recall(data)
            elif data['notice_type'] == 'group_card':
                #群成员名片更新
                group_card(data)
            elif data['notice_type'] == 'offline_file':
                #接收到离线文件
                offline_file(data)
            elif data['notice_type'] == 'client_status':
                #客户端状态改变
                client_status(data)
            else:
                unknown_event(data)
        elif data['post_type'] == 'request':
            if data['request_type'] == 'friend':
                #好友添加请求
                friend_request(data)
            elif data['request_type'] == 'group':
                #群添加请求
                group_request(data)
            else:
                unknown_event(data)
        elif data['post_type'] == 'message':
            if data['message_type'] == 'private':
                #私聊消息
                private_event(data)
            elif data['message_type'] == 'group':
                #群聊消息
                group_event(data)
            else:
                unknown_event(data)
        else:
            unknown_event(data)
    return