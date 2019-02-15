# """
# Initialising Automagica
# """"
import time
from datetime import datetime
from datetime import timedelta
from automagica import *

def test_with_robot():
    print('###start###')
    scenario = 0 #scenario
    st = datetime.now()
    # + timedelta(days=31)
    while scenario < 1:
        scenario = scenario + 1
        ii = 0
        browser = ChromeBrowser()
        #browser.minimize_window
        browser.get('https://ifestionas.pythonanywhere.com')
        title = browser.title
        if title != 'ganimedes business technology':
            print('FAILED!!!!!!!!!!!!!')
            #//*[@id="id_ifestionas_pythonanywhere_com"]/form/div[1]/div/button
            exit(0)
        waitsec=1
        while ii < 13:
            ii = ii + 1
            ct = datetime.now()
            title = browser.title
            #DisplayMessageBox(title)
            #x = 10
            #y = 10
            #DoubleClickOnPosition(x, y)
            e = ct - st
            e_seconds = e.total_seconds()
            e_minutes =  divmod(e_seconds, 60)[0]
            print('   ', ii, datetime.now(), e_seconds, e_minutes, title)
            print('      ', browser.current_url, browser.session_id)
            Wait(seconds=waitsec)
            waitsec = waitsec * 2
            try:
                askmelater = browser.find_element_by_id('askmelater')
                askmelater.click()
                x = 1
                print('         ', '***ask me later')
            except:
                x = 2

            try:
                learnmore = browser.find_element_by_id('learnmore')
                learnmore.click()
                x = 1
                print('         ', 'learn more')
            except:
                x = 0

            if x == 0:
                try:
                    learnmore = browser.find_element_by_xpath('//*[@id="/html/body/div[1]/div[2]/div[12]/div/div[1]/div/div[3]/p/a"]')
                    learnmore.click()
                    x = 1
                    print('         ', 'xxxx learn more')
                except:
                    x = 0

            if x == 0:
                print('                Errors........')        

        browser.close()
        ct = datetime.now()
        e = ct - st
        e_seconds = e.total_seconds()
        e_minutes =  divmod(e_seconds, 60)[0]
        print('')
        print(scenario, datetime.now(), e_seconds, e_minutes)
        #Wait(seconds=5)

    print('###finished###')

# """
# Browser Automation - Searching on Google with Xpath
# """

# from automagica import *
# browser = ChromeBrowser()
# browser.get('https://google.com')
# # Enter Search Text
# browser.find_element_by_xpath('//*[@id="lst-ib"]').send_keys('Oslo')

# # Submit
# browser.find_element_by_xpath('//*[@id="lst-ib"]').submit()

# """
# Browser Automation - Searching on Google with ?q in URL
# """

# from automagica import *
# browser = ChromeBrowser()
# browser.get('https://google.com/?q=oslo')

# """
# Browser Automation - Searching on Bing with Xpath
# """

# from automagica import *
# browser = ChromeBrowser()
# browser.get('https://bing.com')
# # Enter Search Text
# browser.find_element_by_xpath('//*[@id="sb_form_q"]').send_keys('Oslo')
# # Submit
# browser.find_element_by_xpath('//*[@id="sb_form_q"]').submit()

# """
# Browser Automation - Searching on Bing with ?q in URL
# """

# from automagica import *
# browser = ChromeBrowser()
# browser.get('https://bing.com/?q=oslo')

# """
# Finding Google search results with Automagica
# """

# from automagica import *
# GetGoogleSearchLinks("oslo")

# """
# Visit every Google Search Result for Oslo
# """

# from automagica import *
# browser = ChromeBrowser()
# for link in GetGoogleSearchLinks("oslo"):
#     browser.get(link)

# """
# Save every Google Search Result for Oslo in a .txt
# """

# from automagica import *
# browser = ChromeBrowser()
# links = GetGoogleSearchLinks("oslo")
# WriteListToFile(links, file="results.txt")

# """
# Browser Automation - Closing
# """"
# from automagica import *

# browser = ChromeBrowser()
# browser.get('https://bing.com')
# title = browser.title
# if not "Google" in title:
#     browser.close()
#     DisplayMessageBox(title, title="Oops!", type="warning")

# """
# Simple Mouse Example 1
# """

# from automagica import *
# GetMouseCoordinates()

# """
# Simple Mouse Example 2
# """

# from automagica import *
# x = 100
# y = 100
# DoubleClickOnPosition(x, y)

# """
# Simple Mouse Example - Failsafe
# """

# from automagica import *
# import random

# for i in range(0,10):
#     random_X_position = random.randint(300,500)
#     random_Y_position = random.randint(300,500)
#     DragToPosition(random_X_position, random_Y_position)

# """
# Copy File, in this case an xlsx
# """
# from automagica import *
# Copyfile("example.xlsx", "copy.xlsx")    
if __name__ == '__main__':
    test_with_robot()
    