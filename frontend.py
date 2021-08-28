from tkinter.constants import NO
from PIL import Image as im
import concurrent.futures as future
import cv2 as cv
import numpy as np
from pyautogui import *
from time import perf_counter as pc
from graphics import *
from button import *


class Frontend:
    def __init__(self, correct, pixel_width=1920, pixel_height=1080):
        self.correct = correct
        self.win = None
        self.pixel_width = pixel_width
        self.pixel_height = pixel_height
        self.increace_height = 0
        self.leftside_players_amount = 0
        self.players = 0
        self.y_const = 0
        self.x_const = 0
        self.visual_name = None
        self.visual_score = None
        self.visual_skilje = None
        self.magisk_siffra = 7  # 16-9 res ==> 9 delar i höjden ==> 7<9
        self.backround = []
        self.visual_question = None
        self.button_hight = 40
        self.button_width = 240

    def get_names(self):
        return self.correct.get_names()

    def get_sorted_by_skilje(self):
        return self.correct.get_sorted_by_skilje()

    # def get_one_correct_answers(self,question):
    #    return self.correct.get_one_correct_answers(question)
    def get_question_number(self):
        return self.correct.question_number

    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.correct_skilje.clicked(pt):
                return "Rätta skiljefråga"
            if self.next_question.clicked(pt):
                return "Nästa fråga"

    def create_window_score(self):
        win = GraphWin(
            "Poängtabell", self.pixel_width, self.pixel_height, autoflush=False
        )
        win.setCoords(0, 0, self.pixel_width, self.pixel_height)
        self.win = win
        self.players = len(self.get_names())
        line_middle = Line(
            Point(self.pixel_width / 2, self.pixel_height),
            Point(self.pixel_width / 2, 0),
        )
        line_middle.draw(self.win)
        self.leftside_players_amount = int(
            round(self.players / 2, 0)
        )  # vänstersidan av scoreboarden
        self.increace_height = self.magisk_siffra / self.leftside_players_amount
        self.y_const = self.pixel_height * 1 / 9
        for i in range(self.leftside_players_amount):
            y = self.pixel_height * (1 / 9 * (self.increace_height * i)) + self.y_const
            line = Line(Point(0, y), Point(self.pixel_width, y))
            line.draw(self.win)
        self.update_next_button(False)
        # self.next_question = Button(self.win, Point(self.pixel_width/2+self.pixel_width/8,self.pixel_height-self.y_const/2), self.button_width, self.button_hight, f"Rätta fråga {self.get_question_number()+1}")
        # self.next_question.activate()
        self.correct_skilje = Button(
            self.win,
            Point(
                self.pixel_width / 2 + 3 * self.pixel_width / 8,
                self.pixel_height - self.y_const / 2,
            ),
            self.button_width,
            self.button_hight,
            "Rätta skiljefråga",
        )
        self.correct_skilje.activate()
        self.display_visual_score()

    def update_next_button(self, at_end):
        if at_end == False:
            self.next_question = Button(
                self.win,
                Point(
                    self.pixel_width / 2 + self.pixel_width / 8,
                    self.pixel_height - self.y_const / 2,
                ),
                self.button_width,
                self.button_hight,
                f"Rätta fråga {self.get_question_number()+1}",
            )
            self.next_question.activate()
        else:
            self.next_question = Button(
                self.win,
                Point(
                    self.pixel_width / 2 + self.pixel_width / 8,
                    self.pixel_height - self.y_const / 2,
                ),
                self.button_width,
                self.button_hight,
                "Alla frågor är rättade",
            )
            self.next_question.deactivate()

    def update_skilje_button(self):
        self.correct_skilje = Button(
            self.win,
            Point(
                self.pixel_width / 2 + 3 * self.pixel_width / 8,
                self.pixel_height - self.y_const / 2,
            ),
            self.button_width,
            self.button_hight,
            "Skiljefråga rättad",
        )
        self.correct_skilje.deactivate()

    def display_visual_score(self, question_number=0):
        x = self.pixel_width / 16
        self.x_const = (
            self.pixel_width / 2 / 3
        )  # delar in halva och har både namn, score o skilje
        if self.visual_name != None:

            for i in range(self.players):
                self.visual_name[i].undraw()
                self.visual_score[i].undraw()
                self.visual_skilje[i].undraw()
                self.visual_question.undraw()
        self.visual_name = []
        self.visual_score = []
        self.visual_skilje = []

        self.visual_question = Text(
            Point(self.pixel_width / 4, self.pixel_height - self.y_const / 2),
            f"Fråga nummer {question_number}",
        )  # eftersom jag printar nedifrån vänster och upp
        self.visual_question.draw(self.win)
        for i in range(self.players):
            y = self.pixel_height - (
                self.pixel_height
                * (1 / 9 * (self.increace_height * i + self.increace_height / 2))
                + self.y_const
            )
            if i > self.leftside_players_amount - 1:
                y = self.pixel_height - (
                    self.pixel_height
                    * (
                        1
                        / 9
                        * (
                            self.increace_height * (i - self.leftside_players_amount)
                            + self.increace_height / 2
                        )
                    )
                    + self.y_const
                )
                x = self.pixel_width / 2 + self.pixel_width / 16

            self.visual_name.append(
                Text(Point(x, y), f"{self.get_sorted_by_skilje()[i][0]}")
            )  # eftersom jag printar nedifrån vänster och upp
            self.visual_score.append(
                Text(Point(x + self.x_const, y), f"{self.get_sorted_by_skilje()[i][1]}")
            )
            self.visual_skilje.append(
                Text(
                    Point(x + 2 * self.x_const, y),
                    f"{self.get_sorted_by_skilje()[i][2]}",
                )
            )

            name = self.get_sorted_by_skilje()[i][0]

            color = "black"
            try:
                if (
                    question_number != 0
                    and self.correct.corrected[name][question_number] == "correct"
                ):
                    color = "green"
                elif (
                    question_number != 0
                    and self.correct.corrected[name][question_number] == "wrong"
                ):
                    color = "red"
            except KeyError as ke:
                pass

            self.visual_name[-1].setFill(color)
            self.visual_score[-1].setFill(color)
            self.visual_skilje[-1].setFill(color)
            self.visual_name[i].draw(self.win)
            self.visual_score[i].draw(self.win)
            self.visual_skilje[i].draw(self.win)
