# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import pygame.mixer
import sys
from qiskit import *
import time
import random

# input: int (0 or 1)
# output: int (0 or 1)
def x_gate(A):
   q = QuantumRegister(1)
   c = ClassicalRegister(1)
   qc = QuantumCircuit(q,c)
   inputdata = [A]
   if inputdata[0] == 1:
       qc.x(q[0])
   qc.x(q[0])
   qc.measure(q[0],c[0])
   backend = Aer.get_backend('qasm_simulator')
   job = execute(qc, backend, shots=1000)
   result = job.result()
   count =result.get_counts()
   answer = list(count.keys())[0]
   a=int(answer[0])
   return a

questions = [
    ["X", 0]
    ]

def AddCircuit(circuit,gate):
   if gate[0] == "H":
       circuit.h(gate[1])
   elif gate[0] == "CX":
       circuit.cx(gate[1],gate[2])
   elif gate[0] == "X":
       circuit.x(gate[1])
   elif gate[0] == "CZ":
       circuit.cz(gate[1],gate[2])

def solve_problem(tele):
   M = len(tele)
   answer = []
   for i in range(1, M+1):
       q = QuantumRegister(3)
       c = ClassicalRegister(3)
       circuit = QuantumCircuit(q,c)
       for j in range(i):
           AddCircuit(circuit, tele[j])
       backend = BasicAer.get_backend('statevector_simulator')
       job = execute(circuit, backend)
       result = job.result()
       outputstate = result.get_statevector(circuit, decimals=3)
       dict={}
       for j in range(len(outputstate)):
           if outputstate[j] != 0 and outputstate[j] > 0:
               if j == 0:
                   dict["000"] = "+"
               if j == 1:
                   dict["001"] = "+"
               if j == 2:
                   dict["010"] = "+"
               if j == 3:
                   dict["011"] = "+"
               if j == 4:
                   dict["100"] = "+"
               if j == 5:
                   dict["101"] = "+"
               if j == 6:
                   dict["110"] = "+"
               if j == 7:
                   dict["111"] = "+"
           if outputstate[j] != 0 and outputstate[j] < 0:
               if j == 0:
                   dict["000"] = "-"
               if j == 1:
                   dict["001"] = "-"
               if j == 2:
                   dict["010"] = "-"
               if j == 3:
                   dict["011"] = "-"
               if j == 4:
                   dict["100"] = "-"
               if j == 5:
                   dict["101"] = "-"
               if j == 6:
                   dict["110"] = "-"
               if j == 7:
                   dict["111"] = "-"
       answer.append(dict)
       dict = {}
   return answer

def evaluate(question, answer):
    if question[0] == "X":
        correct_answer = x_gate(question[1])
        if correct_answer == answer:
            return True
        else:
            return False

def CircleOrBatsu(is_correct, screen):
   if is_correct:
       pygame.draw.circle(screen, (255, 0, 0), (975, 260), 170, 30)
   else:
       pygame.draw.line(screen, (0, 0, 255), (825, 115), (1125, 415), 50)
       pygame.draw.line(screen, (0, 0, 255), (825, 415), (1125, 115), 50)
   time.sleep(1)
   pygame.display.update()
   time.sleep(1)

class Score():
    def __init__(self, x, y):
        self.sysfont = pygame.font.SysFont(None, 50)
        self.score = 0
        (self.x, self.y) = (x, y)
    def draw(self, screen):
        img = self.sysfont.render("SCORE: "+str(self.score), True, (20,20,20))
        screen.blit(img, (self.x, self.y))
    def add_score(self, x):
        self.score += x

class Title():
    def __init__(self, x, y):
        self.sysfont = pygame.font.SysFont(None, 60)
        (self.x, self.y) = (x, y)
    def draw(self, screen):
        img = self.sysfont.render("QQQ!", True, (0, 0, 0))
        screen.blit(img, (self.x, self.y))

class Picture():
    def __init__(self, file_name, x, y):
        self.image = pygame.image.load(file_name)
        rect_bg = self.image.get_rect()
        height = rect_bg[3]
        width = int(height * rect_bg[2] / rect_bg[3])
        self.image = pygame.transform.scale(self.image, (width, height))
        (self.x, self.y) = (x, y)
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Frame():
    def __init__(self, x0, y0, x1, y1):
        (self.x0, self.y0, self.x1, self.y1) = (x0, y0, x1, y1)
    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), Rect(self.x0, self.y0, 10, self.y1-self.y0))
        pygame.draw.rect(screen, (50, 50, 50), Rect(self.x1-10, self.y0, 10, self.y1-self.y0))
        pygame.draw.rect(screen, (50, 50, 50), Rect(self.x0, self.y0, self.x1-self.x0, 10))
        pygame.draw.rect(screen, (50, 50, 50), Rect(self.x0, self.y1-10, self.x1-self.x0, 10))

