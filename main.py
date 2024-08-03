import pgzrun
import random
WIDTH = 600
HEIGHT = 600


def calculate_distance(x1, y1, x2, y2):
    """
    使用勾股定理计算两个二维点之间的距离。

    参数:
    x1, y1 : float
        第一个点的x和y坐标。
    x2, y2 : float
        第二个点的x和y坐标。

    返回:
    distance : float
        两个点之间的距离。
    """
    # 计算两点在x轴和y轴上的距离差
    dx = x2 - x1
    dy = y2 - y1
    # 使用勾股定理计算距离
    distance = (dx ** 2 + dy ** 2) ** 0.5
    return distance


def elastic_collision_2d(mA, mB, vAx1, vAy1, vBx1, vBy1):
    """
    计算两个球在二维空间中的弹性碰撞后的速度。

    参数:
    mA, mB : float
        球A和球B的质量。
    vAx1, vAy1 : float
        球A碰撞前的x和y速度。
    vBx1, vBy1 : float
        球B碰撞前的x和y速度。

    返回:
    vAx2, vAy2, vBx2, vBy2 : float
        球A和球B碰撞后的x和y速度。
    """
    # x方向上的动量守恒
    total_momentum_x = mA * vAx1 + mB * vBx1
    vAx2 = (mA - mB) * vAx1 / (mA + mB) + 2 * mB * vBx1 / (mA + mB)
    vBx2 = (mB - mA) * vBx1 / (mA + mB) + 2 * mA * vAx1 / (mA + mB)

    # y方向上的动量守恒（与x方向类似，但速度在y方向上可能不同）
    total_momentum_y = mA * vAy1 + mB * vBy1
    vAy2 = (mA - mB) * vAy1 / (mA + mB) + 2 * mB * vBy1 / (mA + mB)
    vBy2 = (mB - mA) * vBy1 / (mA + mB) + 2 * mA * vAy1 / (mA + mB)

    return vAx2, vAy2, vBx2, vBy2
class Ball:
    def __init__(self,x,y,color,speed_x,speed_y,radius):
        self.x = x
        self.y = y
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = radius
    def draw(self):
        screen.draw.filled_circle((self.x,self.y),self.radius,self.color)
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
    def bounce(self):
        if self.x + self.radius > WIDTH or self.x - self.radius < 0:
            self.speed_x *= -1.0625
            self.x = WIDTH - self.radius if self.x + self.radius > WIDTH else self.radius
        if self.y + self.radius > HEIGHT or self.y - self.radius < 0:
            self.speed_y *= -1.0625
            self.y = HEIGHT - self.radius if self.y + self.radius > HEIGHT else self.radius
    def check_collision(self,other):
        distance = calculate_distance(self.x,self.y,other.x,other.y)
        if distance < self.radius + other.radius:
            return True
        return False
    def handle_collision(self,other):
        if self.check_collision(other):
            vAx2, vAy2, vBx2, vBy2 = elastic_collision_2d(self.radius/10, other.radius/10, self.speed_x, self.speed_y, other.speed_x, other.speed_y)
            self.speed_x, self.speed_y = vAx2, vAy2
            other.speed_x, other.speed_y = vBx2, vBy2
            self.radius-=10
            other.radius-=10
    def update(self):
        if self.radius < 0:
            self.radius = 0
        self.radius += 1
        if self.radius > 400:
            self.radius = 400
        if self.speed_x ** 2 + self.speed_y ** 2 > 700:
            self.speed_x *= 0.5
            self.speed_y *= 0.5
        if self.speed_x > 0:
            self.speed_x - 0.5
        elif self.speed_x < 0:
            self.speed_x + 0.5
        if self.speed_y > 0:
            self.speed_y - 0.5
        elif self.speed_y < 0:
            self.speed_y + 0.5
balls = []
bigger_index = 0
for i in range(10):
    balls.append(Ball(random.randint(0,WIDTH),random.randint(0,HEIGHT),random.choice(["red","blue","green","yellow"]),random.randint(-10,10),random.randint(-10,10),75))
def update():
    global bigger_index
    bigger = 0
    bigger_index = 0
    for ball in balls:
        ball.move()
        ball.bounce()
        ball.update()
        if ball.radius <= 10:
            balls.remove(ball)
        if ball.radius > bigger:
            bigger = ball.radius
            bigger_index = balls.index(ball)
        for other in balls:
            if ball != other:
                ball.handle_collision(other)
def draw():
    screen.fill((250,250,250))
    for ball in balls:
        ball.update()
        if ball.radius <= 10:
            balls.remove(ball)
        try:
            ball.draw()
            screen.draw.text(str(balls.index(ball)+1),center = (ball.x,ball.y),color = 'black')
        except:
            pass
    screen.draw.text('KING:' + str(bigger_index + 1),midtop = (300,0),color = 'black')
pgzrun.go()