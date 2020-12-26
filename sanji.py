import pygame
import csv
import random

# Init pygame
pygame.init()

# Screen
HEIGHT = 700
WIDTH = 500

PADDING_TOP = 100
PADDING_BOTTOM = 100
PADDING_BETWEEN_COLUMNS = 10
PADDING_BETWEEN_ROWS = 10
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Sanjijukugo")

# Chips
CHIP_W = 60
CHIP_H = 60
CHIP_PAD = 7
CHIP_COLORS = ["#000000","#eeeeee","#aaee00","#888888","#000000"]

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (200,200,200)


def draw_text(x_pos, y_pos, text, size, color):
    '''pos coordinates begins in upper left corner of text box'''
    font1 = pygame.font.Font('fonts/ipaexg.ttf', size)
    img = font1.render(text, True, color)
    win.blit(img, (x_pos,y_pos))


def gen_juku_sample_list(level):
    n = 4 + level*2
    with open('jukugo.csv', newline='', encoding='utf-8') as f:
        reader  = csv.reader(f)
        juku_list = [x for x in reader][0]
    return random.sample(juku_list, n)


def gen_shuffled_grid(juku_sample_list):
    new_list = []
    for word in juku_sample_list:
        new_list.append(word[0])
        new_list.append(word[1])
        new_list.append(word[2])
    random.shuffle(new_list)
    return_list = []
    for i in range(int(len(new_list) / 3)):
        return_list.append([new_list[0 + i*3], new_list[1 + i*3], new_list[2 + i*3]])
    return return_list

def get_cols(level):
    if level == 0:
        return 4
    elif level == 1:
        return 6
    elif level == 2:
        return 4
    elif level == 3:
        return 5
    else:
        return 6

def get_rows(level):
    if level == 0:
        return 1
    elif level == 1:
        return 1
    elif level == 2:
        return 2
    elif level == 3:
        return 2
    else:
        return 2


