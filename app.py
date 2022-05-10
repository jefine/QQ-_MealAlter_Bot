from flask import Flask, request
import random
import json
import requests
import re
import time


from paho.mqtt import client as mqtt_client


broker = '更换为自己或公用的MQTT服务器'
port = 1883
topic = "testtopic"
# generate client ID with pub prefix randomly
client_id = f'win_python-mqtt-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, msg):
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")




'下面这个函数用来判断信息开头的几个字是否为关键词'，用于过滤信息，判断是否执行

key = {"饭","领","餐","发"}
# 12345678 应该改为自己的QQ群的帐号
def keyword(message, uid, gid):
    if(gid==12345678 | gid==12345678):
        return
    message = str(message)
    for i in key:
        if (message.find(i)!=-1):
            send(uid, gid, message)
            return



def send(uid, gid, message):
    '''群消息'''
    message = str(message)
    # sign = {"&": "%26", "+": "%2B", "#": "%23"}
    # for i in sign:
    #     message = message.replace(i, sign[i])  # 防止在请求中特殊符号出现消息错误
    # if uid != 0:
    #     message = "[CQ:at,qq={}]\n".format(uid) + message  # CQ码，这里是at某人的作用
    #requests.get(
    #    url='http://127.0.0.1:10001/send_group_msg?group_id={0}&message={1}'.format(gid,
    #                                                                               message))  # 发送群消息的api，前面的地址保证和配置中的一致
    publish(client,message+"_"+str(uid)+"_"+str(gid))

app = Flask(__name__)

'''监听端口，获取QQ信息'''


@app.route('/', methods=["POST"])
def post_data():
    #修改就boom，无法发送Mqtt
    data = request.get_json()
    msg = str(data)
    if(msg.find("'interval': 5000")!=-1) :return "OK"
    print(data)
    if data['message_type'] == 'group':  # 如果是群聊信息
        gid = data['group_id']  # 获取群号
        uid = data['sender']['user_id']  # 获取信息发送者的 QQ号码
        message = data['raw_message']  # 获取原始信息
        print(message,uid,gid)
        #common.keyword(message, uid, gid)  # 将 Q号和原始信息传到我们的后台
        keyword(message,uid,gid)
    return 'OK'


if __name__ == '__main__':
    # 此处的 host和 port对应上面 yml文件的设置
    client = connect_mqtt()
    client.loop_start()
    app.run(host='127.0.0.1', port=10001)  # 保证和我们在配置里填的一致
