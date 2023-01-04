import pygame
import sklearn
import numpy as np
import matplotlib
matplotlib.use('module://pygame_matplotlib.backend_pygame')

from game_components import Button, text_box, Im_Button
from ingest import load_data

class GAME:
    blue = [0, 0, 255]
    light_blue = [0, 75, 255]
    yellow = [255, 255, 0]
    empty = [0,0,0,0]
    window_size = 500
    image_size = 800
    flag_size = 100
    title = 'Learn a Language'
    native = 'English'


    def __init__(self):
        # Params
        self.STATE = 0
        self.vocab_lists, self.foreign = load_data()
        self.vocab_lists_names = [i for i in list(self.vocab_lists.keys())]
        self.current_name = ''
        self.current_list = ''
        self.current_len = 0
        self.button_lists = []
        # Mechanics
        self.question_language = 0 # 1 for english, 0 for foreign
        self.q_lang = self.foreign if self.question_language == 0 else self.native
        self.a_lang = self.foreign if self.question_language == 1 else self.native
        self.attempts = 0
        self.stats = {'first': 0, 'average': []}

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([self.window_size, self.window_size])
        pygame.display.set_caption(self.title)
        self.font = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 30)
        # Images
        ukraine = pygame.image.load('Sprites/slava_ukraini.png').convert()
        self.ukraine_small = pygame.transform.scale(ukraine, (self.image_size, int(1.3967 * self.image_size) ))
        russian = pygame.image.load('Sprites/slava_ruski.png').convert()
        self.russian_small = pygame.transform.scale(russian, (self.flag_size, int(0.5 * self.flag_size) ))
        english = pygame.image.load('Sprites/australia.png').convert()
        self.english_small = pygame.transform.scale(english, (self.flag_size, int(0.5 * self.flag_size) ))

        self.loop()

    def background(self):
        # Image
        self.screen.fill(self.blue)
        pygame.draw.rect(self.screen, self.yellow, pygame.Rect(0, int(self.window_size / 2), self.window_size, self.window_size))
        self.screen.blit(self.ukraine_small, (50,50))
        pygame.display.flip()


    def loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                # print('State: ', self.STATE)
                if event.type == pygame.QUIT:
                    pygame.quit()
                if self.STATE == 0:
                    # Beginning
                    _ = self.home_screen(event)
                    self.STATE = 1
                elif self.STATE == 1:
                    # Ready to begin
                    self.current_name = self.home_screen(event)
                    if self.current_name != '':
                        self.current_list = sklearn.utils.shuffle(self.vocab_lists[self.current_name])
                        self.current_len = len(self.current_list)
                        self.STATE = 2
                elif self.STATE == 2:
                    # Setup question
                    if self.question_screen(event):
                        self.STATE = 3
                    else:
                        self.STATE = 4

                elif self.STATE == 3:
                    # Wait for questions answer and process
                    if self.question_screen(event):
                        self.STATE = 4

                elif self.STATE == 4:
                    # Vocab list finished
                    self.fin_screen(event)
                    self.STATE = 5

                elif self.STATE == 5:
                    # Vocab list finished
                    self.fin_screen(event)

                else:
                    pass
            pygame.display.flip()
            self.clock.tick(15)

    def fin_screen(self, event):
        if self.STATE == 4:
            # init:
            self.background()
            fin_text, fin_pose = text_box(self.font, 'Thnx 4 Playin', self.yellow, (250, 100))
            self.screen.blit(fin_text, fin_pose)
            stats_0 = f'{self.stats["first"]}/{self.current_len} Correct First Time'
            stats_1 = f'{np.mean(self.stats["average"]):.2f} Attempts Per Question'

            stats_0_text, stats_0_pose = text_box(self.font, stats_0, self.blue, (250, 250))
            self.screen.blit(stats_0_text, stats_0_pose)

            stats_1_text, stats_1_pose = text_box(self.font, stats_1, self.blue, (250, 300))
            self.screen.blit(stats_1_text, stats_1_pose)
            print(self.stats)

            self.button_lists = []
            button = Button('Return to Start', (250, 350), bg=self.blue, bg_hover=self.light_blue)
            self.button_lists.append(button)

        else:
            # State == 5
            for button in self.button_lists:
                if button.click(event):
                    self.STATE = 0
                self.screen.blit(button.surface, (button.x, button.y))



    def question_screen(self, event):
        if self.STATE == 2:
            # init:
            self.background()
            if len(self.current_list) > 3:
                self.current_list = sklearn.utils.shuffle(self.current_list)
                question = self.current_list.iloc[0][self.q_lang]
                answer = self.current_list.iloc[0][self.a_lang]
                question_text, question_pose = text_box(self.font, question, self.yellow, (250, 100))
                self.screen.blit(question_text, question_pose)
                distractions = [self.current_list.iloc[i][self.a_lang] for i in np.random.choice(range(1, len(self.current_list)), 3, replace=False)]
                answers = sklearn.utils.shuffle([answer] + distractions)

                self.button_lists = []
                index = 0
                for i in range(2):
                    for j in range(2):
                        button = Button(answers[index], (i * 100 + 200, j * 50 + 250), bg=self.blue, bg_hover=self.light_blue)
                        self.button_lists.append(button)
                        index += 1

                print(question, answer, distractions, len(self.current_list))
                self.attempts = 0
                return 1
            else:
                return 0
        else:
            question = self.current_list.iloc[0][self.q_lang]
            answer = self.current_list.iloc[0][self.a_lang]
            # self.STATE == 3
            for button in self.button_lists:
                if button.click(event):
                    self.attempts += 1
                    if button.name == answer:
                        print(self.current_list.iloc[0])
                        if self.attempts < 2:
                            self.current_list = self.current_list.iloc[1:]

                        self.stats['first'] += 1 if self.attempts == 1 else 0
                        self.stats['average'].append(self.attempts)
                        if len(self.current_list) < 4:
                            return 1
                        self.STATE = 2
                self.screen.blit(button.surface, (button.x, button.y))
            return 0





    def home_screen(self, event):
        if self.STATE == 0:
            # init:
            self.background()
            title_text, title_pose = text_box(self.font, self.title, self.yellow, (250, 100))
            self.screen.blit(title_text, title_pose)

            # Outline
            for i in [[-2, -2], [-2, 2], [2, -2], [2, 2]]:
                csv_text, csv_pose = text_box(self.font_small, 'Select which List', self.blue, (200+i[0], 200+i[1]))
                self.screen.blit(csv_text, csv_pose)

            csv_text, csv_pose = text_box(self.font_small, 'Select which List', self.yellow, (200, 200))
            self.screen.blit(csv_text, csv_pose)


        else:
            # Game Data
            button_data = []
            for i in range(len(self.vocab_lists_names)):
                button = Button(self.vocab_lists_names[i], (250, i * 50 + 250), bg=self.blue, bg_hover=self.light_blue)
                button_data.append(button)

            for button in button_data:
                if button.click(event):
                    return button.name
                self.screen.blit(button.surface, (button.x, button.y))

            # Game Language
            button_language = []
            im_button = Im_Button('native', (350,150), self.english_small)
            button_language.append(im_button)
            self.screen.blit(self.english_small, self.english_small.get_rect(center=im_button.rect.center))
            im_button = Im_Button('foreign', (350, 220), self.russian_small)
            button_language.append(im_button)
            self.screen.blit(self.russian_small, self.russian_small.get_rect(center=im_button.rect.center))
            im_text_button = Button('Q: ?', (350, 300), bg=self.blue, bg_hover=self.light_blue)
            for button in button_language:
                if button.click(event):
                    if button.name == 'native':
                        self.question_language = 1  # 1 for english, 0 for foreign
                        lang_text, lang_pose = text_box(self.font_small, f"Selected English Questions", self.yellow, (350, 130))
                    elif button.name == 'foreign':
                        pass
                    else:
                        lang_text, lang_pose = text_box(self.font_small, f"Selected {self.foreign} Questions", self.yellow, (350, 130))
                        self.question_language = 0  # 1 for english, 0 for foreign
                    self.screen.blit(lang_text, lang_pose)

        return ''





if __name__ == '__main__':
    game = GAME()

    # Done! Time to quit.
    pygame.quit()
