from PIL import Image as im
import os
import concurrent.futures as future
import cv2 as cv
import numpy as np
from pyautogui import *
from time import perf_counter as pc
from graphics import *


class ValueError(Exception):
    def __init__(self, arg):
        self.arg = arg


class FileNotFoundError(Exception):
    def __init__(self, arg):
        self.arg = arg


class Input:
    def __init__(
        self,
        width_cm=8.6,
        width_first_box=3.5,
        width_boxes=1.71,
        hight_cm=14.9,  # 14,3
        height_boxes=0.796,
        svarsalternativ=3,
        questions=14,
        picture_folderpath="bildbank7",
        file_name=r"svar\svar_22_8.txt",
        half_of_points=50,
    ):
        self.width_cm = width_cm
        self.width_first_box = width_first_box
        self.width_boxes = width_boxes
        self.hight_cm = (
            hight_cm  # 14.55 tänk på att appen lägger till vattenstämpel längst ned
        )
        self.height_boxes = height_boxes
        self.answers = {}  # {jonathan: {1:'x'...} simon:{1:2}}
        self.correct_answers = {}  # {1:x, ...} de rätta svaren
        self.svarsalternativ = svarsalternativ
        self.questions = questions
        self.X = []
        self.Y = []
        self.pixels_width_per_cm = 0
        self.pixels_height_per_cm = 0
        self.names = {}
        self.skilje = {}
        self.correct_skilje = 0
        self.picture_folderpath = picture_folderpath
        self.file_name = file_name
        self.half_of_points = half_of_points
        self.main_dir = os.getcwd()

    def get_names(self):
        return self.names

    def get_answers(self):
        return self.answers

    def set_input(self, image_name, question, svar, diff=None):
        if diff != None:
            diff = int(diff)
        ans = input(
            f"person {image_name} med diff {int(diff)} på fråga {question} \ninscanning säger {svar} skriv in rätta svaret "
        )
        if ans == "":
            self.answers[image_name][question] = svar
        elif ans == "x":
            self.answers[image_name][question] = ans
        else:
            self.answers[image_name][question] = int(ans)

    def get_picture_rgb(
        self, image_name
    ):  # släng in imagename varje gång man kallar på denna
        if image_name.endswith(".jpg"):

            self.set_names_and_ans(image_name)
            image = im.open(image_name)
            width, height = image.size
            self.pixels_width_per_cm = width / self.width_cm
            self.pixels_height_per_cm = height / self.hight_cm
            for m in range(
                self.svarsalternativ
            ):  # gör en lista med de x man bör gå igenom
                self.X.append(
                    self.pixels_width_per_cm
                    * (self.width_first_box + (m + 1 / 2) * self.width_boxes)
                )
            for i in range(self.questions):
                self.Y.append(
                    ((i + 1.5) * self.height_boxes) * self.pixels_height_per_cm
                )  # i ska börja på 0 o sluta 11
            rgb_image = image.convert("RGB")

            self.answers[image_name] = {}
            question = 1
            for y in self.Y:
                self._get_picture_rbg(image_name, rgb_image, y, question)
                question += 1
            self.Y = []
            self.X = []
            self.pixels_width_per_cm = 0
            self.pixels_height_per_cm = 0
            image.close()

    def _get_picture_rbg(self, image_name, rgb_image, y, question):
        i = 1
        min_rgb = None
        rgb_list = []
        for x in self.X:
            rgb = 0
            s1 = self.half_of_points  # antalet punkter
            punkter = 2 * s1 + 1  # t.ex om s1 = 1 ==> 1, 0, -1
            for m in range(
                -s1, s1 + 1
            ):  # nedan hittas först de x o y-värden och sedan kollas dessas rgb-värden.
                new_x = x + (
                    m * 1 / 3 * (1 / s1) * self.width_boxes * self.pixels_width_per_cm
                )  # kollar rgb från x-1/3*rutlängd
                new_y = y + (
                    m * 1 / 3 * (1 / s1) * self.height_boxes * self.pixels_height_per_cm
                )
                rgb += self.get_pixel_rgb(rgb_image, new_x, new_y)
            rgb = rgb / (
                3 * punkter
            )  # eftersom medelvärde mellan pantalet punkter och r,g,b
            rgb_list.append(rgb)
            if min_rgb == None or rgb < min_rgb:
                min_rgb = rgb
                svar = 1
                if i == 2:
                    svar = "x"
                elif i == 3:
                    svar = 2
                if (
                    question in self.answers[image_name]
                ):  # ifall den redan har besvarats har något gått snett
                    self.set_input(image_name, question, svar)

            i += 1
        min_rgb = min(rgb_list)
        rgb_list.remove(min_rgb)
        secound_min_rgb = min(rgb_list)
        # print(secound_min_rgb, "soucundminrgb")

        diff = secound_min_rgb - min_rgb
        # print(diff,image_name)
        max_diff = 10
        if diff < max_diff:
            self.set_input(image_name, question, svar, diff)
        else:
            self.answers[image_name][question] = svar  # sparar svaret

    # vit har rgb = 255, 255, 255 och det är nästan bara det på tipspromenadlappen som ej ifyllda.
    # de ifyllda är typ 100, 100, 100

    def get_pixel_rgb(self, rgb_image, x, y):
        r, g, b = rgb_image.getpixel((x, y))  # kollar pixeln
        a = r + g + b
        return a

    def load_picture(self):
        start = pc()  # startar en klocka
        try:
            picture_dir = os.path.join(
                self.main_dir, self.picture_folderpath
            )  # hittar mappen där bilderna är
            os.chdir(picture_dir)
            images_names = []
            images_names.append(os.listdir(picture_dir))
        except:
            raise FileNotFoundError(f"mappen {picture_dir} hittades inte")
        images_names = images_names[0]
        for image_name in images_names:
            self.get_picture_rgb(image_name)
        # with future.ProcessPoolExecutor() as ex:
        #    ex.map(self.get_picture_rgb, images_names)
        end = pc()
        print(f"Process took {round((end-start), 3)} secounds i input")

    def get_correct_txtanswers(self):
        try:
            lines = open(self.file_name, "r")  # öppnar txt-filen med svaren
            read_lines = lines.readlines()
            self.correct_answers = {}
            for line in read_lines:
                row = line.strip()
                new_row = row.split(":", 1)
                if new_row[0] == "skilje":
                    self.correct_skilje = new_row[1]
                else:
                    self.correct_answers[int(new_row[0])] = new_row[1]
        except:
            file_path = os.path.join(self.main_dir, self.file_name)
            raise FileNotFoundError(f"filen {file_path} hittades inte")

    def set_names_and_ans(self, image_name):
        image_name_splited = image_name.split("_")
        name_and_ans = image_name_splited[
            2
        ]  # hämtar namn och svar på skiljefrågan från filnamnet t.ex sfj_jonathan carlson 324.jpg
        try:
            firstname, lastname, ans = name_and_ans.split()
            ans = ans[:-4]
            firstname = firstname.capitalize()
            lastname = lastname.capitalize()
            name = firstname + " " + lastname
            self.names[image_name] = name
            self.skilje[image_name] = ans
        except:
            raise ValueError(
                f"22fel format på filnamn på fil {image_name}. \nFormatet ska vara t.ex sfj_jonathan carlson 324.jpg"
            )


"""(self, width_cm=8.25, width_first_box=3.35, width_boxes = 1.65, hight_cm = 15.04,height_boxes = 0.7667
                ,svarsalternativ=3, questions = 15, picture_folderpath = 'bildbank4', file_name = r"svar\svar_aslatorp.txt", half_of_points = 100):
        self.width_cm = width_cm"""
