import os
import sys
import json
import requests
from flask import Flask, request

app = Flask(__name__)

senderMap = {}

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                  
                    final = dicto(message_text.lower())
                    
                    for x in final:
                        send_message(sender_id, x)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200
'''
def keywords(text):
    import http.client, urllib.request, urllib.parse, urllib.error, base64 #@UnusedImport
    import json
    
    log("finding key words from raw input")
  
    headers = {
        #Request headers
        'Ocp-Apim-Subscription-Key': '0bb5a4cf5f5646108c4ee0e9f6be339c',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    body = json.dumps(
        {
            "documents": [
                {
                    "language": "en",
                    "id": "1",
                    "text": text
                }
            ]
         })
    
    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com') #@UndefinedVariable
        conn.request("POST", "/text/analytics/v2.0/keyPhrases", body, headers)
        response = conn.getresponse()
        data = response.read().decxode("utf-8")
        dic = json.loads(data)
        return dic["documents"][0]["keyPhrases"]
        conn.close()
    except Exception as e:
        log("[Errno {0}] {1}".format(e.errno, e.strerror))
'''  
def dicto(msg):
    endGame = False
    global state
    keyword = msg
    if keyword == "":
        temp = msg.strip().split()
    else:
        temp = keyword.strip().split()
    
    msgList = []
    for x in temp:
        newWord = "".join([y for y in x if y != "!" or y != "?"])
        msgList.append(newWord)
      
    response = ""
    dicWord = [
        ["hi", "hello", "hey","what's","sup","yo", "whatsup", "whats"],
        ["yes", "yeap", "sure", "go", "start", "begin","yep","yup","sure","mhm","yeah","yea"],
        ["suspects", "choices", "people", "suspects", "who", "guys"], 
        ["about", "background", "yourself", "yourselves", "introduce","backgrounds","introduction","introductions"],
        ["scene", "see", "witness", "crime", "statement"],
        ["alibi", "reason", "excuse", "doing", "testament","testaments","excuses","reasons","alibis"],
        ["decision", "made", "mind", "answer", "ready","decided"],
        ["joanna", "jack", "john", "killer", "murdered", "culprit", "bad"]
      ]
    
    dicReply = [
        ["Welcome to InvestiChat, where you will be taking part in a murder mystery.",
         "If you made your decision at any point during this chat, please say so and you'll be prompted for your answer.",
         "Now, shall we start?"],
        ["Detective, currently we are investigating the murder of a Dr. Jones, who was found dead in his home.",
         "So far we have identified a possible items of interest, specifically a bloody golf club, and a strip of cotton fabric. However, No fingerprints have been found.",
         "We too have three suspects: John, Jack, and Joanna. All three are ready to introduce themselves.", "Throughout the investigation you can ask the suspects questions such as who they are/their backgrounds, why they were at the crime scene, and their alibi. Tell us when you are ready, and you can choose the murderer at the end."],
        ["John: Hello there, how may I help you?",
         "Jack: waddup officer, whats all this big talk about", 
         "Joanna: Yes? What is wrong?"],
        ["John: Well I'm a research professor, studying polymer chemistry. I am thirty-six years old and one of Dr. Jones' good friends.",
         "Jack: Hey man, I'm just an average dude, working in construction man. I have mad respect for Dr. Jones; he was my niece's prof. That dude was smart man.", 
         "Joanna: We were friends and neighbours. This is just heart-breaking"],
        ["John: Dr. Jones and I were working on a research project you see, and I was going to visit him to discuss about pressing matters in our recent discovery when I stumbled across his dead body", 
         "Jack: I was strollin' in the neighborhood, and I noticed some weird stuff. Dr. Jones' front door was open, so I walked in. Shit man, there he was, like dead and all.", 
         "Joanna: I was at home preparing dinner when I heard the sound of a gunshot, so I went over to check if everything was okay."],
        ["John: Just as I entered his house, I saw a person in a hoodie running away from the general direction. What was perculiar was that that persona looked surprisingly like Jack, the neighbourhood's local gardener",
         "Jack: Hey man, I mean no harm towards no one, but dang, when I got close you know who I saw walking out? Prof John from the uni, with his shiny raincoat and all coming out",
         "Joanna: I was so terrified when I saw John, the kindly old professor menacingly walking out of the door! I was so shocked and scared, who would've known that he could do such a thing!"],
        ["Welcome back to the real world, detective. Please tell us who you think is the killer."],
        ""
      ]
      
    for i,v in enumerate(dicWord):
        breakAll = False
        for x in msgList:
            if x in v:
                response = dicReply[i]
                breakAll = True
                if i == len(dicWord) - 1:
                    endGame = True
                break
        if breakAll:
            break
            
    if response != "":
        if "john" in msg:
            response = [response[0]]
        elif "jack" in msg:
            response = [response[1]]
        elif "joanna" in msg:
            response = [response[2]]
    elif response == "" and ("jack" in msg or "john" in msg or "joanna" in msg):
        response = [
            "John: Pardon me?",
            "Jack: Huh?",
            "Joanna: Come again?"
        ]
        if "john" in msg:
            response = [response[0]]
        elif "jack" in msg:
            response = [response[1]]
        elif "joanna" in msg:
            response = [response[2]]
      
    if endGame:
        count = 0
        answer = ""
        for name in ["john", "jack", "joanna"]:
            if name in msg:
                answer = name.capitalize()
                count += 1
        if 0 < count < 2:
            stats(answer)
            return ["Thanks for playing!"]
        else:
            return ["That wasn't an acceptable decision, who do you think was the killer?"] 
      
    if response == "":
        return ["Sorry I didn't really understand what you said..."]
    else:
        return response

def stats(name):
    pass
  
def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.8/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


        
def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

    
  



if __name__ == '__main__':
    app.run(debug=True)
    
    
