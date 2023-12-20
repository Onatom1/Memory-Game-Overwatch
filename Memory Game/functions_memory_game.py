import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

class MemoryGame:
    def __init__(self, num_rows, num_cols, card_size_w, card_size_h, bg_color, font_color, font_style, max_attempts):
        # Inicialização da classe com parâmetros configuráveis
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.card_size_w = card_size_w
        self.card_size_h = card_size_h
        self.bg_color = bg_color
        self.font_color = font_color
        self.font_style = font_style
        self.max_attempts = max_attempts

        # Criação da janela principal
        self.window = tk.Tk()
        self.window.title('Jogo de Memória')
        self.window.configure(bg=self.bg_color)

        # Criação do grid de cartas e imagem do verso
        self.grid, self.image_back = self.create_card_grid()
        self.cards = []
        self.revealed_cards = []
        self.matched_cards = []
        self.can_click = True
        self.attempts = 0

        # Criação das cartas na interface gráfica
        for row in range(self.num_rows):
            row_of_cards = []
            for col in range(self.num_cols):
                card = tk.Button(self.window, width=self.card_size_w, height=self.card_size_h, image=self.image_back, relief=tk.RAISED, bd=3, command=lambda r=row, c=col: self.card_clicked(r, c))
                card.grid(row=row, column=col, padx=5, pady=5)
                row_of_cards.append(card)
            self.cards.append(row_of_cards)

        # Estilo dos botões
        button_style = {'activebackground': '#f8f9fa', 'font': self.font_style, 'fg': self.font_color}
        self.window.option_add('*Button', button_style)

        # Número de tentativas
        self.attempts_label = tk.Label(self.window, text='Tentativas: {}/{}'.format(self.attempts, self.max_attempts), fg=self.font_color, bg=self.bg_color, font=self.font_style)
        self.attempts_label.grid(row=self.num_rows, columnspan=self.num_cols, padx=10, pady=10)

    def load_images(self):
        # Carrega imagens do jogo a partir dos arquivos
        images = []
        for i in range(1, 9):
            img_path = os.path.join('images', f'{i}.png')
            image = Image.open(img_path)
            image = image.resize((self.card_size_w, self.card_size_h), resample=Image.BICUBIC)
            images.append(ImageTk.PhotoImage(image))
        return images

    def create_card_grid(self):
        # Cria o grid de cartas embaralhado com as imagens e a imagem do verso
        images = self.load_images()
        image_back = Image.open(os.path.join('images', 'back.png'))
        image_back = image_back.resize((self.card_size_w, self.card_size_h), resample=Image.BICUBIC)
        image_back = ImageTk.PhotoImage(image_back)

        card_images = images * 2
        random.shuffle(card_images)

        grid = []
        for _ in range(self.num_rows):
            row = []
            for _ in range(self.num_cols):
                image = card_images.pop()
                row.append(image)
            grid.append(row)  # Esta linha deve estar alinhada com o primeiro loop `for`, não com o segundo

        return grid, image_back

    def card_clicked(self, row, col):
        # Função chamada quando uma carta é clicada
        card = self.cards[row][col]

        if self.can_click and len(self.revealed_cards) < 2 and card not in self.revealed_cards:
            card.config(image=self.grid[row][col])
            self.revealed_cards.append(card)

            if len(self.revealed_cards) == 2:
                self.can_click = False
                self.window.after(1000, self.check_match)  # Espera 1 segundo antes de chamar check_match

    def check_match(self):
        # Verifica se as cartas reveladas são iguais
        card1, card2 = self.revealed_cards
        if card1['image'] == card2['image']:
            card1.after(1000, card1.destroy)
            card2.after(1000, card2.destroy)
            self.matched_cards.extend([card1, card2])
            self.window.after(1000, self.enable_click)  # Espera 1 segundo antes de permitir o próximo clique
            self.check_win()
        else:
            card1.after(1000, lambda: card1.config(image=self.image_back))
            card2.after(1000, lambda: card2.config(image=self.image_back))
            self.window.after(1300, self.enable_click)  # Espera 1.3 segundo antes de permitir o próximo clique
        self.revealed_cards.clear()
        self.update_score()

    def enable_click(self):
        # Função para habilitar o clique após um certo período
        self.can_click = True

    def check_win(self):
        # Verifica se o jogador venceu o jogo
        if len(self.matched_cards) == self.num_rows * self.num_cols:
            messagebox.showinfo('Parabéns!', 'Você venceu!')
            self.window.quit()

    def update_score(self):
        # Atualiza a contagem de tentativas
        self.attempts += 1
        self.attempts_label.config(text=f'Tentativas: {self.attempts}/{self.max_attempts}')
        if self.attempts >= self.max_attempts:
            messagebox.showinfo('Fim de jogo', 'Você perdeu!')
            self.window.quit()

    def run(self):
        # Inicia o loop principal da interface gráfica
        self.window.mainloop()

# Uso da classe
game = MemoryGame(4, 4, 100, 100, '#42709E', 'white', ('Arial', 12, 'bold'), 15)
game.run()