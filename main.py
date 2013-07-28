#!/usr/bin/python

from json import load
from urllib2 import *
from Tkinter import *
import socket
from ast import literal_eval
import subprocess
import os

class Gui(Frame):
  def __init__(self, parent, bg='white'):
    self.city_name_base = StringVar()
    self.city_name_base.set('City name')
    Frame.__init__(self, parent, bg='White')
    self.parent = parent
    self.initUI()
    
  def initUI(self):
    self.parent.title("Weather checker 1.0")
    self.pack()
    self.widgets()
    
  def widgets(self):
    self.city_name = StringVar()
    self.city_name.set('City')

    self.label_city = LabelFrame(self.parent, text = "Choose your city", padx=1, pady=5, bg='#DF7401', fg='#8A4B08')
    self.label_city.pack(ipadx=10, ipady=10)

    self.entry_name = Entry(self.label_city, width=30, textvariable=self.city_name_base)
    self.entry_name.pack()
  
    self.city_prompt = Label(self. label_city, justify=RIGHT, textvariable=self.city_name, bg='#DF7401' )
    self.city_prompt.pack(side=RIGHT)
  
    self.butt_apply = Button(self.label_city, text='Submit', bg='#FFBF00', command=self.change_city, width=20)
    self.butt_apply.pack(side=LEFT)
 
  def change_city(self):
    self.city_name.set("Your city is " + self.city_name_base.get())
    self.city_name_1 = self.city_name_base.get()
    
#    self.city_name_1 = 'London'    # just for testing delete afterwards

    Fetch_weather = fetch_weather(self.city_name_1)

class fetch_weather(Gui):
  def __init__(self, city_name_1):
    self.city_name = city_name_1
    self.fetch_raw()

  def fetch_raw(self):
    self.proxy = ProxyHandler({'http': '172.17.35.1:8080'})    #just comment 3 lines if you don't use proxy
    self.opener = build_opener(self.proxy)
    install_opener(self.opener)

    self.data = urlopen('http://openweathermap.org/data/2.1/find/name?q='+self.city_name+'&units=metric')
    self.cities = load(self.data)

    self.get_info()

  def get_info(self):
    if self.cities['count'] > 0:
      self.city = self.cities['list'][0]

      self.max_temp = (self.city['main']['temp_max'])
      self.temp_min = (self.city['main']['temp_min'])
      self.pressure = (self.city['main']['pressure'])
      self.temp = (self.city['main']['temp'])
      self.humidity = (self.city['main']['humidity'])
 
      self.main = str((self.city['weather'])).split(',')

      self.desc = ''
      for line in self.main:
        self.match = re.search(r"description.+u'(.+)'", line )
        if self.match:
          self.description = self.match.group(1).rstrip()
           
      self.desc1 = self.description.split(' ') 
      self.desc = "_".join(self.desc1)

    for line in self.main:
      self.match = re.search(r".+icon.+'(.+)'", line)
      if self.match:
        self.iconID = self.match.group(1)

    self.fetch_pictures()

  def fetch_pictures(self):
    '''fetching and creating icon of current weather'''

    self.full_path_ico = ''

    self.proxy = ProxyHandler({'http': '172.17.35.1:8080'})    #just comment 3 lines if you don't use proxy
    self.opener = build_opener(self.proxy)
    install_opener(self.opener)

    self.img_path = r'./ico'
    if not os.path.exists(self.img_path): os.makedirs(self.img_path)

    try:                                                            #check if this icon already exists
      with open(''+self.img_path+'/'+self.iconID+'.png'):pass
    except IOError:                                                 # if icon doesn't exist - create it
      self.img = open(''+self.img_path+'/'+self.iconID+'.png', 'w')
      self.img.write(urlopen('http://openweathermap.org/img/w/'+self.iconID+'.png').read())
      self.img.close()

    self.current_path = os.getcwd()
    self.full_path_ico = self.current_path + '/ico/'+self.iconID + '.png'

    self.notify()

  def notify(self):

    temp = subprocess.Popen(["notify-send -u critical 'Temperature in "+self.city_name+" is "+str(self.temp)+"C \n"+str(self.desc)+"'  -i "+self.full_path_ico+""], stdout=subprocess.PIPE, shell= True).communicate()[0]      

def main():
  root = Tk()
  app_gui = Gui(root)

  root.resizable(0,0)
  root.mainloop()
  
  
if __name__ == '__main__':
  main()
  
