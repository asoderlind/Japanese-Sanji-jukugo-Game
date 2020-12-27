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
BLACK = '#000000'
GREEN = '#aaee00'
GRAY = 'eeeeee'
DARK_GRAY = '#888888'


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


def stage_dimensions(level):
    ''' returns num of rows and columns'''
    if level == 0:
        return 4, 1
    if level == 1:
        return 6, 1
    if level == 2:
        return 4, 2
    if level == 3:
        return 5, 2
    return 6, 2


class Chip:
    ''' Abstraction of the kanji chip, which contains position
    coordinate corresponding to upper left corner, the kanji,
    and the status (0=uncompleted,unclicked, 1=clicked, 2=completed)'''
    def __init__(self, x_pos, y_pos, kanji, status):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.kanji = kanji
        self.status = status

    def set_pos(self, new_x, new_y):
        '''Updated position'''
        self.x_pos = new_x
        self.y_pos = new_y

    def get_pos(self):
        '''Returns position'''
        return [self.x_pos, self.y_pos]

    def __str__(self):
        return "Coordinates: " + str(self.x_pos) + ", " + \
                                 str(self.y_pos) + ", " + \
                "Kanji: " + self.kanji + ", Status: " + str(self.status)


def gen_chip_array(juku_sample_list, level, num_cols, num_rows):
    '''Returns a list of chip objects with corresponding kanji, position
    and status'''
    # calculate corners of box containing columns and rows
    corner_x_left = WIDTH/2 - (CHIP_W*num_cols/2 +
                               PADDING_BETWEEN_COLUMNS*(num_cols/2 - 1) +
                               PADDING_BETWEEN_COLUMNS/2)
    corner_y_up = HEIGHT/2 - CHIP_W*(1.5 + 2*(num_rows - 1))

    # Initialize list of coordinates
    pos_list = []

    # Add coordinates to list
    for i in range(level*2 + 4): # column
        if i >= num_cols:
            for j in range(3): # print kanjis in second row
                pos = [corner_x_left + (i%num_cols)*(PADDING_BETWEEN_COLUMNS + CHIP_W), 
                       corner_y_up + j*(CHIP_W) + 4*CHIP_W]
                pos_list.append(pos) # add coordinate to list
        else:
            for j in range(3): # print kanjis in first row
                pos = [corner_x_left + i*(PADDING_BETWEEN_COLUMNS + CHIP_W),
                       corner_y_up + j*(CHIP_W)]
                pos_list.append(pos) # add coordinate to list

    # Initialize list of kanjis
    kanji_list = []

    # Add kanjis to list
    for word in juku_sample_list:
        kanji_list.append(word[0])
        kanji_list.append(word[1])
        kanji_list.append(word[2])

    # Shuffle list of kanjis
    random.shuffle(kanji_list)

    # Initialize list of chips
    chip_array = []

    # Add chips with coordinates, kanjis and statuses to list
    for i in range(len(pos_list)):
        chip_array.append(Chip(pos_list[i][0], pos_list[i][1], kanji_list[i], 0))

    # Return the final array
    return chip_array


class Stage:
    ''' Abstraction of the current stage, also handles actions'''
    def __init__(self, level):
        self.level = level
        self.is_completed = False
        self.load_next_stage_ready = False
        self.num_cols, self.num_rows = stage_dimensions(level)
        self.juku = gen_juku_sample_list(level)
        self.chips = gen_chip_array(self.juku, self.level, self.num_cols, self.num_rows)
        print(self.juku)

    def two_chips_selected(self):
        '''True if 2 or more chips are selected'''
        count = 0
        for chip in self.chips:
            if chip.status == 1:
                count = count + 1
                if count > 1:
                    return True
        return False

    def check_for_completed_line(self):
        '''True if one line corresponds to word in juku'''
        for i in range(0, len(self.chips), 3):
            #print(self.chips[i].kanji + self.chips[i+1].kanji + self.chips[i+2].kanji)
            if self.chips[i].kanji + self.chips[i+1].kanji + self.chips[i+2].kanji in self.juku:
                self.chips[i].status = 2
                self.chips[i+1].status = 2
                self.chips[i+2].status = 2

    def all_lines_completed(self):
        completed_count = 0
        for c in self.chips:
            if c.status == 2:
                completed_count = completed_count + 1
        if completed_count == len(self.chips):
            self.is_completed = True
            return True
        return False        

    def swap_chips(self):
        ''' swaps the kanji between two chip objects with status 1'''
        # Find first
        for i in range(len(self.chips)):
            if self.chips[i].status == 1:
                tmp = self.chips[i].kanji
                # Find second
                for j in range(i+1, len(self.chips)):
                    if self.chips[j].status == 1:
                        self.chips[i].kanji = self.chips[j].kanji
                        self.chips[j].kanji = tmp
                        self.chips[i].status = 0
                        self.chips[j].status = 0
                        break
                break

    def draw(self):
        ''' draws everything'''
        # info text
        draw_text(30, 30, "LEVEL " + str(self.level + 1) + "/5", 32, "#444444")
        if self.level == 0:
            draw_text(60, HEIGHT - 30, "漢字を入れ替えて三字熟語を完成させよう！", 20, '#444444')

        # draw chips
        for i in range(len(self.chips)):
            # box
            pygame.draw.rect(WIN, BLACK, pygame.Rect(self.chips[i].x_pos,
                                                     self.chips[i].y_pos, CHIP_W - 2, CHIP_W - 2)
                             , 1)
            # box fill
            if self.chips[i].status == 1:
                pygame.draw.rect(WIN, GREEN, pygame.Rect(self.chips[i].x_pos,
                                                         self.chips[i].y_pos,
                                                         CHIP_W - 3,
                                                         CHIP_W - 3))
            elif self.chips[i].status == 2:
                pygame.draw.rect(WIN, DARK_GRAY, pygame.Rect(self.chips[i].x_pos,
                                                             self.chips[i].y_pos,
                                                             CHIP_W - 3,
                                                             CHIP_W - 3))
            # kanji
            draw_text(self.chips[i].x_pos + CHIP_PAD,
                      self.chips[i].y_pos + CHIP_PAD,
                      self.chips[i].kanji, CHIP_W - 2 * CHIP_PAD, BLACK)


def click(s):
    '''Function that runs whenever you click the screen'''
    # Mouse pos
    m_x, m_y = pygame.mouse.get_pos()
    #print(f"Click! x pos is: {m_x}, y pos is: {m_y}")
    for i in range(len(s.chips)): # 0 till 11 om len = 12
        if m_x > s.chips[i].x_pos and m_x < (s.chips[i].x_pos + CHIP_W):
            if m_y > s.chips[i].y_pos and m_y < (s.chips[i].y_pos + CHIP_W):
                #print(f"A click was registered on tile no: {i}")
                if s.chips[i].status == 0:
                    s.chips[i].status = 1
                elif s.chips[i].status == 1:
                    s.chips[i].status = 0

    if s.two_chips_selected():
        s.swap_chips()

    s.check_for_completed_line()


def render(s):
    WIN.fill(WHITE)
    s.draw()
    pygame.display.update()


def main():
    level = 0
    s = Stage(level)
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(s)

        render(s) # Run update sequence

        if s.load_next_stage_ready:
            level = level + 1
            s = Stage(level)


while True:
    if __name__ == '__main__':
        main()