class Stage:
    def __init__(self, level):
        self.level = level
        self.num_cols = get_cols(level)
        self.num_rows = get_rows(level)
        self.juku = gen_juku_sample_list(level)
        self.grid = gen_shuffled_grid(self.juku)
        self.marked_positions = []
        self.kanji_pos_array = self.gen_kanji_pos_array()
        print(f"self.juku: {self.juku}\nself.grid: {self.grid}")

    def gen_kanji_pos_array(self):
        re_array = []
        corner_x_left = WIDTH/2 - (CHIP_W*self.num_cols/2 + PADDING_BETWEEN_COLUMNS*(self.num_cols/2 - 1) + PADDING_BETWEEN_COLUMNS/2)
        corner_y_up = HEIGHT/2 - CHIP_H*(1.5 + 2*(self.num_rows - 1))
        for i in range(len(self.grid)): # column
            if i >= self.num_cols:
                for j in range(len(self.grid[i])): # print kanjis in second row
                    pos = (corner_x_left + (i%self.num_cols)*(PADDING_BETWEEN_COLUMNS + CHIP_W), corner_y_up + j*(CHIP_H) + 4*CHIP_H)
                    re_array.append(pos) # add coordinate to list
            else:
                for j in range(len(self.grid[i])): # print kanjis in first row
                    pos = (corner_x_left + i*(PADDING_BETWEEN_COLUMNS + CHIP_W), corner_y_up + j*(CHIP_H))
                    re_array.append(pos) # add coordinate to list
        return re_array

    def draw(self):
        # info text
        draw_text(30, 30,"LEVEL " + str(self.level + 1) + "/5",32,"#444444")
        if self.level == 0:
            draw_text(60, HEIGHT - 30, "漢字を入れ替えて三字熟語を完成させよう！", 20, '#444444')
        
        # calculate corners of box containing columns and rows
        corner_x_left = WIDTH/2 - (CHIP_W*self.num_cols/2 + PADDING_BETWEEN_COLUMNS*(self.num_cols/2 - 1) + PADDING_BETWEEN_COLUMNS/2)
        corner_x_right = WIDTH/2 + (CHIP_W*self.num_cols/2 + PADDING_BETWEEN_COLUMNS*(self.num_cols/2 - 1) + PADDING_BETWEEN_COLUMNS/2)
        corner_y_up = HEIGHT/2 - CHIP_H*(1.5 + 2*(self.num_rows - 1))
        corner_y_down = HEIGHT/2 + CHIP_H*(1.5 + 2*(self.num_rows - 1))

        # draw help box
        #pygame.draw.line(win, GRAY, (0, corner_y_up), (WIDTH, corner_y_up), 1)
        #pygame.draw.line(win, GRAY, (0, corner_y_down), (WIDTH, corner_y_down), 1)
        #pygame.draw.line(win, GRAY, (corner_x_left, 0), (corner_x_left, HEIGHT), 1)
        #pygame.draw.line(win, GRAY, (corner_x_right, 0), (corner_x_right, HEIGHT), 1)

        # draw all columns and rows (relative to upper left corner)
        for i in range(self.num_cols): # rör i sidled åt höger
            for j in range(self.num_rows*4): # rör i höjdled nedåt
                # horizontal lines
                pygame.draw.line(win, BLACK, ((corner_x_left + i*(PADDING_BETWEEN_COLUMNS + CHIP_W)),          corner_y_up + j*CHIP_H),
                                             ((corner_x_left + i*(PADDING_BETWEEN_COLUMNS + CHIP_W)) + CHIP_W, corner_y_up + j*CHIP_H))
                # vertical lines
                pygame.draw.line(win, BLACK, ((corner_x_left+i*(PADDING_BETWEEN_COLUMNS + CHIP_W)),          corner_y_up),
                                             ((corner_x_left+i*(PADDING_BETWEEN_COLUMNS + CHIP_W)),          corner_y_up + 3*CHIP_H))
                pygame.draw.line(win, BLACK, ((corner_x_left+i*(PADDING_BETWEEN_COLUMNS + CHIP_W)) + CHIP_W, corner_y_up), 
                                             ((corner_x_left+i*(PADDING_BETWEEN_COLUMNS + CHIP_W)) + CHIP_W, corner_y_up + 3*CHIP_H))
                if self.num_rows == 2:
                    pygame.draw.line(win, BLACK, ((corner_x_left+i*(PADDING_BETWEEN_COLUMNS + CHIP_W)),          corner_y_up + 4*CHIP_H),
                                                 ((corner_x_left+i*(PADDING_BETWEEN_COLUMNS + CHIP_W)),          corner_y_up + 7*CHIP_H))
                    pygame.draw.line(win, BLACK, ((corner_x_left+i*(PADDING_BETWEEN_COLUMNS + CHIP_W)) + CHIP_W, corner_y_up + 4*CHIP_H), 
                                                 ((corner_x_left+i*(PADDING_BETWEEN_COLUMNS + CHIP_W)) + CHIP_W, corner_y_up + 7*CHIP_H))

        # draw kanjis (relative to upper left corner)
        for i in range(len(self.grid)): # column
            if i >= self.num_cols:
                for j in range(len(self.grid[i])): # print kanjis in second row
                    pos = (corner_x_left + (i%self.num_cols)*(PADDING_BETWEEN_COLUMNS + CHIP_W) + CHIP_PAD, corner_y_up + j*(CHIP_H) + CHIP_PAD + 4*CHIP_H)
                    draw_text(pos[0], pos[1], self.grid[i][j], CHIP_W - 2*CHIP_PAD, BLACK) # paint kanji
            else:
                for j in range(len(self.grid[i])): # print kanjis in first row
                    pos = (corner_x_left + i*(PADDING_BETWEEN_COLUMNS + CHIP_W) + CHIP_PAD, corner_y_up + j*(CHIP_H) + CHIP_PAD)
                    draw_text(pos[0], pos[1], self.grid[i][j], CHIP_W - 2*CHIP_PAD, BLACK) # paint kanji


def click(s):
    # Mouse pos
    m_x, m_y = pygame.mouse.get_pos()
    print(f"Click! x pos is: {m_x}, y pos is: {m_y}")
    for i in range(len(s.kanji_pos_array)): # 0 till 11 om len = 12
        if m_x > s.kanji_pos_array[i][0] and m_x < (s.kanji_pos_array[i][0] + CHIP_W):
            if m_y > s.kanji_pos_array[i][1] and m_y < (s.kanji_pos_array[i][1] + CHIP_H):
                print(f"A click was registered on tile no: {i}")



def render(s):
    win.fill(WHITE)
    s.draw()
    pygame.display.update()


def main():
    s = Stage(0) # Init stage
    run = True # Turn on game

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(s)

        render(s) # Run update sequence

        # if correct_sequence
        # if all_correct


while True:
    if __name__ == '__main__':
        main()