class AnswerBox():
    def __init__(self, x0, y0):
        (self.x0, self.y0) = (x0, y0)
    def draw(self, screen, answer_number):
        for i in range(answer_number):
            x2, y2 = self.x0 + i * 50, self.y0
            width, height = 40, 40
            pygame.draw.rect(screen, (50, 50, 50), Rect(x2, y2, width, height), 10)

class Transparent():
   def __init__(self, x0, y0, width, height, alpha):
       (self.x0, self.y0, self.width, self.height, self.alpha) = (x0, y0, width, height, alpha)
   def draw(self, screen, shift):
       s = pygame.Surface((self.width - shift, self.height))
       s.set_alpha(self.alpha)
       s.fill((255, 0, 0))
       screen.blit(s, (self.x0 - self.width + shift, self.y0))

class Underbar():
    def __init__(self, x, y, fontsize):
        self.sysfont = pygame.font.SysFont(None, fontsize)
        self.underbar = "_"
        (self.x, self.y) = (x, y)
    def draw(self, screen):
        img = self.sysfont.render(self.underbar, True, (20,20,20))
        screen.blit(img, (self.x, self.y))


class Input():
    def __init__(self, x, y, answer):
        self.sysfont = pygame.font.SysFont(None, 60)
        if answer == 0:
            self.input = 0
        else:
            self.input = 1
        (self.x, self.y) = (x, y)
    def draw(self, screen):
        img = self.sysfont.render(str(self.input), True, (20,20,20))
        screen.blit(img, (self.x, self.y))
        pygame.display.update()

def hadamard_gate1(A):
   q = QuantumRegister(1)
   c = ClassicalRegister(1)
   qc = QuantumCircuit(q,c)
   inputdata = [A]
   if inputdata[0] == 1:
       qc.x(q[0])
   qc.h(q[0])
   backend = BasicAer.get_backend('statevector_simulator')
   job = execute(qc, backend)
   result = job.result()
   outputstate = result.get_statevector(qc, decimals=3)
   answer_a = outputstate[0]
   answer_b = outputstate[1]
   dict = {}
   if answer_a == 0.707+ 0j:
       dict["0"] =  "+"
   if answer_b == -0.707 + 0j:
       dict["1"] = "-"
   else:
       dict["1"] = "+"
   return dict

