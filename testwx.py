# -- coding: utf-8 --
import requests
import json
import datetime
import time


def sleeptime(hour,min,sec):
    return hour*3600 + min*60 + sec;
second = sleeptime(0,30,0);

def get_access_token():
    """
    获取微信全局接口的凭证(默认有效期俩个小时)
    如果不每天请求次数过多, 通过设置缓存即可
    """
    result = requests.get(
        url="https://api.weixin.qq.com/cgi-bin/token",
        params={
            "grant_type": "client_credential",
            "appid": "wx6ec0fd7a3ebe1bd5",
            "secret": "fa48630f7473044b648a5cd18d2e4b0e",
        }
    ).json()

    if result.get("access_token"):
        access_token = result.get('access_token')
    else:
        access_token = None
    return access_token

def sendmsg(openid,msg):

    access_token = get_access_token()



    body = {
        "touser": openid,
        #text消息回复类型
        "msgtype": "text",
        "text": {
            "content": msg
        }
        # "url":"www.caiyunapp.com/map",
        # "template_id":"zA72bQ4hCs5cZ-DKZ12IlXVx0J8s2wN0U1AvHIgO6zs",#模板ID

        # "data": {
        #     "weather": {
        #         "value":msg,
        #         "color":"#173177"
        #     }
        # }
    }

    response = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
        params={
            'access_token': access_token
        },
        data=bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8')
    )
    # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
    result = response.json()
    print(result)

#获取天气API数据
while True:
    # 彩云天气API
    json_text = requests.get(str.format("https://api.caiyunapp.com/v2/OQbKoLnm5O0VkY8C/118.808702,32.102147/forecast.json")).content
    self_realtime_data = json.loads(json_text)
    # 天气API
    json_text = requests.get("https://www.tianqiapi.com/api/?version=v6&cityid=101190101", params={'appid':'22668592' ,'appsecret':'Iwn2beZW'}).content
    # 取出天气API json格式里的部分数据
    data = json.loads(json_text)
    cityid=data['cityid']
    city=data['city']
    date=data['date']
    utime=data['update_time']
    week=data['week']
    wea=data['wea']
    h_tem=data['tem1']
    l_tem=data['tem2']
    n_tem=data['tem']
    win=data['win']
    win_speed=data['win_speed']
    win_meter=data['win_meter']
    hum=data['humidity']
    visit=data['visibility']
    pressure=data['pressure']
    air=data['air']
    pm25=data['air_pm25']
    air_level=data['air_level']
    air_tips=data['air_tips']
    alarm=data['alarm']['alarm_content']
    alarm_type=data['alarm']['alarm_type']
    alarm_level=data['alarm']['alarm_level']
    # print(data)
    # 取出彩云天气json里的指定数据
    now_data=self_realtime_data['result']['minutely']['description']
    now1_data=self_realtime_data['result']['hourly']['description']
    print ("降雨预报："+now_data)
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print ("更新于："+nowTime)
    now2_data="\n城市："+city+"\n天气："+wea+"  "+n_tem+"℃\n最高/低温："+h_tem+"℃ /"+l_tem+"℃\n湿度："+hum+"\n"+win+"  "+win_speed+"  "+win_meter+"\n能见度："+visit+"\n空气质量："+air+"  "+air_level+"  "+air_tips+"\npm2.5："+pm25+"\n预警消息："+alarm+"\n数据来源：彩云科技、中国天气网"
    print(now2_data)
    send_data="降雨预报：\n"+now_data+"\n\n天气预报：\n"+now1_data+now2_data+"\n\n更新于："+nowTime
    # send_data="降雨预报：\n"+now_data+"\n\n天气预报：\n"+now1_data+"\n\n更新于："+nowTime

    if __name__ == '__main__':
        sendmsg('oLV7xs3MNo1HHhbuzd_J2YR-pePc',send_data) #用户ID  
        # sendmsg('oLV7xszi0ZHJfP1RhAYAnpJ638oQ',send_data)
    time.sleep(second);