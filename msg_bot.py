import telebot
import requests
import datetime

url = 'https://bookingform.communitytest.gov.hk/form/api_center'
data = {'center_id':'22'}
headers = {
    #'Accept: '*/*'
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '12',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'bookingform.communitytest.gov.hk',
    'Origin': 'https://booking.communitytest.gov.hk',
    'Referer': 'https://booking.communitytest.gov.hk/',
    #'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"'
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'sec-Fetch-Dest': 'empty',
    'sec-Fetch-Mode': 'cors',
    'sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}

def send_time_slots():
    response = requests.post(url,data=data)
    timeslots_msg = ''
    if response.status_code == 200 and response.json() != None:
        timeslots_msgs = print_time_slots(response)
    else:
        timeslots_msgs = ['\nSystem Error!']
    return timeslots_msgs

def print_time_slots(response):
    avalible_timeslots = response.json()['avalible_timeslots']
    timeslots_msgs = []

    for avalible_timeslot in avalible_timeslots:
        timeslots_msg = '\n' + avalible_timeslot['date'] + ':\n'

        avalible_day = 0
        for timeslot in avalible_timeslot['timeslots']:
            if timeslot['value'] == 1:
                timeslots_msg = timeslots_msg + '            ' +timeslot['display_label']
                avalible_day = 1
        if avalible_day == 0:
            timeslots_msg = timeslots_msg + '\nThis day is no avalible timeslot.\n'
        timeslots_msgs.append(timeslots_msg)
    return timeslots_msgs

bot = telebot.TeleBot('5133395491:AAGONhybrF_XR3DscEDBRLUuegSRVGsHaQo', parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    timeslots_msgs = send_time_slots()
    for timeslots_msg in timeslots_msgs:
        bot.reply_to(message, timeslots_msg)

bot.infinity_polling()