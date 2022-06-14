import requests

token = 'ODIyODI0MzkyNTc1OTQyNjU2.GVJSm8.Am2_tgQagRiQFWAhl2X_w1UpxHHQoYSTPEzv1I'
channel_id = 986276615849926668

def sendMessage(token, channel_id, message):

    url = 'https://discord.com/api/v9/channels/{}/messages'.format(channel_id)
    data = {'content': message}
    header = {'authorization': token}


    r = requests.post(url, data=data, headers=header)
    print(r.status_code)

#print(len(token))
sendMessage(token, channel_id, ';-; за съжаление няма да мога')