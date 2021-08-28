from PIL import Image as im
import concurrent.futures as future
import cv2 as cv
import numpy as np
from pyautogui import *
from time import perf_counter as pc
from graphics import *
import operator


class Correct:
    def __init__(self, input):
        self.input = input
        self.score = {}
        self.corrected_skilje = {}
        self.corrected = {}  # huriva en person fick rätt eller fel på en fråga
        self.sorted_by_skilje = []
        self.question_number = 0

    def get_names(self):
        return self.input.get_names()

    def get_sorted_by_skilje(self):
        return self.sorted_by_skilje

    def get_one_correct_answers(self, question_number):
        self.question_number = question_number
        for image_name in self.input.answers:
            if question_number == 0:
                self.corrected[self.input.get_names()[image_name]] = {}
                self.score[image_name] = 0
            else:
                # print(str(self.input.correct_answers[question_number]))
                if str(self.input.answers[image_name][question_number]) == str(
                    self.input.correct_answers[question_number]
                ):
                    self.corrected[self.input.get_names()[image_name]][
                        question_number
                    ] = "correct"
                    self.score[image_name] += 1
                else:
                    self.corrected[self.input.get_names()[image_name]][
                        question_number
                    ] = "wrong"
        # print(self.score, "poäng")

    def get_correct_answers(
        self,
    ):  # ifall man är otolig och vill rätta allt samtidigt;)
        for image_name in self.input.answers:
            self.corrected[image_name] = {}
            self.score[image_name] = 0
            for question_number in self.input.correct_answers:
                if str(self.input.answers[image_name][question_number]) == str(
                    self.input.correct_answers[question_number]
                ):
                    self.corrected[image_name][question_number] = "correct"
                    self.score[image_name] += 1
                else:
                    self.corrected[image_name][question_number] = "wrong"
        # print(self.score, "score")

    def compare_skilje(self):
        # returnar kanske en dic med imagename:skillnad ifrån svaret.
        for image_name in self.input.answers:
            diff = abs(
                int(self.input.skilje[image_name]) - int(self.input.correct_skilje)
            )
            self.corrected_skilje[image_name] = diff

    def dont_compare_skilje(self):
        for image_name in self.input.answers:
            self.corrected_skilje[image_name] = int(self.input.skilje[image_name])

    def print_method(self):
        self.sorted_by_skilje = []
        sorted_by_value = dict(
            sorted(self.score.items(), key=operator.itemgetter(1), reverse=True)
        )
        self._print_method(True, sorted_by_value)
        i = 0
        for name_list in self.sorted_by_skilje:
            self.sorted_by_skilje[i][0] = self.input.get_names()[name_list[0]]
            i += 1

    def _print_method(self, bol, sorted_by_value):  # första sorteringen
        i = 1
        bol = False  # om man gått igenom en hel print_method utan att ändra ordning i listan är man klar och bol blir False.
        for image_name, score in sorted_by_value.items():
            if i == 1:
                self.sorted_by_skilje.append(
                    [image_name, score, self.corrected_skilje[image_name]]
                )
            else:
                if sorted_by_value[image_name] == self.sorted_by_skilje[i - 2][1]:
                    if (
                        self.corrected_skilje[image_name]
                        < self.sorted_by_skilje[i - 2][2]
                    ):
                        bol = True
                        last_sorted = self.sorted_by_skilje[i - 2]
                        self.sorted_by_skilje[i - 2] = [
                            image_name,
                            score,
                            self.corrected_skilje[image_name],
                        ]
                        self.sorted_by_skilje.append(last_sorted)
                    else:

                        self.sorted_by_skilje.append(
                            [image_name, score, self.corrected_skilje[image_name]]
                        )
                else:
                    self.sorted_by_skilje.append(
                        [image_name, score, self.corrected_skilje[image_name]]
                    )
            i += 1
        # print(self.sorted_by_skilje, "sorterat by skilje")
        return self._double_print_method(bol)

    def _double_print_method(
        self, bol
    ):  # ifall många har exakt samma poäng kan även denna behövas
        i = 1
        if (
            bol == False
        ):  # basfall i rekuriton ifall det inte ändrades nåt förra gången är vi klara
            return ""
        bol = False
        for image_list in self.sorted_by_skilje:
            image_name = image_list[0]
            score = image_list[1]
            skilje = image_list[2]
            if i != 1:
                if score == self.sorted_by_skilje[i - 2][1]:
                    if skilje < self.sorted_by_skilje[i - 2][2]:
                        bol = True
                        last_sorted = self.sorted_by_skilje[i - 2]
                        self.sorted_by_skilje[i - 2] = [
                            image_name,
                            score,
                            self.corrected_skilje[image_name],
                        ]
                        self.sorted_by_skilje[i - 1] = last_sorted
                else:
                    self.sorted_by_skilje[i - 1] = [
                        image_name,
                        score,
                        self.corrected_skilje[image_name],
                    ]
            i += 1
        return self._double_print_method(bol)
