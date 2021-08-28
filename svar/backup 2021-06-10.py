#from sys import last_value
from PIL import Image as im
import os
import concurrent.futures as future
import cv2 as cv
import numpy as np
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
from time import perf_counter as pc
from graphics import *

#gör set metod för manuell set av svar för de svaren som är oklara och gör automatiskt detta
#där rgb<220. kanske släng in svaren i txt fil så man kan rätta dom där?

# gör en knapp nästa fråga och när man trycker på den så rättas nästa fråga och scoreboarden uppdateras
# gör en separat mapp som man kan slänga in alla bildfiler i och läs ifrån dem.



# känn igen handstil namn och skiljefråga
# hitta storleken på bilden vilket gör att man kan ta bilden hur som helst. Gör detta
# genom att gå från mitten av bilden uppåt oh när man kommer till svart, gå till höger tills man kommer till vitt
# då har man nedre högra hörnet.
#gör mycket try och except. t.ex om man skriver in fel filnamn ska den säga vilket som är fel

class Tips:
    def __init__(self):
        self.file_name = "ratta_svar555.txt"
        self.pixel_rgb = None
        self.images = []
        self.width_cm = 8.25#9.5
        self.width_first_box = 3.35
        self.width_boxes = 1.65
        self.hight_cm = 15.04#14.55 tänk på att appen lägger till vattenstämpel längst ned 
        self.height_boxes = 0.7667
        self.answers = {} #{jonathan: {1:'x'...} simon:{1:2}}
        self.correct_answers = {} #{1:x, ...} de rätta svaren
        
        self.score = {}
        self.svarsalternativ = 3
        self.questions = 15

        self.X = []
        self.Y = []
        self.pixels_width_per_cm = 0
        self.pixels_height_per_cm = 0
        self.names = {}
        self.skilje = {}
        self.corrected_skilje = {}
        self.correct_skilje = 0

        self.corrected = {} #huriva en person fick rätt eller fel på en fråga.
        self.sorted_by_skilje = []
        self.win = None
        self.pixel_width = 1920
        self.pixel_height = 1080
        self.increace_height = 0
        self.leftside_players_amount = 0
        self.players = 0
        self.y_const = 0
        self.x_const = 0

        
    def get_picture_rgb(self, image_name): #släng in imagename varje gång man kallar på denna
        if image_name.endswith('.jpg'):
            self.set_names_and_ans(image_name)

            image = im.open(image_name)
            width, height = image.size
            self.pixels_width_per_cm = width/self.width_cm
            self.pixels_height_per_cm = height/self.hight_cm
            
            #self.X = [self.pixels_width_per_cm*4.2, self.pixels_width_per_cm*5.7, self.pixels_width_per_cm*7.4]
            for m in range(self.svarsalternativ):
                self.X.append(self.pixels_width_per_cm*(self.width_first_box+(m+1/2)*self.width_boxes))
            for i in range(self.questions):
                self.Y.append(((i+1.5)*self.height_boxes)*self.pixels_height_per_cm) #i ska börja på 0 o sluta 11
            #print(width, height ,"längd o höjd", image_name)
            rgb_image = image.convert('RGB')
            
            #print(image_name, "namnet")
           
            self.answers[image_name] = {}
            question = 1
            for y in self.Y:
                self._get_picture_rbg(image_name,0.4, rgb_image, y, question)
                question+=1
            self.Y = []
            self.X = []
            self.pixels_width_per_cm = 0
            self.pixels_height_per_cm = 0
      
            
    def _get_picture_rbg(self,image_name, threshold, rgb_image, y, question):
        i = 1
        #answerd = False
        #rgb_value = 255*threshold
        min_rgb = None
        for x in self.X:
            #print(x)
            
            #print(round(self.X/(self.pixels_width_per_cm), 2), "self.X")
            rgb = 0
            s1 = 100
            punkter = 2*s1+1
            for m in range(-s1,s1+1):
                new_x = x+(m*1/3*(1/s1)*self.width_boxes*self.pixels_width_per_cm)
                new_y = y+(m*1/3*(1/s1)*self.height_boxes*self.pixels_height_per_cm)
                rgb +=self.get_pixel_rgb(rgb_image, new_x, new_y)
            rgb = rgb/(3*punkter) #eftersom medelvärde mellan 3 rgb och r,g,b därav 9
            #print(rgb, "rgb", i, "i")
            if min_rgb == None or rgb<min_rgb:
                min_rgb = rgb
                svar = 1
                if i == 2:
                    svar='x'
                elif i == 3:
                    svar = 2
                if question in self.answers[image_name]:
                    print("FEEL fråga", question,"rgb = ", "säger att det är", svar)
                    pass
            #print("på fråga ", question, "har svarat " , svar)#, "med x= ",  x ,"o y= ", y )
         
            #print(r,"r", g,"g", b, "b",question, "fråga",  i, "svarsalternativ")
            #print(round(x/self.pixels_width_per_cm,2), round(y/(self.pixels_height_per_cm),2), "x,y och fråga", question)
            i += 1
        if min_rgb > 220:
            print("oskäker på fråga", question)
        #if answerd == False and i==4:
        #    print("ändrar threshold fråga", question)
        #    self._get_picture_rbg(image_name, threshold+0.1, rgb_image, y, question)
        self.answers[image_name][question] = svar
    
    def get_pixel_rgb(self, rgb_image, x,y):
        r,g,b = rgb_image.getpixel((x,y)) #kollar pixeln
        #print(r+g+b)
        a = r+g+b
        if a <2:#testa ta bort
            a = 255*3
        return a                 
            
