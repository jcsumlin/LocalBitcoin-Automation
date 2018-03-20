# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 17:05:36 2018

@author: Chat
"""
import LocalBitcoin
import time
import json


username = "J_C"
contact_id = 0
hmac_auth_key = "94fc97dc37a122753dc9fd3d460e2b90"
hmac_auth_secret = "0a9423f2cb1fcb45dd98a1590cb41f33b3b7f72ac82a2dfe8ebefdb000bef57f"


lc = LocalBitcoin.LocalBitcoin(hmac_auth_key, hmac_auth_secret, True)
jSon = {u'contact_list': [{u'data': {u'disputed_at': u'2018-03-20T12:02:53+00:00', u'exchange_rate_updated_at': u'2018-03-20T00:18:51+00:00', u'advertisement': {u'payment_method': u'VANILLA', u'advertiser': {u'username': u'J_C', u'feedback_score': 100, u'trade_count': u'100+', u'last_online': u'2018-03-20T13:28:24+00:00', u'name': u'J_C (100+; 100%)'}, u'trade_type': u'ONLINE_BUY', u'id': 713669}, u'is_buying': True, u'payment_completed_at': u'2018-03-20T00:41:39+00:00', u'created_at': u'2018-03-20T00:18:51+00:00', u'contact_id': 19826811, u'seller': {u'username': u'GaiaTree', u'feedback_score': 100, u'trade_count': u'100+', u'last_online': u'2018-03-20T00:19:23+00:00', u'name': u'GaiaTree (100+; 100%)'}, u'currency': u'USD', u'amount': u'500.00', u'is_selling': False, u'buyer': {u'username': u'J_C', u'feedback_score': 100, u'trade_count': u'100+', u'last_online': u'2018-03-20T13:28:24+00:00', u'name': u'J_C (100+; 100%)'}, u'escrowed_at': u'2018-03-20T00:18:51+00:00', u'amount_btc': u'0.06466281', u'reference_code': u'L19826811BBSYGR', u'released_at': None, u'closed_at': None, u'account_info': u'{}', u'funded_at': u'2018-03-20T00:18:51+00:00', u'canceled_at': None, u'fee_btc': u'0.00064663'}, u'actions': {u'message_post_url': u'https://localbitcoins.com/api/contact_message_post/19826811/', u'advertisement_url': u'https://localbitcoins.com/api/ad-get/713669/', u'messages_url': u'https://localbitcoins.com/api/contact_messages/19826811/', u'cancel_url': u'https://localbitcoins.com/api/contact_cancel/19826811/', u'advertisement_public_view': u'https://localbitcoins.com/ad/713669'}}], u'contact_count': 1}
msg = {}
lastMessage = {}
attachment = False
messages = ["Hello!\r To continue with this trade please first verify identity with me. Please upload a selfie with yourself and your government issued identification (United States driver's license or for people outside the United States, Passport) \rI will check them then open information for you to send to me. \r\r***** HOLD PASSPORT OR ID CARD UNDER YOUR CHIN FOR VERIFICATION***** \r(This is an automated message I will be in the chat shortly)", "Payment Details released! \rPlease be sure to COMPLETELY read the payment details section and follow its instructions!  \r- thanks \rJ_C", "This is a test please ignore me :)", "Thanks for opening a trade with me! I will be here shortly if im not already. \r\r Just as a quick reminder this is for a Vanila Prepaid Debit Card that has a $5.95 fee that will be sbtracted from the total you have requested. I will be sending you pictures of the front and back of that card against the reciept so you can se the balance and that it is activated. \r\r\r If this is not what you wanted please let me know and I can cancel and if you have ny questions please feel free to ask.", "Hello!\r To continue with this trade please copy this next part and fill in the information.\r\r ======\rFirst Name: \rMiddle Name: \rLast Name: \rCountry of Residence: \rState of Residence (if applicable): \r======\r Please make sure your ID matches the info you have provided. :)", "*This is an Automated Message*\rThanks for sending me your information! I will review this info manually and make sure that I don't have any questions or need any more info.", "Great Seller! - J_C +100 (100%)", "Great buyer! - J_C +100 (100%)"]
balance = lc.getWallet()

#Checks if ther are any open contacts
def check_for_contacts():
    global contact_id
    global jSon
    while jSon['contact_count'] == 0:
        print("There are not contacts open at this time. Checing again in 1 mins")
        time.sleep(60)
        jSon = lc.getDashboard
    if jSon['contact_count'] != 0:
        contact_id = jSon['contact_list'][0]['data']['contact_id'] #dictionary inside list inside dictionary
        print("There is a contact! Checking against conditions now...")
    return contact_id

def lastMessage(contact_id):
    global msg
    global lastMessage
    msg = lc.getContactMessages(str(contact_id))
    lastMessage = msg["message_list"][-1]
    return lastMessage
        
def checkAttachment(lastMessage):
    global attachment
    attachment = lastMessage.has_key(["attachment_name"])
    return attachment

def getUser(contact_id):
    username = json['contact_list'][0]['data']['seller']['username']
    return username

def leaveSellerFeedback():
    while jSon['contact_list'][0]['data']['canceled_at'] == None and jSon['contact_list'][0]['data']['closed_at'] != None:
            lc.postFeedbackToUser(getUser(contact_id), "positive", message = messages[6])

check_for_contacts()
if contact_id != 0:
    #Checks if contact is a Zelle ONLINE_SELL Ad
    if  jSon['contact_list'][0]['data']['advertisement']['id'] == 605739:
#        lc.postMessageToContact(str(contact_id), messages[0])
#        msgs = lc.getContactMessages(str(contact_id))
        while lastMessage(contact_id)['msg'] == messages[0]:
            print("No response yet... checking in 15 seconds")
            time.sleep(15)
        if checkAttachment(lastMessage) == True:
            lc.postMessageToContact(str(contact_id), "")

    #Checks if contct is ONLINE_SELL bitcoins using Vanilla with US Dollar (USD)
    elif jSon['contact_list'][0]['data']['advertisement']['id'] == 713669:
#        lc.postMessageToContact(str(contact_id), messages[3])
        while lastMessage(contact_id)['msg'] == messages[3]:
            print("No response yet... checking in 15 seconds")
            time.sleep(15)
        if lastMessage(contact_id)['msg'] != messages[3]:
            print(lastMessage(contact_id)['msg'])
            
        
    
    #Check if contact is ONLINE_SELL bitcoins using Western Union with US Dollar (USD) 
    elif jSon['contact_list'][0]['data']['advertisement']['id'] == 679958:
#        lc.postMessageToContact(str(contact_id), messages[4])
        while lastMessage(contact_id)['msg'] == messages[4]:
            print("No response yet... checking in 15 seconds")
            time.sleep(15)
        if "First Name:" in lastMessage(contact_id)['msg']:
#           lc.postMessageToContact(str(contact_id), messages[5])
            1+1
    else:
        print("This contact meets none of the requirements and will be ignored...")
        check_for_contacts()
    





