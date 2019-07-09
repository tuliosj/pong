import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from network import Network
from random import randint
import math

class GetOutOfLoop( Exception ):
    pass

class Player():
    width = 10
    height = 100

    def __init__(self, startx, starty, color, score):
        self.x = startx
        self.y = starty
        self.velocity = 5
        self.color = color
        self.score = score
        self.direction = 0

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)

    def move(self, dirn):
        if self.direction == dirn:
            self.velocity += 0.4
        else:
            self.velocity = 5
        if dirn == 0:
            self.y = round(self.y-self.velocity)
        else:
            self.y = round(self.y+self.velocity)
        self.direction = dirn

class Ball():
    width = 10
    height = 10

    def __init__(self, startx, starty, color):
        self.x = startx
        self.y = starty
        self.xv = 0
        while self.xv == 0:
            self.xv = randint(-4,4)
        self.yv = randint(-4,4)
        self.color = color

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)

class Game:
    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.canvas = Canvas(self.width, self.height, "Tela Principal")
        self.nome = ""
        self.clock = pygame.time.Clock()

    def run(self):
        try:
            if self.nome == "":
                self.nomear()
            # Após inserir o nome de usuário
            reply = self.clientList(str(self.net.id) + ":name:" + self.nome)
            oponente = self.listagem(reply)
            resposta = self.espera(oponente).split(";")
            match = Match(self.width, self.height, [resposta[0], self.nome], resposta[1], resposta[2])
            match.run()
            self.run()
        except GetOutOfLoop:
            pass
        
    def nomear(self):
        done = False
        while not done:
            self.clock.tick(20)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.destroy()
                        raise GetOutOfLoop
                    elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.nome = self.nome[:-1]
                    else:
                        self.nome += event.unicode

            self.canvas.draw_background()
            self.canvas.draw_text("Digite seu nome:", 24, 10, 0)
            pygame.draw.rect(self.canvas.get_canvas(), (200,50,50), (0, 35, self.width, 2), 0)
            self.canvas.draw_text(self.nome, 20, 10, 40)
            pygame.draw.rect(self.canvas.get_canvas(), (0,0,0) ,(self.width-90, self.height-50, 80, 40), 0)
            pygame.draw.rect(self.canvas.get_canvas(), (180,255,180) ,(self.width-85, self.height-45, 70, 30), 0)
            self.canvas.draw_text("Enter", 14, self.width-68, self.height-38)
            self.canvas.update()

    def listagem(self, reply):
        oponente = 0
        done = False
        while not done:
            self.clock.tick(15)
            qntClientes = len(reply)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.destroy()
                        raise GetOutOfLoop
                    elif event.key == pygame.K_F5:
                        reply = self.clientList(str(self.net.id) + ":refresh")
                    elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                        if qntClientes != 0:
                            return reply[oponente-1]
                    elif event.key == pygame.K_UP and oponente > 1:
                        oponente -= 1
                    elif event.key == pygame.K_DOWN and oponente < qntClientes:
                        oponente += 1
                    elif event.key == pygame.K_UP and oponente == 1:
                        oponente = qntClientes
                    elif event.key == pygame.K_DOWN and oponente == qntClientes:
                        oponente = 1

            self.canvas.draw_background()
            self.canvas.draw_text("Jogadores disponíveis", 24, 10, 0)
            pygame.draw.rect(self.canvas.get_canvas(), (200,50,50), (0, 35, self.width, 2), 0)
            for i,text in enumerate(reply):
                self.canvas.draw_text(text, 20, 40, 40+(i*20))
            if qntClientes != 0:
                if oponente == 0:
                    oponente = 1
                pygame.draw.circle(self.canvas.get_canvas(), (100,0,0), [15,32+(oponente*20)], 10)
            pygame.draw.rect(self.canvas.get_canvas(), (0,0,0) ,(self.width-180, self.height-50, 80, 40), 0)
            pygame.draw.rect(self.canvas.get_canvas(), (170,170,170) ,(self.width-175, self.height-45, 70, 30), 0)
            self.canvas.draw_text("F5", 14, self.width-150, self.height-38)
            pygame.draw.rect(self.canvas.get_canvas(), (0,0,0) ,(self.width-90, self.height-50, 80, 40), 0)
            pygame.draw.rect(self.canvas.get_canvas(), (180,255,180) ,(self.width-85, self.height-45, 70, 30), 0)
            self.canvas.draw_text("Enter", 14, self.width-68, self.height-38)
            self.canvas.update()

    def espera(self, oponente):
        done = False
        timer = 0
        while not done:
            self.clock.tick(30)
            timer += 1
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.destroy()
                        raise GetOutOfLoop
                    elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                        oponente = self.listagem(self.clientList(str(self.net.id) + ":refresh"))
                        timer = 0

            self.canvas.draw_background()
            self.canvas.draw_text("Esperando " + oponente.split(": ")[1] + "...", 24, 10, 0)
            pygame.draw.rect(self.canvas.get_canvas(), (200,50,50), (0, 35, self.width, 2), 0)
            self.canvas.draw_text("Pressione enter caso queira cancelar. Segundos passados: " + str(int(timer/30)), 20, 10, 40)
            pygame.draw.rect(self.canvas.get_canvas(), (0,0,0) ,(self.width-90, self.height-50, 80, 40), 0)
            pygame.draw.rect(self.canvas.get_canvas(), (180,255,180) ,(self.width-85, self.height-45, 70, 30), 0)
            self.canvas.draw_text("Enter", 14, self.width-68, self.height-38)
            self.canvas.update()
            reply = self.net.send(str(self.net.id) + ":wait:" + oponente.split(": ")[0])
            if reply!="nada":
                done = True
        done = False
        timer = 5
        while not done:
            self.clock.tick(1)
            timer -= 1
            self.canvas.draw_background()
            self.canvas.draw_text("Partida começará em " + str(timer), 24, 10, 0)
            pygame.draw.rect(self.canvas.get_canvas(), (200,50,50), (0, 35, self.width, 2), 0)
            self.canvas.update()
            if timer==0:
                done = True
        return reply


    def destroy(self):
        pygame.display.quit()
        pygame.quit()

    def clientList(self, data):
        reply = self.net.send(data)
        clientList = reply.split(";")
        for client in clientList[1:]:
            if(client.split(": ")[0] == clientList[0]):
                clientList.remove(client)
                clientList.remove(clientList[0])
                return clientList


