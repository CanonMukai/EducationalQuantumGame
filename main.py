# -*- coding:utf-8 -*- 
import pygame
from pygame.locals import *
import pygame.mixer
import sys
from qiskit import *
import time

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
   qc.draw(output='mpl')
   answer = list(count.keys())[0]
   a=int(answer[0])
   return a

questions = [
    ["X", 0]
    ]

def evaluate(question, answer):
    if question[0] == "X":
        correct_answer = x_gate(question[1])
        if correct_answer == answer:
            return True
        else:
            return False

def CircleOrBatsu(is_correct, screen):
    if is_correct:
        pygame.draw.circle(screen, (255, 0, 0), (800, 200), 10, 30)
    #else:
        #pygame.draw.line(screen, (0, 0, 255), (800, 200), 
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
        img = self.sysfont.render("Qiskit Shooting Game", True, (0, 0, 0))
        screen.blit(img, (self.x, self.y))

class Picture():
    def __init__(self, file_name, x, y):
        self.image = pygame.image.load(file_name)
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
"""
class Question():
    def __init__(self, question):
        self.qestion = question
    def draw(self, screen):
"""
        
def main():
    pygame.init()
    screen = pygame.display.set_mode((1300, 800))
    pygame.display.set_caption('Qiskit Shooting')

    button0 = pygame.Rect(100, 200, 200, 200)
    button1 = pygame.Rect(400, 200, 200, 200)
    font = pygame.font.SysFont(None, 25)
    text0 = font.render('0', True, (50, 50, 50))
    text1 = font.render('1', True, (50, 50, 50))
    score = Score(500, 20)
    title = Title(20, 20)
    frame_game = Frame(70, 70, 700, 450)
    frame_question = Frame(750, 70, 1200, 450)
    frame_circuit = Frame(70, 500, 1200, 750)
    answer_box = AnswerBox(850, 330)

    question_number = 0
    answer_number = 2

    while True:
        screen.fill((255, 255, 255))
        title.draw(screen)
        pygame.draw.rect(screen, (100, 100, 200), button0)
        pygame.draw.rect(screen, (100, 100, 200), button1)
        screen.blit(text0, (200, 300))
        screen.blit(text1, (500, 300))
        score.draw(screen)
        frame_game.draw(screen)
        frame_question.draw(screen)
        frame_circuit.draw(screen)
        answer_box.draw(screen, answer_number)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button0.collidepoint(event.pos):
                    answer = 0
                    is_correct = evaluate(questions[question_number], answer)
                    CircleOrBatsu(is_correct, screen)
                if button1.collidepoint(event.pos):
                    answer = 1
                    is_correct = evaluate(questions[question_number], answer)
                    CircleOrBatsu(is_correct, screen)
                    if is_correct:
                        print ("correct")
                        
                    else:
                        print ("incorrect")

if __name__=="__main__":
    main()

