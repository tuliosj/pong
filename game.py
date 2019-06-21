import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from network import Network


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


class Player():
    width = 10
    height = 100

    def __init__(self, startx, starty, color, score):
        self.x = startx
        self.y = starty
        self.velocity = 5
        self.color = color
        self.score = score

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
    maxscore = 5

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(0, 50, (255,0,0), 0)
        self.player2 = Player(self.width-self.player.width, 100, (0,255,0), 0)
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

                if event.type == pygame.K_ESCAPE:
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
            self.canvas.draw_text("Jogador 1:", 30, self.width/4-30, self.height/10)
            self.canvas.draw_text(str(self.player.score)+"/"+str(self.maxscore), 20, self.width/4, 2*self.height/10)
            self.canvas.draw_text("Jogador 2:", 30, 3*self.width/4-60, self.height/10)
            self.canvas.draw_text(str(self.player2.score)+"/"+str(self.maxscore), 20, 3*self.width/4-30, 2*self.height/10)
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
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
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.blit(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))
