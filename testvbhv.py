import os, sys, time, json
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message, MediaMessage

profiledir=os.path.join(".","chrome_cache")
if not os.path.exists(profiledir): os.makedirs(profiledir)
driver = WhatsAPIDriver(profile=profiledir, client='chrome')

# driver = WhatsAPIDriver(client='chrome')
print("Waiting for QR")
driver.wait_for_login()
print("Saving session")
print("Bot started")

contacts = [7000521889, 8109583706];

for i in range(len(contacts)):
    wappId = "91" + str(contacts[i]) + "@c.us"
    print(wappId)
    driver.send_message_to_id(wappId, "hello world" + str(i))

driver.quit()