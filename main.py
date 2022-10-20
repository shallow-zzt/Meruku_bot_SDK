from sys import path
#导入独立包路径
path.append('.\\Lib')
import websockets
import asyncio
import threading, configparser
import json
from multiprocessing import Process, Pipe
from importlib import import_module
import time

def get_ws_uri():
    config = configparser.ConfigParser()
    config.read("./config.ini")
    secs = config.sections()
    if "QQ_config" not in secs:
        #添加不存在的配置节并初始化
        config.add_section("QQ_config")
        config.set("QQ_config", "ws_uri", "ws://127.0.0.1:5700")
        f = open('./config.ini', 'w')
        config.write(f)
        f.close()

    opt = config.options("QQ_config")
    if "ws_uri" not in opt:
        config.set("QQ_config", "ws_uri", "ws://127.0.0.1:5700")
    ws_uri = config.get("QQ_config", "ws_uri")
    return ws_uri

async def async_processing(conn_queu):
    async with websockets.connect(get_ws_uri()) as websocket:
        while True:
            try:
                message = await websocket.recv()
                #将接受到的信息异步的送入消息匹配流程中
                conn_queu.send(message)
                
            except websockets.ConnectionClosed:
                print('ConnectionClosed')
                break

def get_conn(conn_queu):
    loop =  asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_processing(conn_queu))
    return



def process_main():
    mapping_flow = import_module('mapping_flow')
    conn_queue, msg_queue = Pipe()
    conn_process = Process(target=get_conn, args=(conn_queue,))
    conn_process.start()
    print('--------------------------------------------------------------------------------')
    while True:
        msg =  msg_queue.recv()
        msg2 =  json.loads(msg)
        msg_type = msg2['post_type']
        if msg_type=='message':
            raw_message = str(msg2['raw_message'])
            user_id = str(msg2['user_id'])
            msg_time = time.localtime(msg2['time'])
            msg_time = time.strftime("%Y-%m-%d %H:%M:%S",msg_time)
            username = str(msg2['sender']['nickname'])
            if 'group_id' in msg2:
                group = str(msg2['group_id'])
            else:
                group = 'private'
            #print(msg2)
            print('[INFO]['+group+'] '+username+'('+user_id+') '+msg_time)
            print(raw_message)
            print('--------------------------------------------------------------------------------')
        match_loop = threading.Thread(target = mapping_flow.match_process, args = [msg])
        match_loop.start()
 
 
 
if __name__ == '__main__':
    process_main()
