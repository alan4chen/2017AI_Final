#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import logging
from datetime import datetime

import requests
from flask import Flask, request
from indicator_predictor.indicator_similarity_predictor import handler
from news_predictor.IR import ir_predictor

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAANa6oMiTBgBAHBWq4T1oB2Ejhh7HIaH5IWxZCvUZCxg1djsid95QDpC5ec3NqsNpZCi0ZBC8quE2idX0RcJhLtl2AfFJASZBBe2PwrKurZArxAkstYkAyIgkTFGOExhXhFCEZBPatpkg3KCVZAhdhBOqvLuLiMU11EGtsMdNIZAa1x9T9ypNfZAZCO"
VERIFY_TOKEN = "foo"

usersRegister = {}
stockMapping = {2427:"https://www.facebook.com/TStockR/photos/a.1533746516741083.1073741828.1529609040488164/1533746556741079/?type=3&theater",
                2453:"https://www.facebook.com/TStockR/photos/a.1533746516741083.1073741828.1529609040488164/1533746556741079/?type=3&theater",
                2468:"https://www.facebook.com/TStockR/photos/a.1533746516741083.1073741828.1529609040488164/1533746556741079/?type=3&theater",
                2471:"https://www.facebook.com/TStockR/photos/a.1533746516741083.1073741828.1529609040488164/1533746556741079/?type=3&theater",
                2480:"https://www.facebook.com/TStockR/photos/a.1533746516741083.1073741828.1529609040488164/1533746556741079/?type=3&theater",
                3029:"https://www.facebook.com/TStockR/photos/a.1533746516741083.1073741828.1529609040488164/1533746556741079/?type=3&theater",
                3130:"https://www.facebook.com/TStockR/photos/a.1533746516741083.1073741828.1529609040488164/1533746556741079/?type=3&theater",
                4994:"https://www.facebook.com/TStockR/photos/a.1533746516741083.1073741828.1529609040488164/1533746556741079/?type=3&theater",
                5203:"https://www.facebook.com/TStockR/photos/a.1533746516741083.1073741828.1529609040488164/1533746556741079/?type=3&theater",
                6112:"https://www.facebook.com/TStockR/photos/a.1533746516741083.1073741828.1529609040488164/1533746556741079/?type=3&theater",
                6183:"https://www.facebook.com/TStockR/photos/a.1533746516741083.1073741828.1529609040488164/1533746556741079/?type=3&theater",
                6214:"https://www.facebook.com/TStockR/photos/a.1533746516741083.1073741828.1529609040488164/1533746556741079/?type=3&theater",
                }

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    global usersRegister

    # endpoint for processing incoming messaging events

    data = request.get_json()
    logging.info("__________ New Request __________")
    logging.debug("Received: {}".format(data))

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message
                    sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    logging.info("receive message from {}".format(sender_id))

                    if not messaging_event["message"].get("text"):
                        logging.info("Status: Message does not contain text, unable to handle the message!")

                        replied_text = 'Hi~ 我是股市小精靈，請輸入"你好"來開始對話喔！我現在可以用指數或是新聞來幫您分析股票喔！'
                        send_message(sender_id, replied_text, "simple")

                        return "ok", 200

                    message_text = messaging_event["message"]["text"]  # the message's text

                    if sender_id not in usersRegister and message_text == "你好":
                        # User say hello and start a new conversation
                        logging.info("Status: New User wants to start a conversation!")

                        usersRegister = {sender_id: "0"}
                        replied_text = "您好～ 請選擇下列兩種分析方式："
                        send_message(sender_id, replied_text, "choice")

                    elif sender_id not in usersRegister and message_text != "你好":
                        # User say did not start a conversation, reply usage
                        logging.info("Status: New User does not start a conversation!")

                        replied_text = 'Hi~ 我是股市小精靈，請輸入"你好"來開始對話喔！我現在可以用指數或是新聞來幫您分析股票喔！'
                        send_message(sender_id, replied_text, "simple")

                    elif usersRegister[sender_id] == "1":
                        logging.info("Status: Handle query with Indicator method!")

                        stockID, replied_text = handler(message_text)
                        send_message(sender_id, replied_text, "simple")

                        # show stock pic
                        if stockID != 0:
                            send_message(sender_id, stockID, "stock")

                        # asked for rating
                        send_message(sender_id, "喜歡我們的服務嗎？請幫我們評分：", "rating")

                        usersRegister[sender_id] = "3"

                    elif usersRegister[sender_id] == "2":

                        logging.info("Status: Handle query with Retrieval method!")
                        stockID, replied_text = ir_predictor(message_text)
                        send_message(sender_id, replied_text, "simple")

                        # show stock pic
                        if stockID != 0:
                            send_message(sender_id, stockID, "stock")

                        # asked for rating
                        send_message(sender_id, "喜歡我們的服務嗎？請幫我們評分：", "rating")

                        usersRegister[sender_id] = "3"

                    elif usersRegister[sender_id] == "3":
                        del usersRegister[sender_id]

                        logging.info("Status: Handle user's rating! ")
                        if messaging_event["message"].get("quick_reply"):
                            payload = messaging_event["message"]["quick_reply"]["payload"]
                            logging.info("{} rates {}!".format(sender_id, payload))

                        send_message(sender_id, "已收到您的回覆！ 謝謝！", "simple")

                        # # receive rating
                        # if messaging_event["message"].get("quick_reply"):
                        #     payload = messaging_event["message"]["quick_reply"]["payload"]
                        #     if payload == "5s":
                        #         send_message(sender_id, "已收到您的回覆！ 謝謝！", "simple")
                        #     elif payload == "4s":
                        #         send_message(sender_id, "已收到您的回覆！ 謝謝！", "simple")
                        #     elif payload == "3s":
                        #         send_message(sender_id, "已收到您的回覆！ 謝謝！", "simple")
                        #     elif payload == "2s":
                        #         send_message(sender_id, "已收到您的回覆！ 謝謝！", "simple")
                        #     elif payload == "1s":
                        #         send_message(sender_id, "已收到您的回覆！ 謝謝！", "simple")
                        #     else:
                        #         pass

                    else:
                        # handle quick response
                        if messaging_event["message"].get("quick_reply"):
                            payload = messaging_event["message"]["quick_reply"]["payload"]
                            if payload == "1":
                                logging.info("Status: User {} chose Indicator Method!".format(sender_id))
                                usersRegister[sender_id] = "1"
                                replied_text = "您選擇了指標分析方法，請輸入查詢內容："
                                send_message(sender_id, replied_text, "simple")

                            elif payload == "2":
                                logging.info("Status: User {} chose Retrial Method!".format(sender_id))
                                usersRegister[sender_id] = "2"
                                replied_text = "您選擇了新聞分析方法，請輸入查詢內容："
                                send_message(sender_id, replied_text, "simple")
                            else:
                                pass
                        else:
                            logging.info("Status: User {} did not choose a method!".format(sender_id))
                            usersRegister[sender_id]  = "0"
                            replied_text = "請再次選擇下列兩種分析方式："
                            send_message(sender_id, replied_text, "choice")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text, action="simple"):

    logging.debug("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    if action == "choice":
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message":{
                "text": message_text,
                "quick_replies":[
                  {
                    "content_type":"text",
                    "title":"指標分析",
                    "payload":"1"
                  },
                  {
                    "content_type":"text",
                    "title":"新聞分析",
                    "payload":"2"
                  }
                ]
            }
        })
    elif action == "rating":
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message":{
                "text": message_text,
                "quick_replies":[
                  {
                    "content_type":"text",
                    "title":"5★",
                    "payload":"5s"
                  },
                  {
                    "content_type":"text",
                    "title":"4★",
                    "payload":"4s"
                  },
                  {
                    "content_type":"text",
                    "title":"3★",
                    "payload":"3s"
                  },
                  {
                    "content_type":"text",
                    "title":"2★",
                    "payload":"2s"
                  },
                  {
                    "content_type":"text",
                    "title":"1★",
                    "payload":"1s"
                  }
                ]
            }
        })
    elif action == "simple":
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
        })
    elif action == "stock":
        global stockMapping
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "media",
                        "elements": [
                            {
                                "media_type": "image",
                                "url": stockMapping[message_text]
                            }
                        ]
                    }
                }
            }
        })
    else:
        pass

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

    if r.status_code != 200:
        logging.error("Return Error Code: {}, Info: {}".format(r.status_code, r.text))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.basicConfig(filename='server.log', level=logging.INFO)

    app.run(host = '0.0.0.0', port = 80, debug=True)
