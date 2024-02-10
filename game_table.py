import random
import sys
import names

import pygame

CARD_SPACING = 20
CARD_X = 80
CARD_Y = 100


class GameTable():
    def __init__(self):
        # Инициализация Pygame
        pygame.init()

        # Создание окна
        self.screen = pygame.display.set_mode((1024, 768))

        # Загрузка изображений
        self.table_image = pygame.image.load("game_table.png")
        self.opponent1_image = pygame.transform.scale(pygame.image.load("opponent1.png"), (150, 150))
        self.opponent2_image = pygame.transform.scale(pygame.image.load("opponent2.png"), (150, 150))
        self.card_back_image = pygame.image.load("cards/card_back.png")

        # Генерация случайных имен оппонентов
        self.opponent1_name = names.get_first_name(gender='male')
        self.opponent2_name = names.get_first_name(gender='male')

        # Загрузка шрифта
        self.font = pygame.font.Font(None, 24)

        self.suits = ['черви', 'бубны', 'крести', 'пики']
        self.ranks = ['9', '10', 'валет', 'дама', 'король', 'туз']

        # Картинки карт
        self.card_images = {}

        # Создание колоды карт
        self.deck = self.__create_deck()

        # Раздача карт
        self.player_hand = []
        self.opponent1_hand = []
        self.opponent2_hand = []
        self.__deal_cards()

    def __create_deck(self):
        for suit in self.suits:
            for rank in self.ranks:
                self.card_images[(rank, suit)] = self.__load_card_image(rank, suit)
        self.card_images['back'] = self.card_back_image
        deck = [(rank, suit) for suit in self.suits for rank in self.ranks]
        random.shuffle(deck)
        return deck

    def __load_card_image(self, rank, suit):
        card_name = f"{rank}_{suit}"
        card_image = pygame.image.load(f"cards/{card_name}.png")
        card_image = pygame.transform.scale(card_image, (CARD_X, CARD_Y))
        return card_image

    def __deal_cards(self):
        for _ in range(7):
            self.player_hand.append(self.deck.pop())
            self.opponent1_hand.append(self.deck.pop())
            self.opponent2_hand.append(self.deck.pop())

    def __draw_card(self, card, x, y, show_back=False):
        if show_back:
            card_image = self.card_images['back']  # Отобразить рубашку карты
            card_image = pygame.transform.scale(card_image, (CARD_X, CARD_Y))
        else:
            card_image = self.card_images[card]  # Загрузка изображения карты
        self.screen.blit(card_image, (x, y))

    def __draw_hand(self, hand, x, y, show_backs=False):
        for i, card in enumerate(hand):
            self.__draw_card(card, x + i * CARD_SPACING, y, show_backs)

    def run(self):
        # Основной цикл игры
        while True:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Отрисовка игрового поля
            self.screen.blit(self.table_image, (0, 0))
            # Отрисовка противников
            self.screen.blit(self.opponent1_image, (100, 300))
            opponent1_name_text = self.font.render(self.opponent1_name, True, (255, 0, 0))
            self.screen.blit(opponent1_name_text, (100, 440))
            self.screen.blit(self.opponent2_image, (600, 100))
            opponent2_name_text = self.font.render(self.opponent2_name, True, (255, 0, 0))
            self.screen.blit(opponent2_name_text, (600, 240))

            # Отрисовка карт в руке игрока и оппонентов
            self.__draw_hand(self.player_hand, 300, 650)
            self.__draw_hand(self.opponent1_hand, 100, 200, show_backs=True)
            self.__draw_hand(self.opponent2_hand, 400, 50, show_backs=True)

            # Обновление экрана
            pygame.display.update()