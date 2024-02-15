import pygame
pygame.init()


WIDTH, HEIGHT = 700, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG GAME")

FPS = 60

ORANGE = (255, 150, 0)     
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 25)


###########################################################################################################
#---------------------------------CREATING A PADDLE CLASS-------------------------------------------------#

class Paddle:
    COLOR = ORANGE
    VEL = 4
    
    def __init__(self, x, y, paddle_width, paddle_height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.paddle_width = paddle_width
        self.paddle_height = paddle_height
        
    def draw(self, screen):
        pygame.draw.rect(
            screen, self.COLOR, (self.x, self.y, self.paddle_width, self.paddle_height))
        
    def moves(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
       
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        
        
###########################################################################################################
#---------------------------------CREATING A Ball CLASS---------------------------------------------------#

class Ball:
    MAX_VEL = 5
    BALL_COLOUR = ORANGE
    
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.BALL_COLOUR, (self.x, self.y), self.radius)    
   
    def moves(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1
        
        
###########################################################################################################
                   
def paddle_movement(keys, left_paddle, right_paddle, ball):
    """ A Function for MOVEMENT OF PADDLE """
    """ It takes keys: list/map as first argument & 
    two object of class Paddle as nxt two argument """
    
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.moves(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.paddle_height <= HEIGHT:
        left_paddle.moves(up=False)
                   
    # AI control for the right paddle
    # The right paddle will track the y position of the ball and move accordingly
    if ball.x_vel > 0:  # Only move if the ball is moving towards the right paddle
        if right_paddle.y + right_paddle.paddle_height / 2 < ball.y and right_paddle.y + right_paddle.paddle_height <= HEIGHT:
            right_paddle.moves(up=False)
        elif right_paddle.y + right_paddle.paddle_height / 2 > ball.y and right_paddle.y >= 0:
            right_paddle.moves(up=True)

                   
###########################################################################################################
  
def collision(ball, left_paddle, right_paddle):
    """ Function to bounce the ball from walls and paddles."""
    """ First argument: object of class Ball, 
    nxt two argument: objects of class Peddals"""
    
    """
    1. reverse(-1 * y_vel) the direction in y axis if it collide with horizontal wall.
    2. reverse(-1 * x_vel) the direction in x-axis if it collide with peddals.
    3. if it collide near center of peddals it bounce with minimum velocity(0) 
    & if it collide near edges it bounce with maximum velocity(5) in y-direction(only).
    NOTE: ball velocity in x axis remain same always, that is MAX_VEL = 5."""
    
    """ Reduction factor -
    the maximum distance from centre of peddal(i.e 50) / constant = MAX_VEL(5)
    50 / const = 5
    constant = reduction factor = 10"""
    
    #ball bounce from upper & lower wall
    if ball.y - ball.radius <= 0 or ball.y + ball.radius >=HEIGHT:
        ball.y_vel *= -1
   
   #ball bounce from left paddle with diff angle
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.paddle_height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.paddle_width :
                ball.x_vel *= -1
                
                middle_y = left_paddle.y + left_paddle.paddle_height / 2
                differnce_y = middle_y - ball.y
                reduction_factor = (left_paddle.paddle_height / 2) / ball.MAX_VEL 
                y_vel = differnce_y / reduction_factor  
                ball.y_vel = -1 * y_vel 
                
    #ball bounce from right paddle with diff angle            
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.paddle_height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1       
                
                middle_y = right_paddle.y + right_paddle.paddle_height / 2
                differnce_y = middle_y - ball.y
                reduction_factor = (right_paddle.paddle_height / 2) / ball.MAX_VEL 
                y_vel = differnce_y / reduction_factor 
                ball.y_vel = -1 * y_vel 
                
                
###########################################################################################################
  
def draw(screen, paddles, ball, left_score, right_score):
    """ Function to draw something and update it in display"""
    
    screen.fill(BLACK)
   
    left_score_text = SCORE_FONT.render(f'{left_score}', 1, ORANGE)
    right_score_text = SCORE_FONT.render(f'{right_score}', 1, ORANGE)
    screen.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    screen.blit(right_score_text, (3 * (WIDTH//4) - right_score_text.get_width()//2, 20))
     
    for paddle in paddles:
        paddle.draw(screen)
    
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(screen, ORANGE, (WIDTH//2 - 5, i, 10, HEIGHT//20))
      
    ball.draw(screen)
      
    pygame.display.update()


###########################################################################################################

  
def main():
    """ Main Function which contains Main loop"""
    run = True
    clock = pygame.time.Clock()
  
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH , HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, RADIUS)
    
    ai_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH , HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    left_score = 0
    right_score = 0
    
    #MAIN LOOP
    while run:
        clock.tick(FPS)
        # draw(SCREEN, [left_paddle, right_paddle], ball, left_score, right_score) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
           
        
        keys: list = pygame.key.get_pressed()   
        paddle_movement(keys, left_paddle, right_paddle, ball)
        
        
        
        ball.moves()
        collision(ball, left_paddle, right_paddle)   
        
        if ball.x < 0:
            right_score +=1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
            
        draw(SCREEN, [left_paddle, right_paddle], ball, left_score, right_score)     
    
        #displays who's winner and re-set everthing
        win = False
        left_win_text = "LOSSER"
        right_win_text = "LOSSER"
        if left_score >= 3:
            win = True
            left_win_text = "WINNER"
        elif right_score >= 3:
            win = True
            right_win_text = "WINNER"
           
             
        if win:
            left_text = SCORE_FONT.render(left_win_text, 1, ORANGE) 
            right_text = SCORE_FONT.render(right_win_text, 1, ORANGE) 
            SCREEN.blit(left_text, (WIDTH//4 - left_text.get_width()//2, HEIGHT//2 - left_text.get_height()//2))
            SCREEN.blit(right_text, (3 * (WIDTH//4) - right_text.get_width()//2, HEIGHT//2 - right_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            
            SCREEN.fill(BLACK)
            creator = SCORE_FONT.render("game by rakshi", 1, ORANGE)
            SCREEN.blit(creator, (WIDTH//2 - creator.get_width()//2, HEIGHT//2 - creator.get_height()//2))
            pygame.display.update()
            pygame.time.delay(500)
            
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
        
                
    pygame.quit()
     
     
     
if __name__ == '__main__':
    main()