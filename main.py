#!/usr/bin/python

from json import load
from urllib2 import *
from Tkinter import *
import socket
from ast import literal_eval
import subprocess
import os

class Connection_timed_out():
  def __init__(self, arg):
    self.srgs = arg

class Main(Frame):
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
    
#    self.city_name_1 = 'london'    # just for testing delete afterwards

    child = Child(self.city_name_1)

class Child(Main):
  def __init__(self, city_name_1):
    self.city_name = city_name_1
    self.fetch_raw()

  def fetch_raw(self):
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
#      self.humidity = (self.city['main']['humidity'])  sometime there is HM smt not
  
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
    self.full_path_ico = ''
#    self.proxy = ProxyHandler({'http': '172.17.35.1:8080'})    #just comment 3 lines if you don't use proxy
#    self.opener = build_opener(self.proxy)
#    install_opener(self.opener)

    self.img_path = r'./ico'
    if not os.path.exists(self.img_path): os.makedirs(self.img_path)
    self.img = open(''+self.img_path+'/'+self.iconID+'.png', 'w')
    self.img.write(urlopen('http://openweathermap.org/img/w/'+self.iconID+'.png').read())
    self.img.close()

    self.current_path = os.getcwd()
    self.full_path_ico = self.current_path + '/ico/'+self.iconID + '.png'

    self.notify()

  def notify(self):
    temp = subprocess.Popen(["notify-send -u critical 'Temperature in "+self.city_name+"' "+str(self.temp)+" -i "+self.full_path_ico+""], stdout=subprocess.PIPE, shell= True).communicate()[0]      
      
    temp = subprocess.Popen(["notify-send 'Weather in "+self.city_name+"' "+str(self.desc)+" "], stdout=subprocess.PIPE, shell= True).communicate()[0]



def main():
  root = Tk()
  app_gui = Main(root)

  root.resizable(0,0)
  root.mainloop()
  
  
if __name__ == '__main__':
  main()
  
'''
[{ JUST FOR TEST
u'main': u'Clouds', 
u'id': 803, 
u'icon': u'04d', 
u'description': 
u'broken clouds'
}]


http://proxylv.ericpol.int/epol.proxy

{
u'pressure': 1027, 
u'temp_min': 24, 
u'temp_max': 25.149999999999999, 
u'temp': 24, 
u'humidity': 47
}

{u'humidity': 81,
u'pressure': 1012,
u'temp': 281.8,
u'temp_max': 283.71,
u'temp_min': 280.15}
[{u'description': u'light rain',
u'icon': u'10d',
u'id': 500,
u'main': u'Rain'},
{u'description': u'light intensity drizzle',
u'icon': u'09d',
u'id': 300,
u'main': u'Drizzle'}]'''