def evaluateH(qubit, answer_dict):
   print ("correct_dict = %s" % hadamard_gate1(qubit))
   print ("answer_dict = %s" % answer_dict)
   if hadamard_gate1(qubit) == answer_dict:
      return True
   else:
      return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((1300, 800))
    pygame.display.set_caption('Qiskit Shooting')

    button0 = pygame.Rect(130, 160, 200, 200)
    button1 = pygame.Rect(430, 160, 200, 200)
    font = pygame.font.SysFont(None, 100)
    text0 = font.render('0', True, (50, 50, 50))
    text1 = font.render('1', True, (50, 50, 50))
    score = Score(500, 20)
    title = Title(20, 20)
    frame_game = Frame(70, 70, 700, 450)
    frame_question = Frame(750, 70, 1200, 450)
    frame_circuit = Frame(70, 500, 1200, 750)
    #answer_box = AnswerBox(850, 330)

    question_number = 0
    answer_number = 2

    #問題のリスト [ [問題(qiskitに送るもの), qubitの桁数, 解答枠の数のリスト, "+"と"-"のリスト, 問題の画像] , ... ]
    #question_list = [[[["X", 0]], 1, [1], ["+"], "x_gate0.png", "teleportation_circuit.png"]]
    question_list = [
                    [[["X", 0]], 1, [[1]], [["+"]], ["x_gate0.png"], "x0_circ.png"],
                    [[["X", 1]], 1, [[1]], [["+"]], ["x_gate1.png"], "x1_circ.png"],
                    [[["H", 0]], 1, [[2]], [["+","+"]], ["h_gate0.png"], "h0_circ.png"],
                    [[["H", 1]], 1, [[2]], [["+","-"]], ["h_gate1.png"], "h0_circ.png"],
                    [[["X",0],["H",1],["CX",1,2],["CX",0,1],["H",0],["CX",1,2],["CZ",0,2]], 3,
                    [1, 2, 2, 2, 4, 4, 4],
                    [["+"], ["+", "+"], ["+", "+"], ["+", "+"], ["+", "-", "+", "-"], ["+", "-", "+", "-"], ["+", "+", "+", "+"]],
                    ["teleportation0.png", "tereportation123.png", "tereportation123.png", "tereportation123.png", "tereportation45.png", "tereportation45.png", "teleportation6.png"], "teleportation_circuit.png"]
                    ]
    #question_list = ["x_gate0.png", "x_gate1.png", "h_gate0.png", "h_gate1.png"]
    #choose question randomly
    #question_num = random.randint(0, len(question_list) - 1)
    question_num = 0

    transparent = Transparent(670, 530, 370, 200, 100)
    count = 0
    answer_dict = {}
    input1 = []
    flag = 1

    while True:
        #アンダーバーの座標とサイズを設定  Underbar(x座標, y座標, フォントサイズ)
        step = 6
        if question_num != 4:
            step = 0
        question = Picture(question_list[question_num][4][step], 820, 150)
        circuit = Picture(question_list[question_num][5],150, 520)

        if question_num == 0 or question_num == 1:
            underbar = Underbar(998, 200, 70)
        if question_num == 2 or question_num == 3:
            underbar = Underbar(1002, 200, 70)
            underbar2 = Underbar(1086, 200, 70)
        if question_num == 4:
                #k = question_list[question_num][1] * question_list[question_num][2][step]
                #for i in range(k):

            if step == 0:
                underbar = Underbar(820, 200, 60)
                underbar2 = Underbar(850, 200, 60)
                underbar3 = Underbar(880, 200, 60)
            if step == 1 or step == 2 or step == 3:
                    #一つ目の枠
                underbar = Underbar(888, 200, 40)
                underbar2 = Underbar(908, 200, 40)
                underbar3 = Underbar(928, 200, 40)
                    #二つ目の枠
                underbar4 = Underbar(1005, 200, 40)
                underbar5 = Underbar(1025, 200, 40)
                underbar6 = Underbar(1045, 200, 40)
                #tereportation45.pngのheightを30に設定
            if step == 4 or step == 5 or step == 6 or step == 7:
                    #一つ目の枠
                underbar = Underbar(850, 200, 30)
                underbar2 = Underbar(864, 200, 30)
                underbar3 = Underbar(878, 200, 30)
                    #二つ目の枠
                underbar4 = Underbar(932, 200, 30)
                underbar5 = Underbar(946, 200, 30)
                underbar6 = Underbar(960, 200, 30)
                    #三つ目の枠
                underbar7 = Underbar(1014, 200, 30)
                underbar8 = Underbar(1028, 200, 30)
                underbar9 = Underbar(1042, 200, 30)
                    #四つ目の枠
                underbar10 = Underbar(1096, 200, 30)
                underbar11 = Underbar(1110, 200, 30)
                underbar12 = Underbar(1124, 200, 30)



        screen.fill((255, 255, 255))
        title.draw(screen)
        pygame.draw.rect(screen, (102, 149, 255), button0)
        pygame.draw.rect(screen, (255, 149, 102), button1)
        screen.blit(text0, (210, 225))
        screen.blit(text1, (510, 225))
        score.draw(screen)
        frame_game.draw(screen)
        frame_question.draw(screen)
        frame_circuit.draw(screen)
        #answer_box.draw(screen, answer_number)
        question.draw(screen)
        circuit.draw(screen)
        #アンダーバーを表示
        if question_num == 0 or question_num == 1:
            underbar.draw(screen)
        if question_num == 2 or question_num == 3:
            underbar.draw(screen)
            underbar2.draw(screen)
        if question_num == 4:
            if step >= 4:
                transparent.draw(screen,48*(step+1))
            else:
                transparent.draw(screen,48*step)
            if step == 0:
                underbar.draw(screen)
                underbar2.draw(screen)
                underbar3.draw(screen)
            if step == 1 or step == 2 or step == 3:
                underbar.draw(screen)
                underbar2.draw(screen)
                underbar3.draw(screen)
                underbar4.draw(screen)
                underbar5.draw(screen)
                underbar6.draw(screen)
            if step == 4 or step == 5 or step == 6 or step == 7:
                underbar.draw(screen)
                underbar2.draw(screen)
                underbar3.draw(screen)
                underbar4.draw(screen)
                underbar5.draw(screen)
                underbar6.draw(screen)
                underbar7.draw(screen)
                underbar8.draw(screen)
                underbar9.draw(screen)
                underbar10.draw(screen)
                underbar11.draw(screen)
                underbar12.draw(screen)


        if(count > 0):
            for i in range(count):
                #print("input1 = "+ str(input1))
                input1[i].draw(screen)

        for event in pygame.event.get():
           if event.type == QUIT:
               pygame.quit()
               sys.exit()
           if event.type == pygame.MOUSEBUTTONDOWN:
               if question_num == 0 or question_num == 1:
                   if button0.collidepoint(event.pos):
                       answer = 0
                       input = Input(1000, 200, answer)
                       input.draw(screen)
                       is_correct = evaluate(questions[question_number], answer)
                       CircleOrBatsu(is_correct, screen)
                       if is_correct:
                           print ("correct")
                           score.add_score(10)
                           input1 = []
                           answer_dict = {}
                           #question_num = random.randint(0, 3)
                           question_num = 3
                           flag = 0
                       else:
                           print ("incorrect")
                       answer_dict = {}
                   if button1.collidepoint(event.pos):
                       answer = 1
                       input = Input(1000, 200, answer)
                       input.draw(screen)
                       is_correct = evaluate(questions[question_number], answer)
                       CircleOrBatsu(is_correct, screen)
                       if is_correct:
                          print ("correct")
                          score.add_score(10)
                          input1 = []
                          print("input1 = " + str(input1))
                          #question_num = random.randint(0, 3)
                          question_num = 3
                          flag = 0
                       else:
                          print ("incorrect")
                       answer_dict = {}
               if question_num == 2 or question_num == 3:
                   if (flag != 0):
                       if button0.collidepoint(event.pos):
                           answer = 0
                           if count < 2:
                              input1.append(Input(1005 + 84 * count, 200, answer))
                              # for i in range(count+1):
                              #     print("i")
                              #     print(i)
                              #     input1[i].draw(screen)
                              # pygame.display.update()
                              print (count)
                              answer_dict[str(answer)] = question_list[question_num][3][0][count]
                              #print ("answer_dict = " + answer_dict)
                              if count == 1:
                                 for i in range(count+1):
                                    #print("input1 = "+ str(input1))
                                    input1[i].draw(screen)
                                 input1 = []
                                 is_correct = evaluateH(question_list[question_num][0][0][1], answer_dict)
                                 CircleOrBatsu(is_correct, screen)
                                 if is_correct:
                                    print ("correct")
                                    score.add_score(10)
                                    #question_num = random.randint(0, 3)
                                    question_num = 3
                                 else:
                                    print ("incorrect")

                                 count = 0
                                 answer_dict = {}
                                 break
                              count += 1
                       if button1.collidepoint(event.pos):
                           answer = 1
                           if count < 2:
                              input1.append(Input(1005 + 84 * count, 200, answer))
                              # for i in range(count+1):
                              #     print("i")
                              #     print(i)
                              #     input1[i].draw(screen)
                              # pygame.display.update()
                              # print (count)
                              # print("input1")
                              print("press1")
                              print(button1.collidepoint(event.pos))
                              print(button0.collidepoint(event.pos))
                              answer_dict[str(answer)] = question_list[question_num][3][0][count]
                              print ("answer_dict = " + str(answer_dict))
                              if count == 1:
                                 for i in range(count+1):
                                    #print("input1 = "+ str(input1))
                                    input1[i].draw(screen)
                                 input1 = []
                                 is_correct = evaluateH(question_list[question_num][0][0][1], answer_dict)
                                 CircleOrBatsu(is_correct, screen)
                                 if is_correct:
                                    print ("correct")
                                    score.add_score(10)
                                    #uestion_num = random.randint(0, 3)
                                    question_num = 3
                                 else:
                                    print ("incorrect")
                                 count = 0
                                 answer_dict = {}
                                 break
                              count += 1
                       print("count = "+ str(count))
               flag = 1

        pygame.display.update()


if __name__=="__main__":
    main()
