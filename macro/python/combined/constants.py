import base64

def decode(encoded):
    return base64.b64decode(encoded).decode('utf-8')

# write your id and password in base64 format
CREDENTIALS = {
    "bananamall": {
        "id": decode(""),
        "password": decode(""),
        "login_url": "https://www.bananamall.co.kr/etc/attendance.php?cl=attendance",
        "attendance_url": "https://www.bananamall.co.kr/etc/attendance.php?cl=attendance",
    },
    "dingdong": {
        "id": decode(""),
        "password": decode(""),
        "login_url": "https://www.dingdong.co.kr/member/login.html",
        "attendance_url": "https://www.dingdong.co.kr/attend/stamp.html",
    },
    "domaedoll": {
        "id": decode(""),
        "password": decode(""),
        "login_url": "https://domaedoll.com/member/login.html",
        "attendance_url": "https://domaedoll.com/attend/stamp.html",
    },
    "oname": {
        "id": decode(""),
        "password": decode(""),
        "login_url": "https://oname.kr/member/login.html",
        "attendance_url": "https://m.oname.kr/attend/stamp2.html",
    },
    "showdang": {
        "id": decode(""),
        "password": decode(""),
        "login_url": "https://www.showdang.co.kr/member/login.php",
        "attendance_url": "https://showdang.co.kr/event/attend_stamp.php",
    },
    "sofrano": {
        "id": decode(""),
        "password": decode(""),
        "login_url": "https://sofrano.com/member/login.html",
        "attendance_url": "https://sofrano.com/attend/stamp.html",
    },
    "shoemarker": {
        "id": decode(""),
        "password": decode(""),
        "login_url": "https://www.shoemarker.co.kr/ASP/Member/Login.asp",
        "attendance_url": "https://www.shoemarker.co.kr/ASP/Event/EventAttend_New.asp",
        "main_url": "https://www.shoemarker.co.kr/"
    },
    "herotime": {
        "id": decode(""),
        "password": decode(""),
        "login_url": "https://herotime.co.kr/member/login.html",
        "attendance_url": "https://herotime.co.kr/attend/stamp.html"
    }
}

# write your slack webhook url
# you can get it from https://api.slack.com/messaging/webhooks
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXX"
TRY_COUNT = 2