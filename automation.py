import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

# sqlite 
conn = sqlite3.connect('instagram_project.sqlite')
curr= conn.cursor()
curr.execute("CREATE TABLE IF NOT EXISTS followers(ID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT , name TEXT)")

driver = webdriver.Firefox(executable_path="path of webdriver") # it is firefox here, but you can use your own browser
driver.get("https://instagram.com/")
sleep(1.5)

class instagram:
   def __init__(self , username , password):
      self.username=username
      self.password=password
      logbox=driver.find_element_by_name('username')
      logbox.send_keys(self.username)

      passwordBox = driver.find_element_by_name('password')
      passwordBox.send_keys(self.password)

      driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]').click()
      sleep(5)

      # first popup
      try:
         driver.find_element_by_xpath('//button[@class = "sqdOP yWX7d    y3zKF     "]').click()
      except:
         pass
      
      # second popup 
      try:
         driver.find_element_by_xpath('//button[@class = "aOOlW   HoLwm "]').click()
      except:
         pass

       # clicking the profile 
      driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/a/img').click()
      sleep(1)

   def followers(self):
      driver.find_element_by_xpath("//a[contains(@href , 'followers')]").click()   
      sleep(1) 

      # scroll the popupbox
      scrollbox = driver.find_element_by_class_name('isgrP')
      oldHeight , newHeight= -1 , 1

      while(oldHeight != newHeight):
         oldHeight = newHeight
         driver.execute_script("arguments[0].scrollTo(0 , arguments[0].scrollHeight);" , scrollbox)
         sleep(1.5)
         newHeight = driver.execute_script("return arguments[0].scrollHeight" , scrollbox)
      
      # fetching names  
      lst = scrollbox.find_elements_by_tag_name('a')

      # getting username
      for name in lst:
         if(len(name.text) != 0):
            # inserting username in database table followers   
            curr.execute("INSERT INTO followers(Username) VALUES(?)", (name.text,))
      conn.commit()

      # getting names
      lst= scrollbox.find_elements_by_class_name('wFPL8')
      for i, name in enumerate(lst):  
         # inserting id names in database
         curr.execute("UPDATE followers set name=? WHERE ID=?" , (name.text ,i+1))
      conn.commit()
 
      print("followers fetching done !!")
      curr.close()
      conn.close()
      scrollbox.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()
      sleep(3)
      driver.close()
    
x=instagram('your username' , 'password')
x.followers()


