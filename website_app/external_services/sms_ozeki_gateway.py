###############################################
##   Ozeki NG - SMS Gateway Python example   ##
###############################################

import urllib
import urllib.parse
import urllib.request


def send_smstext(parRecipient,parText):
    ###############################################
    ###            Ozeki NG informations        ###
    ###############################################
    host = "http://127.0.0.1"
    user_name = "admin"
    user_password = "Philea13"
    recipient = parRecipient
    message_body = parText
    recipient = "0035799359864"
    #message_body = "Hello World from Python"

    ###############################################
    ### Putting together the final HTTP Request ###
    ###############################################
    http_req = host
    http_req += ":9501/api?action=sendmessage&username="
    http_req += urllib.parse.quote(user_name)
    http_req += "&password="
    http_req += urllib.parse.quote(user_password)
    http_req += "&recipient="
    http_req += urllib.parse.quote(recipient)
    http_req += "&messagetype=SMS:TEXT&messagedata="
    http_req += urllib.parse.quote(message_body)
    ################################################
    ####            Sending the message          ###
    ################################################
    get = urllib.request.urlopen(http_req)
    req = get.read().decode('utf8')
    get.close()
    #print(req)
    ###############################################x
    ###        Verifying the response            ###
    ##############################################x#

    if req.find("Message accepted for delivery") > 1:
        print ("Message successfully sent")
        return("OK")
    else:
        print ("Message not sent! Please check your settings!")
        return("Message not sent! Please check your settings!")
