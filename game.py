import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from network import Network

class GetOutOfLoop( Exception ):
    pass

class Player():
    width = 10
    height = 100

    def __init__(self, startx, starty, color):
        self.x = startx
        self.y = starty
        self.velocity = 5
        self.color = color

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)

    def move(self, dirn):
        """
        :param dirn: 0 - 1 (up, down)
        :return: None
        """
        if dirn == 0:
            self.y -= self.velocity
        else:
            self.y += self.velocity

class Ball():
    width = 10
    height = 10

    def __init__(self, startx, starty, color):
        self.x = startx
        self.y = starty
        self.xv = 3
        self.yv = 3
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
            self.nomear()
            # Após inserir o nome de usuário
            reply = self.clientList(str(self.net.id) + ":name:" + self.nome)
            oponente = self.listagem(reply)
            resposta = self.espera(oponente).split(";")
            match = Match(self.width, self.height, [resposta[0],self.nome], resposta[1], resposta[2])
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
        oponente = 1
        done = False
        while not done:
            self.clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    qntClientes = len(reply)
                    if event.key == pygame.K_ESCAPE:
                        self.destroy()
                        raise GetOutOfLoop
                    elif event.key == pygame.K_F5:
                        reply = self.clientList(str(self.net.id) + ":refresh")
                    elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
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
            self.clock.tick(60)
            timer += 1/60
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
            self.canvas.draw_text("Pressione enter caso queira cancelar. Segundos passados: " + str(int(timer)), 20, 10, 40)
            pygame.draw.rect(self.canvas.get_canvas(), (0,0,0) ,(self.width-90, self.height-50, 80, 40), 0)
            pygame.draw.rect(self.canvas.get_canvas(), (180,255,180) ,(self.width-85, self.height-45, 70, 30), 0)
            self.canvas.draw_text("Enter", 14, self.width-68, self.height-38)
            self.canvas.update()
            reply = self.net.send(str(self.net.id) + ":wait:" + oponente[0])
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
                #clientList.remove(client)
                clientList.remove(clientList[0])
                return clientList


class Match:
    maxscore = 5

    def __init__(self, w, h, eu, ele, lado):
        self.net = Network()
        self.width = w
        self.height = h
        self.eu = eu
        self.ele = ele.split(":")
        if lado == 1:
            self.player = Player(0, 50, (255,0,0), 0)
            self.player2 = Player(self.width-10, 100, (0,255,0), 0)
        else:
            self.player2 = Player(0, 50, (255,0,0), 0)
            self.player = Player(self.width-10, 100, (0,255,0), 0)
        self.ball = Ball(self.width/2, self.height/2,(0,0,255))
        self.canvas = Canvas(self.width, self.height, "Testing...")

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity and self.player.y > 0:
                    self.player.move(0)

            if keys[pygame.K_DOWN]:
                if self.player.y <= self.height - self.player.velocity and self.player.y < self.height - self.player.height:
                    self.player.move(1)

            # Send Network Stuff
            self.player2.x, self.player2.y = self.parse_data(self.send_data())

            # Update Canvas
            self.update()
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.ball.draw(self.canvas.get_canvas())
            self.canvas.draw_text(eu[1], 30, self.width/4-30, self.height/10)
            self.canvas.draw_text(str(self.player.score)+"/"+str(self.maxscore), 20, self.width/4, 2*self.height/10)
            self.canvas.draw_text(ele[1], 30, 3*self.width/4-60, self.height/10)
            self.canvas.draw_text(str(self.player2.score)+"/"+str(self.maxscore), 20, 3*self.width/4-30, 2*self.height/10)
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":pos:" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0

    def update(self):
        self.ball.x += self.ball.xv
        self.ball.y += self.ball.yv
        if((self.ball.y<self.player.width and self.ball.yv<0) or (self.ball.y>self.height and self.ball.yv>0)):
            self.ball.yv = -self.ball.yv

        if(self.ball.x<0):
            if(self.ball.y>self.player.y and self.ball.y<self.player.y+self.player.height):
                self.ball.xv = -self.ball.xv
                self.ball.yv = 0.3*(self.ball.y-(self.player.y+self.player.height)/2)
            else:
                self.player2.score += 1
                self.ball = Ball(self.width/2, self.height/2,(0,0,255))
                self.player = Player(0, self.height/2, self.player.color, self.player.score)
                self.player2 = Player(self.width-self.player.width, self.height/2, self.player.color, self.player2.score)

        if(self.ball.x>self.width):
            if(self.ball.y>self.player2.y and self.ball.y<self.player2.y+self.player2.height):
                self.ball.xv = -self.ball.xv
                self.ball.yv = 0.3*(self.ball.y-(self.player2.y+self.player2.height)/2)
            else:
                self.player.score += 1
                self.ball = Ball(self.width/2, self.height/2,(0,0,255))


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

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))