class Match:
    maxscore = 5
    winner = 0

    def __init__(self, w, h, eu, ele, lado):
        self.net = Network()
        self.width = w
        self.height = h
        self.eu = eu
        self.ele = ele.split(":")
        self.lado = lado
        self.player = Player(0, 50, (255,0,0), 0)
        self.player2 = Player(self.width-10, 100, (0,255,0), 0)
        self.ball = Ball(self.width/2, self.height/2,(0,0,255))
        self.canvas = Canvas(self.width, self.height, "Pong! - Túlio Silva Jardim")

    def run(self):
        clock = pygame.time.Clock()
        done = False
        while not done:
            clock.tick(60)

            if self.winner != 0:
                done = True

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True

            keys = pygame.key.get_pressed()

            if self.lado == "1":
                if keys[pygame.K_UP]:
                    if self.player.y >= self.player.velocity and self.player.y > 0:
                        self.player.move(0)
                if keys[pygame.K_DOWN]:
                    if self.player.y <= self.height - self.player.velocity and self.player.y < self.height - self.player.height:
                        self.player.move(1)
            else:
                if keys[pygame.K_UP]:
                    if self.player2.y >= self.player2.velocity and self.player2.y > 0:
                        self.player2.move(0)
                if keys[pygame.K_DOWN]:
                    if self.player2.y <= self.height - self.player2.velocity and self.player2.y < self.height - self.player2.height:
                        self.player2.move(1)

            # Send Network Stuff
            if self.lado == "1":
                if self.winner != 0:
                    reply = self.net.send(str(self.net.id) + ":acabou:" + str(self.winner))
                else:
                    reply = self.net.send(str(self.net.id) + ":pos:" + str(self.player.y) + "," + str(int(self.ball.x)) + "," + str(int(self.ball.y)))
                split = reply.split(":")
                if len(split) > 1 and split[1] == "acabou":
                    done = True
                    self.winner = int(split[2])
                else:
                    self.player2.y = int(reply)
            else:
                if self.winner != 0:
                    reply = self.net.send(str(self.net.id) + ":acabou:" + str(self.winner))
                else:
                    reply = self.net.send(str(self.net.id) + ":pos:" + str(self.player2.y))
                split = reply.split(":")
                if len(split) > 1 and split[1] == "acabou":
                    done = True
                    self.winner = int(split[2])
                else:
                    reply = reply.split(":pos:")[0].split(",")
                    self.player.y = int(reply[0])
                    if len(reply) > 1:
                        self.ball.x = int(reply[1])
                        self.ball.y = int(reply[2])

            # Update Canvas 
            self.update()
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.ball.draw(self.canvas.get_canvas())
            if self.lado == "1":
                self.canvas.draw_text(self.eu[1], 30, self.width/4-30, self.height/10)
                self.canvas.draw_text(str(self.player.score)+"/"+str(self.maxscore), 20, self.width/4, 2*self.height/10)
                self.canvas.draw_text(self.ele[1], 30, 3*self.width/4-60, self.height/10)
                self.canvas.draw_text(str(self.player2.score)+"/"+str(self.maxscore), 20, 3*self.width/4-30, 2*self.height/10)
            else:
                self.canvas.draw_text(self.ele[1], 30, self.width/4-30, self.height/10)
                self.canvas.draw_text(str(self.player2.score)+"/"+str(self.maxscore), 20, self.width/4, 2*self.height/10)
                self.canvas.draw_text(self.eu[1], 30, 3*self.width/4-60, self.height/10)
                self.canvas.draw_text(str(self.player.score)+"/"+str(self.maxscore), 20, 3*self.width/4-30, 2*self.height/10)
            self.canvas.update()

        done = False
        clock = pygame.time.Clock()
        while not done:
            clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return self.net.send(str(self.net.id) + ":acabou:" + str(self.winner))
                    elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                        return str(self.net.id) + ":selfdelete"

            reply = self.net.send(str(self.net.id) + ":acabou:" + str(self.winner))

            # Update Canvas 
            self.update()
            self.canvas.draw_background()
            if (self.winner == 1 and self.lado == "1") or (self.winner == 2 and self.lado == "2"):
                self.canvas.draw_text("Vitória de "+self.eu[1]+"!", 24, 10, 0)
                self.canvas.image_center("venci.jpg", 160, 80)
            elif self.winner != 0:
                self.canvas.draw_text("Vitória de "+self.ele[1]+"!", 24, 10, 0)
                self.canvas.image_center("perdi.jpg", 160, 80)
            else:
                self.canvas.draw_text("A conexão foi finalizada!", 24, 10, 0)            
            pygame.draw.rect(self.canvas.get_canvas(), (200,50,50), (0, 35, self.width, 2), 0)
            pygame.draw.rect(self.canvas.get_canvas(), (0,0,0) ,(self.width-90, self.height-50, 80, 40), 0)
            pygame.draw.rect(self.canvas.get_canvas(), (180,255,180) ,(self.width-85, self.height-45, 70, 30), 0)
            self.canvas.draw_text("Enter", 14, self.width-68, self.height-38)
            self.canvas.update()

    def update(self):
        self.ball.x += self.ball.xv
        self.ball.y += self.ball.yv
        if((self.ball.y<self.player.width and self.ball.yv<0) or (self.ball.y>self.height and self.ball.yv>0)):
            self.ball.yv = -self.ball.yv

        # Se a bola bater no canto esquerdo
        if(self.ball.x<self.player.width):
            if(self.ball.y>self.player.y and self.ball.y<self.player.y+self.player.height):
                angulo = abs(self.ball.y-self.player.y-self.player.height/2)
                self.ball.xv = (2+angulo/12)
                self.ball.yv = angulo/7
            else:
                if self.lado == "1":
                    self.player2.score += 1
                else:
                    self.player.score += 1
                self.pointScored()

        # Se a bola bater no canto direito
        if(self.ball.x>self.width-self.player.width-self.ball.width):
            if(self.ball.y>self.player2.y and self.ball.y<self.player2.y+self.player2.height):
                angulo = abs(self.ball.y-self.player2.y-self.player2.height/2)
                self.ball.xv = -(2+angulo/12)
                self.ball.yv = -angulo/7
            else:
                if self.lado == "2":
                    self.player2.score += 1
                else:
                    self.player.score += 1
                self.pointScored()

    def pointScored(self):
        if (self.player.score >= self.maxscore):
            self.winner = 1
        elif (self.player2.score >= self.maxscore):
            self.winner = 2
        else:
            self.ball = Ball(self.width/2, self.height/2,(0,0,255))
            self.player = Player(self.player.x, int((self.width-self.player.height)/2), self.player.color, self.player.score)
            self.player2 = Player(self.player2.x, int((self.width-self.player2.height)/2), self.player2.color, self.player2.score)

class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.Font("lato.ttf", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.blit(render, (x,y))

    def image_center(self, filename, x, y):
        render = pygame.image.load(filename)
        self.screen.blit(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))
