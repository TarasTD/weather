from json import load
from urllib2 import urlopen
from Tkinter import *

class gui(Frame):
  def __init__(self, parent):
    self.city_name_base = StringVar()
    self.city_name_base.set('City name')
    Frame.__init__(self, parent, bg='White')
    self.parent = parent
    self.initUI()
    
  def initUI(self):
    self.parent.title("Weather checker 1.0")
    self.pack(fill=BOTH, expand=1)
    self.widgets()
    
  def widgets(self):
    self.entry_name = Entry(self.parent,width=30, textvariable = self.city_name_base)
    self.entry_name.pack()
  
    self.butt_apply = Button(self.parent, text='Submit', bg='Red', command=self.test)
    self.butt_apply.pack()
    
  def test(self):
    self.city_name = self.city_name_base.get()
    self.label_city = Label(self.parent, text=''+self.city_name)
    self.label_city.pack()
    

class weather(gui):
  def __init__(self, city_name):
    self.city_name = app_gui.city_name
    self.data = urlopen("http://openweathermap.org/data/2.1/find/name?q="+self.city_name+"")
    self.cities = load(self.data) 
    get_info()
    
  def get_info(self):
    if self.cities['count'] > 0:
      self.city = self.cities['list'][0]
      print(self.city['main'])
      print(self.city['weather'])

    for line in cities['list']:
      re.search()
    
def main():
  root = Tk()
  app_gui = gui(root)
  app = weather(city_name)
  
  root.mainloop()
  
  
if __name__ == '__main__':
  main()
  
'''
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
