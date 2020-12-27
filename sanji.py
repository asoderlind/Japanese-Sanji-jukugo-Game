'''A kanji game made in python'''
import csv
import random
import pygame

# Init pygame
pygame.init()

# Screen
HEIGHT = 700
WIDTH = 500

PADDING_TOP = 100
PADDING_BOTTOM = 100
PADDING_BETWEEN_COLUMNS = 10
PADDING_BETWEEN_ROWS = 10
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sanjijukugo")

# Chips
CHIP_W = 60
CHIP_PAD = 7

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


def draw_text(x_pos, y_pos, text, size, color):
    '''Positive coordinates begins in upper left corner of text box'''
    font1 = pygame.font.Font('fonts/ipaexg.ttf', size)
    img = font1.render(text, True, color)
    WIN.blit(img, (x_pos, y_pos))


def gen_juku_sample_list(level):
    ''' Makes a list of random sanjijukugo '''
    num_jukus = 4 + level*2
    with open('jukugo.csv', newline='', encoding='utf-8') as my_file:
        reader = csv.reader(my_file)
        juku_list = [x for x in reader][0]
    return random.sample(juku_list, num_jukus)


def gen_shuffled_grid(juku_sample_list):
    ''' Shuffles the jukugos around and returns '''
    new_list = []
    for word in juku_sample_list:
        new_list.append(word[0])
        new_list.append(word[1])
        new_list.append(word[2])
    random.shuffle(new_list)
    return new_list


def get_cols(level):
    '''gets number of columns depending on level'''
    if level == 0:
        return 4
    if level == 1:
        return 6
    if level == 2:
        return 4
    if level == 3:
        return 5
    return 6


def get_rows(level):
    '''gets number of rows depending on level'''
    if level == 0:
        return 1
    if level == 1:
        return 1
    if level == 2:
        return 2
    if level == 3:
        return 2
    return 2


class Stage:
    ''' Abstraction of the current stage, also handles actions'''
    def __init__(self, level):
        self.level = level
        self.num_cols = get_cols(level)
        self.num_rows = get_rows(level)
        self.juku = gen_juku_sample_list(level)
        self.grid = gen_shuffled_grid(self.juku)
        self.marked_positions = []
        self.kanji_pos_array = self.gen_kanji_pos_array()
        #print(self.kanji_pos_array)
        #print(f"self.juku: {self.juku}\nself.grid: {self.grid}")

    def gen_kanji_pos_array(self):
        '''Generates an array of positions from upper left corner of chip'''
        re_array = []
        # calculate corners of box containing columns and rows
        corner_x_left = WIDTH/2 - (CHIP_W*self.num_cols/2 +
                                   PADDING_BETWEEN_COLUMNS*(self.num_cols/2 - 1) +
                                   PADDING_BETWEEN_COLUMNS/2)
        corner_y_up = HEIGHT/2 - CHIP_W*(1.5 + 2*(self.num_rows - 1))
        # add coordinates
        for i in range(self.level*2 + 4): # column
            if i >= self.num_cols:
                for j in range(3): # print kanjis in second row
                    pos = [corner_x_left + (i%self.num_cols)*(PADDING_BETWEEN_COLUMNS + CHIP_W), 
                           corner_y_up + j*(CHIP_W) + 4*CHIP_W]
                    re_array.append(pos) # add coordinate to list
            else:
                for j in range(3): # print kanjis in first row
                    pos = [corner_x_left + i*(PADDING_BETWEEN_COLUMNS + CHIP_W),
                           corner_y_up + j*(CHIP_W)]
                    re_array.append(pos) # add coordinate to list
        return re_array

    def draw(self):
        ''' draws everything'''
        # info text
        draw_text(30, 30, "LEVEL " + str(self.level + 1) + "/5", 32, "#444444")
        if self.level == 0:
            draw_text(60, HEIGHT - 30, "漢字を入れ替えて三字熟語を完成させよう！", 20, '#444444')

        # draw kanjis
        for i in range(len(self.grid)):
            # kanji
            draw_text(self.kanji_pos_array[i][0] + CHIP_PAD,
                      self.kanji_pos_array[i][1] + CHIP_PAD,
                      self.grid[i], CHIP_W - 2*CHIP_PAD, BLACK)
            # upper line
            pygame.draw.line(WIN, BLACK, (self.kanji_pos_array[i][0], self.kanji_pos_array[i][1]),
                             (self.kanji_pos_array[i][0] + CHIP_W, self.kanji_pos_array[i][1]))
            # bottom line
            pygame.draw.line(WIN, BLACK, (self.kanji_pos_array[i][0], self.kanji_pos_array[i][1] + CHIP_W),
                             (self.kanji_pos_array[i][0] + CHIP_W, self.kanji_pos_array[i][1] + CHIP_W))
            # left line
            pygame.draw.line(WIN, BLACK, (self.kanji_pos_array[i][0], self.kanji_pos_array[i][1]),
                             (self.kanji_pos_array[i][0], self.kanji_pos_array[i][1] + CHIP_W))
            # right line
            pygame.draw.line(WIN, BLACK, (self.kanji_pos_array[i][0] + CHIP_W, self.kanji_pos_array[i][1]),
                             (self.kanji_pos_array[i][0] + CHIP_W, self.kanji_pos_array[i][1] + CHIP_W))


def click(s):
    # Mouse pos
    m_x, m_y = pygame.mouse.get_pos()
    print(f"Click! x pos is: {m_x}, y pos is: {m_y}")
    for i in range(len(s.kanji_pos_array)): # 0 till 11 om len = 12
        if m_x > s.kanji_pos_array[i][0] and m_x < (s.kanji_pos_array[i][0] + CHIP_W):
            if m_y > s.kanji_pos_array[i][1] and m_y < (s.kanji_pos_array[i][1] + CHIP_W):
                #s.kanji_pos_array[i][0] = s.kanji_pos_array[i][0] + 10
                #s.kanji_pos_array[i][1] = s.kanji_pos_array[i][1] + 10
                print(f"A click was registered on tile no: {i}")


def render(s):
    WIN.fill(WHITE)
    s.draw()
    pygame.display.update()


def main():
    s = Stage(2) # Init stage
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
