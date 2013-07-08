#!/usr/bin/python

from json import load
from urllib2 import *
from Tkinter import *
import socket
from ast import literal_eval

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

    child = Child(self.city_name_1)

class Child(Main):
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

      #for line in (self.city['main']):
      print(self.city['main'])


    
def main():
  root = Tk()
  app_gui = Main(root)

  root.resizable(0,0)
  root.mainloop()
  
  
if __name__ == '__main__':
  main()
  
'''
http://proxylv.ericpol.int/epol.proxy

{u'pressure': 1027, u'temp_min': 24, u'temp_max': 25.149999999999999, u'temp': 24, u'humidity': 47}

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
