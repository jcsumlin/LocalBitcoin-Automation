# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 17:05:36 2018

@author: Chat
"""
import LocalBitcoin
import time
#import Image
#import kivy
#from kivy.app import App
#from kivy.uix.button import Button


username = "J_C"
contact_id = 0
hmac_auth_key = ""
hmac_auth_secret = ""


lc = LocalBitcoin.LocalBitcoin(hmac_auth_key, hmac_auth_secret, True)
dIct = lc.getDashboard()
msg = {}
lastMessage = {}
attachment = False
messages = ["Hello!\r To continue with this trade please first verify identity with me. Please upload a selfie with yourself and your government issued identification (United States driver's license or for people outside the United States, Passport) \rI will check them then open information for you to send to me. \r\r***** HOLD PASSPORT OR ID CARD UNDER YOUR CHIN FOR VERIFICATION***** \r(This is an automated message I will be in the chat shortly)", "Payment Details released! \rPlease be sure to COMPLETELY read the payment details section and follow its instructions!  \r- thanks \rJ_C", "This is a test please ignore me :)", "Thanks for opening a trade with me! I will be here shortly if im not already. \r\r Just as a quick reminder this is for a Vanila Prepaid Debit Card that has a $5.95 fee that will be sbtracted from the total you have requested. I will be sending you pictures of the front and back of that card against the reciept so you can se the balance and that it is activated. \r\r\r If this is not what you wanted please let me know and I can cancel and if you have ny questions please feel free to ask.", "Hello!\r To continue with this trade please copy this next part and fill in the information.\r\r ======\rFirst Name: \rMiddle Name: \rLast Name: \rCountry of Residence: \rState of Residence (if applicable): \r======\r Please make sure your ID matches the info you have provided. :)", "*This is an Automated Message*\rThanks for sending me your information! I will review this info manually and make sure that I don't have any questions or need any more info.", "Great Seller! - J_C +100 (100%)", "Great buyer! - J_C +100 (100%)", "Thanks for uploading the picture! Verifying now..."]
balance = lc.getWallet()

#Checks if ther are any open contacts
def check_for_contacts():
    global contact_id
    global dIct
    while dIct['contact_count'] == 0:
        print("There are not contacts open at this time. Checing again in 1 mins")
        time.sleep(60)
        dIct = lc.getDashboard
    if dIct['contact_count'] != 0:
        contact_id = dIct['contact_list'][0]['data']['contact_id'] #dictionary inside list inside dictionary
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
    username = dIct['contact_list'][0]['data']['seller']['username']
    return username

def leaveSellerFeedback():
    while dIct['contact_list'][0]['data']['canceled_at'] == None and dIct['contact_list'][0]['data']['closed_at'] != None:
            lc.postFeedbackToUser(getUser(contact_id), "positive", message = messages[6])
def leaveBuyerFeedback():
    while dIct['contact_list'][0]['data']['canceled_at'] == None and dIct['contact_list'][0]['data']['closed_at'] != None:
        lc.postFeedbackToUser(getUser(contact_id), "positive", message = messages[7])


while check_for_contacts() != 0:
    for x in dIct['contact_list']:  #for each open contact...
        #Checks if contact is a Zelle ONLINE_BUY Ad
        if  dIct['contact_list'][0]['data']['advertisement']['id'] == 605739:#Replace with your own ad identifier (Found in the Dashboard)
    #        lc.postMessageToContact(str(contact_id), messages[0])
    #        msgs = lc.getContactMessages(str(contact_id))
            while lastMessage(contact_id)['msg'] == messages[0]:
                print("No response yet... checking in 15 seconds")
                time.sleep(15)
            if checkAttachment(lastMessage) == True:
                lc.postMessageToContact(str(contact_id), )#messages[8])
                s = input("Should we verify the idendity of the user? (yes/no)")
                if s.lower() == "yes" or s.lower() == "y":
                    lc.markIdentityVerified(contact_id)
                elif s.lower() == "no" or s.lower() == "n":
                    1+1
            while dIct['contact_list'][0]['data']['released_at'] != None:
                leaveBuyerFeedback(getUser(contact_id), "positive", message = messages[7])
            
            
        #Checks if contct is ONLINE_SELL bitcoins using Vanilla with US Dollar (USD)
        elif dIct['contact_list'][0]['data']['advertisement']['id'] == 713669:
    #        lc.postMessageToContact(str(contact_id), messages[3])
            while lastMessage(contact_id)['msg'] == messages[3]:
                print("No response yet... checking in 15 seconds")
                time.sleep(15)
            if lastMessage(contact_id)['msg'] != messages[3]:
                print(lastMessage(contact_id)['msg'])
            leaveSellerFeedback()
            
        
        #Check if contact is ONLINE_SELL bitcoins using Western Union with US Dollar (USD) 
        elif dIct['contact_list'][0]['data']['advertisement']['id'] == 679958:
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
            
    
    





