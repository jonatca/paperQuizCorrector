from input import *
from correct import *
from frontend import *

# gör try och except. t.ex om man skriver in fel filnamn ska den säga vilket som är fel

# gör som kahoot en ruta med mest intressant fakta t.ex många gissade fel eller många gissade rätt eller att någon har haft rätt
# många gånger i rad eller stegat flest steg på listan

# känn igen handstil namn och skiljefråga

# hitta storleken på bilden vilket gör att man kan ta bilden hur som helst. Gör detta
# genom att gå från mitten av bilden uppåt oh när man kommer till svart, gå till höger tills man kommer till vitt
# då har man nedre högra hörnet.


def main():
    skilje_corrected = False
    questions = 14
    start = pc()  # startar en klocka
    input_data = Input()
    input_data.get_correct_txtanswers()

    try:
        input_data.load_picture()
        correct = Correct(input_data)
        correct.get_one_correct_answers(0)
        correct.dont_compare_skilje()
        correct.print_method()
        end = pc()
        print(f"Process took {round((end-start), 3)} secounds i main")
        frontend = Frontend(correct)
        frontend.create_window_score()
        question = 1
        question_at_end = False
        while question <= questions:
            if frontend.interact() == "Nästa fråga":
                correct.get_one_correct_answers(question)
                if skilje_corrected:
                    correct.compare_skilje()
                else:
                    correct.dont_compare_skilje()
                correct.print_method()
                frontend.display_visual_score(question)
                if question < questions:
                    frontend.update_next_button(question_at_end)
                else:
                    question_at_end = True
                    frontend.update_next_button(question_at_end)
                question += 1
            elif frontend.interact() == "Rätta skiljefråga":
                correct.compare_skilje()
                correct.print_method()
                frontend.display_visual_score(question)
                skilje_corrected = True
                frontend.update_skilje_button()
        while True:
            if frontend.interact() == "Rätta skiljefråga":
                correct.compare_skilje()
                correct.print_method()
                frontend.display_visual_score(question - 1)
                skilje_corrected = True
                frontend.update_skilje_button()
    except ValueError as ve:
        print("ValueError:", ve.arg)
    except GraphicsError as gp:
        # print(gp.arg)
        if "getMouse in closed window" in gp.args:
            print("Hejdå")
        else:
            print("GraphicsError", gp.args)
    except KeyboardInterrupt as ki:
        print("Hejdå")
    except FileNotFoundError as fnf:
        print("FileNotFoundError", fnf.arg)
    except ZeroDivisionError as zd:
        print("ZeroDivistionError: varje gång du delar med noll dör en kattunge!!:(")


main()