# vit har 255 255 255 och det är nästan bara det på tipspromenadlappen.
# det svarta ifyllda är typ 135 men kan kolla på allt som är mindre än 200.
        

    def load_picture(self):
        images_names = []
        answers = []
        folder_path = os.getcwd()
        images_names.append(os.listdir(folder_path))
        images_names = images_names[0]
    
        for image_name in images_names:
            answers.append(self.get_picture_rgb(image_name))
        print(self.answers)
      
    def get_correct_answers(self):
        for image_name in self.answers:
            self.corrected[image_name] = {}
            self.score[image_name] = 0
            for question_number in self.correct_answers:
                #print(question_number, "frågenummer")
                #print(self.answers[image_name][question_number], "gissat")
                #print(self.correct_answers[question_number], "rätt svar")
                if str(self.answers[image_name][question_number]) == str(self.correct_answers[question_number]):
                    self.corrected[image_name][question_number] = 'correct'
                    self.score[image_name] +=1
                    #print("rätt",question_number)
                else:
                    self.corrected[image_name][question_number] = 'wrong'
                    #print("fel", question_number)
        print(self.score, "poäng")
        #print(self.corrected, "rättat")
        #print(self.names, "namn")
        #print(self.skilje, "ans")

        
    def get_correct_txtanswers(self):
        lines = open(self.file_name, 'r') 
        read_lines = lines.readlines()
        self.correct_answers = {}
        for line in read_lines: #går igenom alla rader i filen. line är varje rad
            row = line.strip()
            new_row = row.split(':', 1)
            if new_row[0] == "skilje":
                self.correct_skilje = new_row[1]
            else:
                self.correct_answers[int(new_row[0])]=new_row[1]

    def set_names_and_ans(self, image_name):
        image_name_splited = image_name.split('_')
        print(image_name_splited, "splittad namn")
        name_and_ans = image_name_splited[2]
        firstname, lastname, ans = name_and_ans.split()
        ans = ans[:-4]
        firstname = firstname.capitalize()
        lastname = lastname.capitalize()
        name = firstname + " " + lastname
        self.names[image_name] = name
        self.skilje[image_name] = ans
    
    def compare_skilje(self):
        #returnar kanske en dic med imagename:skillnad ifrån svaret.
        #givet är self.answers har alla imagenames
        #self.skilje har alla svaren
        for image_name in self.answers:
            diff = abs(int(self.skilje[image_name]) - int(self.correct_skilje))
            self.corrected_skilje[image_name] = diff

    def print_method(self):
        import operator
        sorted_by_value = dict(sorted(self.score.items(), key=operator.itemgetter(1),reverse=True))
        self._print_method(True, sorted_by_value)
        i = 0
        print(self.sorted_by_skilje, "sorted by skilje")
        for name_list in self.sorted_by_skilje:
            print(self.sorted_by_skilje[i], "sorted skilje")
            print(name_list, "[namelist]")
            print(self.names[name_list[0]], "self.name[namelist]")
            self.sorted_by_skilje[i][0] = self.names[name_list[0]]
            i +=1
        print(self.sorted_by_skilje)
    def _print_method(self, bol, sorted_by_value):
        
        print('Dictionary in descending order by value : ',sorted_by_value)
        i = 1
        bol = False
        for image_name, score in sorted_by_value.items():
            if i == 1:
                self.sorted_by_skilje.append([image_name, score, self.corrected_skilje[image_name]])
            else:
                #print(self.sorted_by_skilje, "skilje")
                #print(i-2, "i-2")
                if sorted_by_value[image_name] == self.sorted_by_skilje[i-2][1]:
                    if self.corrected_skilje[image_name] < self.sorted_by_skilje[i-2][2]:
                        bol = True
                        last_sorted = self.sorted_by_skilje[i-2]
                        self.sorted_by_skilje[i-2] = [image_name, score, self.corrected_skilje[image_name]]
                        self.sorted_by_skilje.append(last_sorted)
                    else:
                       
                        self.sorted_by_skilje.append([image_name, score, self.corrected_skilje[image_name]])
                else:
                    self.sorted_by_skilje.append([image_name, score, self.corrected_skilje[image_name]])
            i+=1
        #print(self.sorted_by_skilje, "sorterat by skilje")
        return self._double_print_method(bol)
    def _double_print_method(self,bol):
        i = 1
        if bol == False:#basfall i rekuriton ifall det inte ändrades nåt förra gången är vi klara
            return ""
        bol = False
        for image_list in self.sorted_by_skilje:    
            image_name = image_list[0]
            score = image_list[1]
            skilje = image_list[2]
            if i != 1:
                if score == self.sorted_by_skilje[i-2][1]:
                    if skilje < self.sorted_by_skilje[i-2][2]:     
                        bol = True
                        last_sorted = self.sorted_by_skilje[i-2]
                        self.sorted_by_skilje[i-2] = [image_name, score, self.corrected_skilje[image_name]]
                        self.sorted_by_skilje[i-1] = last_sorted
                else: 
                    self.sorted_by_skilje[i-1] = [image_name, score, self.corrected_skilje[image_name]]
            i+=1
        return self._double_print_method(bol)

    def create_window_score(self):
        win = GraphWin("Poäng" , self.pixel_width, self.pixel_height, autoflush=False)
        win.setCoords(0,0,self.pixel_width, self.pixel_height)
        self.win = win
        self.players = len(self.names)
        print(self.players, "players")
        #self.players = 40
        #gör specialfall för få players med endast i mitten
        line_middle = Line(Point(self.pixel_width/2, self.pixel_height) , Point(self.pixel_width/2,0))
        line_middle.draw(self.win)
        self.leftside_players_amount = int(round(self.players/2, 0))
        #rightside_players_amount = int(round(players-leftside_players_amount, 0))
        self.increace_height = 8/self.leftside_players_amount
        self.y_const = self.pixel_height*1/15
        for i in range(self.leftside_players_amount):
            y = self.pixel_height*(1/9*(self.increace_height*i))+self.y_const
            #lines.append(Line(Point(0, y),Point(self.pixel_width,y)))
            line = (Line(Point(0, y),Point(self.pixel_width,y)))
            line.draw(self.win)
        self.display_visual_score()

        
        

    def display_visual_score(self):
        x = self.pixel_width/16
        self.x_const = self.pixel_width/2/3 #delar in halva och har både namn, score o skilje
        for i in range(self.players):
            y = self.pixel_height*(1/9*(self.increace_height*i+self.increace_height/2))+self.y_const
            if i > self.leftside_players_amount-1:
                y = self.pixel_height*(1/9*(self.increace_height*(i-self.leftside_players_amount)+self.increace_height/2))+self.y_const
                x = self.pixel_width/2+self.pixel_width/16
            #self.leftside_players_amount-i-1
            visual_name = Text(Point(x, y), f"{self.sorted_by_skilje[self.leftside_players_amount-i-1][0]}") #eftersom jag printar nedifrån vänster och upp
            visual_score = Text(Point(x+self.x_const, y), f"{self.sorted_by_skilje[self.leftside_players_amount-i-1][1]}")
            visual_skilje = Text(Point(x+2*self.x_const, y), f"{self.sorted_by_skilje[self.leftside_players_amount-i-1][2]}")
            visual_name.draw(self.win)
            visual_score.draw(self.win)
            visual_skilje.draw(self.win)
        
    
if __name__ == "__main__":
    start = pc()#startar en klocka
    tips = Tips()
    #tips.set_correct_anwers()
    tips.get_correct_txtanswers()
    tips.load_picture()
    tips.get_correct_answers()
    tips.compare_skilje()
    tips.print_method()
    tips.create_window_score()
    inp = input("skriv nåt kul")
    end = pc()
    print(f"Process took {round((end-start)/10, 3)} secounds")
    
    

        
