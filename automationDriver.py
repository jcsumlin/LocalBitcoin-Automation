# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 17:05:36 2018

@author: Chat
"""
import LocalBitcoin
import time
import re
import webbrowser
import glob
import os
from PIL import Image
from pushbullet import Pushbullet
import sys

pb = Pushbullet("o.QZcGfXBjlLNbDvi5ldZNSG2zkxoYAPps")

MyUsername = "J_C"
contact_id = 0
contact = 0

hmac_auth_key = ""
hmac_auth_secret = ""

lc = LocalBitcoin.LocalBitcoin(hmac_auth_key, hmac_auth_secret, True)

msg = {}
lastMessage = {}
attachment = False
messages = ["Hello!\r To continue with this trade please first verify identity with me. Please upload a selfie with yourself and your government issued identification (United States driver's license or for people outside the United States, Passport) \rI will check them then open information for you to send to me. \r\r***** HOLD PASSPORT OR ID CARD UNDER YOUR CHIN FOR VERIFICATION***** \r(This is an automated message I will be in the chat shortly)", "Payment Details released! \rPlease be sure to COMPLETELY read the payment details section and follow its instructions!  \r- thanks \rJ_C", "This is a test please ignore me :)", "Thanks for opening a trade with me! I will be here shortly if im not already. \r\r Just as a quick reminder this is for a Vanila Prepaid Debit Card that has a $5.95 fee that will be sbtracted from the total you have requested. I will be sending you pictures of the front and back of that card against the reciept so you can se the balance and that it is activated. \r\r\r If this is not what you wanted please let me know and I can cancel and if you have ny questions please feel free to ask.", "Hello!\r To continue with this trade please copy this next part and fill in the information.\r\r ======\rFirst Name: \rMiddle Name: \rLast Name: \rCountry of Residence: \rState of Residence (if applicable): \r======\r Please make sure your ID matches the info you have provided. :)", "*This is an Automated Message*\rThanks for sending me your information! I will review this info manually and make sure that I don't have any questions or need any more info.", "Great Seller! - J_C +100 (100%)", "Great buyer! - J_C +100 (100%)", "Thanks for uploading the picture! Verifying now...", "Im sorry but the name on your LocalBTC account does not match the name on your ID and I cannot fully verify you for this trade.", "HI there! \r Thanks for opening a trade with me to sell your bitcoins for Zelle payment. Please copy and fill this next part so I can submit payment! \r=======\r First Name: \r Last Name: \r Email/Phonr on account:\r=======", "Payment has been made, please confirm then release coins :)", "Thanks for your reply I am verifying your info manually now then I will submit payment!", "Beep Boop Beep, I am a Bot!\r I don't recognize that last message as a valid input. If you have questions please reply with QUESTIONS and I will get you assistance :)", "Beep Boop Beep! Im a Bot!\rResponse Recieved! Notifing Account Holder, they'll be with you soon!", "Thanks for opening a trade with me! I will be here shortly if im not already.\r\r Just as a quick reminder this is for a MoneyPak Card that has a $5.95 fee that will be subtracted from the total you have requested. I will be sending you pictures of the back of that card against the reciept so you can se the balance and that it is activated.\r\r If this is not what you wanted please let me know and I can cancel and if you have ny questions please feel free to ask.", "Hi there! \rThanks for opening a trade with me to sell your bitcoins for Wells Fargo/PNC/ZELLE/BB&T/Regions deposits. Please copy and fill this next part so I can submit payment! \r=======\r First Name: \r Last Name: \r Email/Phone on account (for Zelle):\r Account Number (for Cash Deposit):\r======", "Hey there! Thanks for opening a trade with me! Please make sure you read the terms of trade and respond with OPTION 1 or OPTION 2 depening on what you want to proceed with.", "Option 1 Selected!(Invoice)\rPlease send the invoice to PayPal email: jcsumlin@gmail.com", "Option 2 Selected! (Cash fill up from CVS)\rPlease generate the barcode for a cash fill up at a CVS store and upload it here.\r\rThe fee is $3.95 and will be deducted from the total loaded"]
balance = lc.getWallet()
latest_file = ""

#Checks if ther are any open contacts
def check_for_contacts():
    global contact_id
    global dIct
    dIct = lc.getDashboard()
    if dIct['contact_count'] == 0:
        print("There are no contacts open at this time. Checing again in 1 mins")
        return False
    
    elif dIct['contact_count'] > 0:
        dIct = lc.getDashboard()
        contact_id = dIct['contact_list'][0]['data']['contact_id'] #dictionary inside list inside dictionary
        return contact_id

def checkLastMessage(contact_id):
    global msg
    global lastMessage
    msg = lc.getContactMessages(str(contact_id))
    lastMessage = msg["message_list"][-1]
    return lastMessage
        
def checkAttachment(contact_id):
    global attachment
    if "attachment_url" in checkLastMessage(str(contact_id)):
        attachment = True
    else:
        attachment = False
    return attachment

def getUser(contact_id):
    username = lc.getContactInfo(str(contact_id))
    if username['is_buying'] == True:
        username = username['seller']['username']
    else:
        username = username['buyer']['username']
    return username

def leaveSellerFeedback(contact_id, contact):
    trade = lc.getContactInfo(str(contact_id))
    if trade['canceled_at'] != None:
        return
    lc.postFeedbackToUser(getUser(contact_id), "positive", message = messages[6])

def leaveBuyerFeedback(contact_id, contact):
    trade = lc.getContactInfo(str(contact_id))
    if trade['canceled_at'] != None:
        return
    lc.postFeedbackToUser(getUser(contact_id), "positive", message = messages[7])

def getImage(contact_id):
    global latest_file
    apiUrl = str(lastMessage['attachment_url'])
    fileNumber = re.search('[0-9]{9}', apiUrl)
    url = "https://localbitcoins.com/contact/" + str(contact_id) + "/download/" + str(fileNumber.group()) + "/"
    webbrowser.open(url)  #Open Attachment URL
    #gets Latest download
    latest_file = max(glob.glob('C:\Users\Chat\Downloads\*'), key=os.path.getctime)
    #prints file path
    print(latest_file)
    

def ZelleBuyAd():
    #Step 1: Send Welcome Message and wait for response
    lc.postMessageToContact(str(contact_id), messages[0])
    while checkLastMessage(contact_id)['msg'] == messages[0]:
        print("No response yet... checking in 15 seconds")
        time.sleep(15)
    #RESPONSE RECIEVED!
    #Step 2: While there is not an attachment in the last message sent... 
        #if no attachment Print that message
        #If yes attachment send thankyou message
    response = ""
    while checkAttachment(str(contact_id)) != True:
        if checkLastMessage(str(contact_id)) != response:
            print("Last Message did not contain an attachment.")
            print("Last Message:", str(lastMessage['msg']))
            response = raw_input("Please Enter Response (or nothing to wait 15s): ")
            if response != "":
                lc.postMessageToContact(str(contact_id), str(response))
            else:
                print("Waiting 15s before checking again")
                time.sleep(15)
        else:
            print("No response yet, waiting 15s before checking again")
            time.sleep(15)
    print("This last message had an attachment!")
    #thankyou message 
    lc.postMessageToContact(str(contact_id), messages[8])
    #Download that attachment through Chrome
    getImage(contact_id)
    
    try:
        download = Image.open(latest_file)
    except:
        print("Unable to load image")
    #Show that most recently downloaded image (in your downloads folder)
    download.show()
    
    print("Does the real name of ...")
    lc.getContactInfo(str(contact_id))
    print(dIct['contact_list'][contact]['data']['buyer']['real_name'])
    realNameAsk = str(raw_input("Match the name on the ID? (y/n): "))
    if realNameAsk.lower() == "n" or realNameAsk.lower() == "no":
        lc.postMessageToContact(str(contact_id), messages[9])
    
    #Step 3 Ask if we should verify identity (if it is even needed)
    s = raw_input("Should we verify the idendity of the user? (yes/no)")
    if s.lower() == "yes" or s.lower() == "y":
        #Mark Identity verified.
        lc.markIdentityVerified(str(contact_id))
    elif s.lower() == "no" or s.lower() == "n":
        reason = raw_input("What is the reason for not verifying?")
        lc.postMessageToContact(str(contact_id), str(reason))
    print("Job done, Please confirm funds and release")
    #Wait for contact to be marked as released
    currentContact = lc.getContactInfo(str(contact_id))
    while currentContact['released_at'] == None:
        time.sleep(60)
        currentContact = lc.getContactInfo(str(contact_id))
    print("All conditions satisfied and contact has been released by user...")
    print("Released at: " + currentContact['released_at'])
    
            
            
def vanillaSellAd():
    lc.postMessageToContact(str(contact_id), messages[3])
    while checkLastMessage(contact_id)['msg'] == messages[3]:
        print("No response yet... checking in 15 seconds")
        time.sleep(15)
    print(checkLastMessage(contact_id)['msg'])
    response = raw_input("Response: ")
    while response != "":
        lc.postMessageToContact(str(contact_id), response)
        while checkLastMessage(contact_id)['msg'] == response:
            print("No response yet... checking in 15 seconds")
            time.sleep(15)
        print(checkLastMessage(contact_id)['msg'])
        response = raw_input("Response: ")

    leaveSellerFeedback(contact_id, contact)
def checkIfPaid(contact_id):
    paid = raw_input("Have you paid? (y/n)")
    while paid.lower() == "n" or paid.lower() == "no":
        time.sleep(2)
        paid = raw_input("Have you paid? (y/n)")
    if paid.lower() == "y" or paid.lower() == "yes":
        return True
    else:
        return False


def main():
    global contact
    contact_id = dIct['contact_list'][contact]['data']['contact_id']
    push = pb.push_note("NEW LOCALBTC CONTRACT", "Trade for: " + dIct['contact_list'][contact]['data']['amount'] + " " + dIct['contact_list'][contact]['data']['currency'])
    for x in dIct['contact_list']:  #for each open contact...
        #Checks if contact is a Zelle ONLINE_BUY Ad
        if  dIct['contact_list'][contact]['data']['advertisement']['id'] == 605739:#Replace with your own ad identifier (Found in the Dashboard)
            ZelleBuyAd()
            #Final Step: Leave positive feedback
            leaveBuyerFeedback(contact_id, contact)
            contact = contact + 1
            
            
        #Checks if contct is ONLINE_SELL bitcoins using Vanilla with US Dollar (USD)
        elif dIct['contact_list'][contact]['data']['advertisement']['id'] == 713669:
            vanillaSellAd()
            contact = contact + 1
        
        #Check if contact is ONLINE_SELL bitcoins using Western Union with US Dollar (USD) 
        elif dIct['contact_list'][contact]['data']['advertisement']['id'] == 679958:
            lc.postMessageToContact(str(contact_id), messages[4])
            while checkLastMessage(contact_id)['msg'] == messages[4]:
                print("No response yet... checking in 15 seconds")
                time.sleep(15)
                
            if "First Name:" in checkLastMessage(contact_id)['msg']:
                lc.postMessageToContact(str(contact_id), messages[5])
                push = pb.push_note("Western Union Trade Info", checkLastMessage(contact_id)['msg'])

            else:
                print("Unrecognized input notifying user")
                lc.postMessageToContact(str(contact_id), messages[13])
                while messages[13] in checkLastMessage(contact_id)['msg']:
                    time.sleep(15)
                if "QUESTIONS" in checkLastMessage(contact_id)['msg']:
                    lc.postMessageToContact(str(contact_id), messages[14])
                    print("User has questions! Please enter chat.")
                    push = pb.push_note("Western Union Trade", "User has question, please check chat")
            if checkIfPaid(contact_id) == True:
                lc.markContactAsPaid(str(contact_id))
                lc.postMessageToContact(str(contact_id), messages[11])
                print("Contact Successfully marked as paid")
            else:
                sys.exit("Error message @ line 229")
            contact = contact + 1

        #Checks if contact is Sell bitcoins using ✔️Zelle✔️
        elif dIct['contact_list'][contact]['data']['advertisement']['id'] == 631643:
            print("New Sell bitcoins using ✔️Zelle✔️")
            lc.postMessageToContact(str(contact_id), messages[10])
            checkIfPaid(contact_id)
            lc.markContactAsPaid(str(contact_id))
            lc.postMessageToContact(str(contact_id), messages[12])
            print("Contact Successfully marked as paid")
            print("Waiting for release...")
            zelle_buy_ad = lc.getContactInfo(str(contact_id))
            while zelle_buy_ad['released_at'] == None:
                time.sleep(15)
                zelle_buy_ad = lc.getContactInfo(str(contact_id))
                print("...")
            lc.postFeedbackToUser(getUser(contact_id), "positive", message = messages[6])
            contact = contact + 1
        #Checks if contact Sell bitcoins using Bank: Zelle
        elif dIct['contact_list'][contact]['data']['advertisement']['id'] == 714946:
            lc.postMessageToContact(str(contact_id), messages[10])
            while checkLastMessage(contact_id)['msg'] == messages[10]:
                print("No response yet... checking in 15 seconds")
                time.sleep(15)
            lc.postMessageToContact(str(contact_id), messages[12])
            if checkIfPaid(contact_id) == True:
                lc.markContactAsPaid(str(contact_id))
                lc.postMessageToContact(str(contact_id), messages[11])
                print("Contact Successfully marked as paid")
            else:
                sys.exit("Error message @ line 257")
            print("Waiting for release...")
            zelle_buy_ad = lc.getContactInfo(str(contact_id))
            while zelle_buy_ad['released_at'] == None:
                time.sleep(15)
                zelle_buy_ad = lc.getContactInfo(str(contact_id))
                print("...")
            lc.postFeedbackToUser(getUser(contact_id), "positive", message = messages[6])
            contact = contact + 1
        #676055 Cash deposit: ⚡️Wells Fargo/PNC/ZELLE/BB&T/Regions⚡️
        elif dIct['contact_list'][contact]['data']['advertisement']['id'] == 676055:
            lc.postMessageToContact(str(contact_id), messages[16])
            while checkLastMessage(contact_id)['msg'] == messages[16]:
                print("No response yet... checking in 15 seconds")
                time.sleep(15)
            if "first name:" in checkLastMessage(contact_id)['msg'].lower():
                lc.postMessageToContact(str(contact_id), messages[5])
                print(checkLastMessage(contact_id)['msg'])
                push = pb.push_note("LocalBTC", checkLastMessage(contact_id)['msg'])
            else:
                print("Unrecognized input notifying user")
                lc.postMessageToContact(str(contact_id), messages[13])
                while messages[13] in checkLastMessage(contact_id)['msg']:
                    time.sleep(15)
                if "QUESTION" in checkLastMessage(contact_id)['msg']:
                    push = pb.push_note("LocalBTC", "User has question for Cash deposit: ⚡️Wells Fargo/PNC/ZELLE/BB&T/Regions⚡️")
                    lc.postMessageToContact(str(contact_id), messages[14])
                elif "First Name:" in checkLastMessage(contact_id)['msg']:
                    lc.postMessageToContact(str(contact_id), messages[5])
                    print(checkLastMessage(contact_id)['msg'])
                    push = pb.push_note("LocalBTC", str(checkLastMessage(contact_id)['msg']))
                else:
                    sys.exit("Error message @ line 292")
            print(checkLastMessage(contact_id)['msg'])
            if checkIfPaid(contact_id) == True:
                lc.markContactAsPaid(str(contact_id))
                lc.postMessageToContact(str(contact_id), messages[12])
                print("Contact Successfully marked as paid")
            else:
                sys.exit("Error message @ line 295")
            print("Waiting for release...")
            zelle_buy_ad = lc.getContactInfo(str(contact_id))
            while zelle_buy_ad['released_at'] == None:
                time.sleep(15)
                zelle_buy_ad = lc.getContactInfo(str(contact_id))
                print("...")
            lc.postFeedbackToUser(getUser(contact_id), "positive", message = messages[6])
            contact = contact + 1
        #680699 Pre-Paid Debit Card: MoneyPak with US Dollar
        elif dIct['contact_list'][contact]['data']['advertisement']['id'] == 680699:
            print("New contact Pre-Paid Debit Card: MoneyPak with US Dollar")
            lc.postMessageToContact(str(contact_id), messages[15])
            lc.postMessageToContact(str(contact_id), "Beep Boop Beep, I'm a bot!\rTo continue with this trade please respond with CONTINUE, or CANCEL to close the trade.")
            while checkLastMessage(contact_id)['msg'] == "Beep Boop Beep, I'm a bot!\rTo continue with this trade please respond with CONTINUE, or CANCEL to close the trade.":
                print("No response yet... checking in 15 seconds")
                time.sleep(15)
            print(checkLastMessage(contact_id)['msg'])
            move_on = False
            while move_on == False:
                if checkLastMessage(contact_id)['msg'] == "CONTINUE":
                    print("User wishes to continue with trade...")
                    lc.postMessageToContact(str(contact_id), "Thanks! The user has been notified and is on the way to get your card")
                    move_on = True
                elif checkLastMessage(contact_id)['msg'] == "CANCEL":
                    print("User wishes to cancel... Canceling trade")
                    lc.cancelContact(str(contact_id))
                    
                else:
                    lc.postMessageToContact(str(contact_id), "Sorry thats not a valid option, please respond with either CONTINUE or CANCEL")
                    move_on = False
            
            if checkIfPaid(contact_id) == True:
                lc.markContactAsPaid(str(contact_id))
                lc.postMessageToContact(str(contact_id), messages[11] + "\rPLease allow 20 before you deposit the card.")
                print("Contact Successfully marked as paid")
            else:
                sys.exit("Error message @ line 336")
            print("Waiting for release...")
            moneypak_buy_ad = lc.getContactInfo(str(contact_id))
            while moneypak_buy_ad['released_at'] == None:
                time.sleep(15)
                moneypak_buy_ad = lc.getContactInfo(str(contact_id))
                print("...")
            lc.postFeedbackToUser(getUser(contact_id), "positive", message = messages[6])
            contact = contact + 1
        #714336 Sell bitcoins using Paypal with US Dollar (USD)
        elif dIct['contact_list'][contact]['data']['advertisement']['id'] == 714336:
            print("New contact Paypal with US Dollar (USD)")
            lc.postMessageToContact(str(contact_id), messages[17])
            while checkLastMessage(contact_id)['msg'] == messages[17]:
                print("No response yet... checking in 15 seconds")
                time.sleep(15)
            print(checkLastMessage(contact_id)['msg'])
            move_on = False
            while move_on == False:
                if checkLastMessage(contact_id)['msg'] == "OPTION 1":
                    lc.postMessageToContact(str(contact_id), messages[18])
                    move_on = True
                elif checkLastMessage(contact_id)['msg'] == "OPTION 2":
                    lc.postMessageToContact(str(contact_id), messages[19])
                    move_on = True
                else:
                    lc.postMessageToContact(str(contact_id), "Sorry thats not a valid option, please respond with either OPTION 1 or OPTION 2")
                    move_on = False
            if checkIfPaid(contact_id) == True:
                lc.markContactAsPaid(str(contact_id))
                print("Contact Successfully marked as paid")
            else:
                sys.exit("Error message @ line 368")

            print("Waiting for release...")
            paypal_buy_ad = lc.getContactInfo(str(contact_id))
            while paypal_buy_ad['released_at'] == None:
                time.sleep(15)
                paypal_buy_ad = lc.getContactInfo(str(contact_id))
                print("...")
            if paypal_buy_ad['released_at'] != None:
                print("User has released contact and feedback will be left now.")
                lc.postFeedbackToUser(getUser(contact_id), "positive", message = messages[6])
            
        else:
            print("This contact meets none of the requirements and will be ignored...")
            check_for_contacts()


while check_for_contacts() == False:
    time.sleep(60)
    contact = 0

print("There is a contact! Checking against conditions now...")
print('Number of contacts: ' + str(dIct['contact_count']))
main()