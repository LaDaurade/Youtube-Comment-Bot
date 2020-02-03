import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import re

 

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu");
chrome_options.add_argument("--no-sandbox");
chrome_options.add_argument("--disable-extensions");
chrome_options.add_argument("--proxy-server='direct://'");
chrome_options.add_argument("--proxy-bypass-list=*");
chrome_options.add_argument("--start-maximized");
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--log-level=3")
chrome_driver = os.getcwd() +"//chromedriver.exe"
chrome_options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

driver.get('https://accounts.google.com/signin/v2/identifier?uilel=3&service=youtube&hl=fr&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fhl%3Dfr%26action_handle_signin%3Dtrue%26next%3D%252F%253Fgl%253DFR%2526hl%253Dfr%26app%3Ddesktop&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
driver.get_screenshot_as_file("capture1.png")

#log in
id='your id'
mdp='your password'
driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(id)
time.sleep(random.randint(2,4))
driver.find_element_by_xpath('//*[@id="identifierNext"]/span/span').click()
time.sleep(random.randint(3,6))
driver.get_screenshot_as_file("capture2.png")
driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(mdp)
time.sleep(random.randint(2,4))
driver.find_element_by_xpath('//*[@id="passwordNext"]/span/span').click()
time.sleep(random.randint(5,10))
driver.get_screenshot_as_file("captureavant.png")
print("\nLOG : Ok\n")

#list of subjects you want
subjects=['subject1','subject2','...']

vuMax=100 #maximum view on the video commented
comMax=5  #maximum comm on the video commented
comMaxPerSub=6 #



 
def comment (s) :
 subject= subjects[s]
 print("SUBJECT:",subject)
 urls = []
 time.sleep(random.randint(2,5))
 driver.get('https://www.youtube.com/results?search_query='+subject+'&sp=CAISBAgCEAE%253D')
 time.sleep(random.randint(2,5))
 driver.get_screenshot_as_file("captureapressubjetct.png")
 driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
 time.sleep(random.randint(2,5))
 

 driver.execute_script("window.scrollBy(0, 2500);")
 time.sleep(random.randint(2,4))
 
 links = driver.find_elements_by_xpath('//*[@id="contents"]/ytd-video-renderer')
 nblink = len(links)
 if nblink > 20:
  nblink = 20 
 else :
  nblink = nblink +1
 print("\n----------NB LIEN(S) POUR :", subject, ":", nblink,"----------\n")
 for t in range(1,nblink):
  try:
   href = driver.find_element_by_xpath('//*[@id="contents"]/ytd-video-renderer['+ str(t) +']').find_element_by_id("video-title").get_attribute("href")
   urls.append(href)
  except:
   continue
 i=0
 u=1
 time.sleep(random.randint(2,5))
 
 for url in urls:
  print("\n**************",u,"/",nblink,"**************\n")
  print(url)
  u=u+1
  
#test if already see
  indexo = url.find('t=')
  if indexo == -1:
   print("Lien pas encore visité : OK")
  if indexo != -1:
   print("Lien déjà visité : NEXT")
   continue
  driver.get(url)
  time.sleep(random.randint(8,10))
  driver.execute_script("window.scrollBy(0, 150);")
  time.sleep(random.randint(2,3))
  driver.get_screenshot_as_file("capture1.png")
  time.sleep(random.randint(1,2))
  
#test sub (if > 1000 next)
  try:
   abo = driver.find_element_by_xpath('//*[@id="owner-sub-count"]').text
  except: #si vidéo de lancement ou live
   print("Live ou vidéo de Lancement : NEXT")
   continue
  index1 = abo.find('M')
  index2 = abo.find('k')
  if index1 == -1 and index2 == -1:
   print(abo,": C'est moins de mille : OK")
  if index1 != -1 or index2 != -1:
   print(abo,": C'est trop : NEXT")
   continue
   
#analyse subject (si != de certains : next)
  try:
   su = driver.find_element_by_xpath('//*[@id="content"]/yt-formatted-string/a').text
   
  except:
   driver.find_element_by_xpath('//*[@id="more"]').click()
   time.sleep(random.randint(1,2))
   su = driver.find_element_by_xpath('//*[@id="content"]/yt-formatted-string/a').text
   
  print(su)
  time.sleep(random.randint(1,2))
  

  try:
   vu = driver.find_element_by_xpath('//*[@id="count"]/yt-view-count-renderer/span[1]').text
   vuok=re.findall('\d+', vu)
   vudone="".join(vuok)
   print(vudone, "vues")
   
  except: #si vidéo de lancement ou live
   print("Live ou vidéo de Lancement : NEXT")
   continue
   
#analyse commentaires (si deja commenté ou + de 10 comms : next)
  driver.execute_script("window.scrollBy(0, 200);")
  time.sleep(random.randint(2,3))
  try:
   com = driver.find_element_by_xpath('//*[@id="count"]/yt-formatted-string').text
  except:
   print("Live ou vidéo de Lancement : NEXT")
   continue
  comok=re.findall('\d+', com)
  comdone="".join(comok)
  print(int(comdone), "commentaire(s)")
  sortir = 0
  
  if int(comdone)>= comMax :
   print("Il y a trop de coms : NEXT")
   continue
   
  if int(comdone)!= 0 :
   comms = driver.find_elements_by_xpath('//*[@id="contents"]/ytd-comment-thread-renderer')
   for c in range(0,len(comms)):
    commOk = re.sub('\n.*','',comms[c].text)
    print("Comm de :",commOk)
    if str(commOk) == "Aurélien Durand":
     print("Deja commenté : NEXT")
     sortir = 1
     break 
	 
  if sortir == 1 : 
   sortir = 0
   continue

#verif sub + vu
  try:
   if int(vudone)<vuMax:
    if str(su) == "Films et animations" or str(su) == "Sport" or str(su) == "Voyages et événements" or str(su) == "People et blogs" or str(su) == "Divertissement" or str(su) == "Vie pratique et style":
     print("Ecriture du commentaire ...")
    else:
     print("Sujet pas adéquat : NEXT")
     continue
   else:
    print("Trop de vues : NEXT")
    continue
	
  except: #si vu = aucune
   if str(su) == "Films et animations" or str(su) == "Sport" or str(su) == "Voyages et événements" or str(su) == "People et blogs" or str(su) == "Divertissement" or str(su) == "Vie pratique et style":
    print("Ecriture du commentaire ...")
   else:
    print("Sujet pas adéquat : NEXT")
    continue
  messages = ['Cool video! I have '+subject+' videos on my channel too','Nice! I made '+subject+' videos too', 'Great shots! I have '+subject+' videos on my channel too', 'interesting stuff! I create '+subject+' videos too', 'Top ! I produce '+subject+' videos on my channel too']

  if i==0 :
   r=0
  if r == len(messages) :
   r=0
  comment = messages[r]
  
  #commenting
  try:
   time.sleep(random.randint(80,100))
   driver.execute_script("window.scrollTo(0, 800)")
   time.sleep(random.randint(10, 15))
   driver.get_screenshot_as_file("capture.png")
   driver.find_element_by_xpath('//*[@id="simplebox-placeholder"]').click()
   time.sleep(random.randint(3,6))
   driver.find_element_by_xpath('//*[@id="contenteditable-root"]').send_keys(comment)
   time.sleep(random.randint(3,5))
   driver.find_element_by_xpath('//*[@id="contenteditable-root"]').send_keys(Keys.CONTROL + Keys.ENTER)
   time.sleep(random.randint(10,15))
   i=i+1
   r=r+1
   print("Comm Numero : ",i,":",comment)
  except:
   continue 
   print("ERREUR COMM : VEUILLEZ VERIFIER LE CODE")
  time.sleep(random.randint(10,20))
  if i == comMaxPerSub:
   break
 print("\n----------NB COM POUR :",subject,":", i,"----------\n")


#infinit loop
while True:
   for k in range(0,len(subjects)-1):
    comment(k)
    print("\nPause...\n")
    time.sleep(random.randint(600,1000))
    print("\nReprise !\n")



