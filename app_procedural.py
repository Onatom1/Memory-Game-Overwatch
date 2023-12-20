import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

NUM_ROWS = 4 # Número de linhas no grid de cartas
NUM_COLS = 4 # Número de colunas no grid de cartas
CARD_SIZE_W = 100  # Largura das cartas em pixels
CARD_SIZE_H = 100  # Altura das cartas em pixels
BG_COLOR = '#42709E' # Cor de fundo da janela
FONT_COLOR = 'white' # Cor da fonte 
FONT_STYLE = ('Arial', 12, 'bold') # Estilo da fonte 
MAX_ATTEMPTS = 25 # Tentativas

# Função para carregar as imagens do jogo
def load_images():
    images = []
    for i in range(1, 9):
        img_path = os.path.join('images', f'{i}.png')
        image = Image.open(img_path)
        image = image.resize((CARD_SIZE_W, CARD_SIZE_H), resample=Image.BICUBIC)
        images.append(ImageTk.PhotoImage(image))
    return images

# Função para criar o grid de cartas e a imagem do verso
def create_card_grid():
    images = load_images()
    image_back = Image.open(os.path.join('images', 'back.png'))
    image_back = image_back.resize((CARD_SIZE_W, CARD_SIZE_H), resample=Image.BICUBIC)
    image_back = ImageTk.PhotoImage(image_back)

    card_images = images * 2
    random.shuffle(card_images)

    grid = []
    for _ in range(NUM_ROWS):
        row = []
        for _ in range(NUM_COLS):
            image = card_images.pop()
            row.append(image)
        grid.append(row)

    return grid, image_back

# Função chamada quando uma carta é clicada
def card_clicked(row, col):
    global revealed_cards, can_click
    card = cards[row][col]

    if can_click and len(revealed_cards) < 2 and card not in revealed_cards:
        card.config(image=grid[row][col])
        revealed_cards.append(card)

        if len(revealed_cards) == 2:
            can_click = False
            window.after(1000, check_match)  # Espera 1 segundo antes de chamar check_match

# Função para verificar se as cartas reveladas são iguais
def check_match():
    global revealed_cards, can_click
    card1, card2 = revealed_cards
    if card1['image'] == card2['image']:
        card1.after(1000, card1.destroy)
        card2.after(1000, card2.destroy)
        matched_cards.extend([card1, card2])
        window.after(1000, enable_click)  # Espera 1 segundo antes de permitir o próximo clique
        check_win()
    else:
        card1.after(1000, lambda: card1.config(image=image_back))
        card2.after(1000, lambda: card2.config(image=image_back))
        window.after(1300, enable_click)  # Espera 1.3 segundo antes de permitir o próximo clique
    revealed_cards.clear()
    update_score()

# Função para habilitar o clique após um certo período
def enable_click():
    global can_click
    can_click = True

# Função para verificar se o jogador venceu o jogo
def check_win():
    if len(matched_cards) == NUM_ROWS * NUM_COLS:
        messagebox.showinfo('Parabéns!', 'Você venceu!')
        window.quit()

# Função para atualizar a contagem de tentativas
def update_score():
    global attempts
    attempts += 1
    attempts_label.config(text=f'Tentativas: {attempts}/{MAX_ATTEMPTS}')
    if attempts >= MAX_ATTEMPTS:
        messagebox.showinfo('Fim de jogo', 'Você perdeu!')
        window.quit()

# Janela principal
window = tk.Tk()
window.title('Jogo de Memória')
window.configure(bg=BG_COLOR)

# Variáveis
grid, image_back = create_card_grid()
cards = []
revealed_cards = []
matched_cards = []
can_click = True
attempts = 0

# Criação das cartas na interface gráfica
for row in range(NUM_ROWS):
    row_of_cards = []
    for col in range(NUM_COLS):
        card = tk.Button(window, width=CARD_SIZE_W, height=CARD_SIZE_H, image=image_back, relief=tk.RAISED, bd=3, command=lambda r=row, c=col: card_clicked(r, c))
        card.grid(row=row, column=col, padx=5, pady=5)
        row_of_cards.append(card)
    cards.append(row_of_cards)

# Estilo dos botões
button_style = {'activebackground': '#f8f9fa', 'font': FONT_STYLE, 'fg': FONT_COLOR}
window.option_add('*Button', button_style)

# Número de tentativas
attempts_label = tk.Label(window, text='Tentativas: {}/{}'.format(attempts, MAX_ATTEMPTS), fg=FONT_COLOR, bg=BG_COLOR, font=FONT_STYLE)
attempts_label.grid(row=NUM_ROWS, columnspan=NUM_COLS, padx=10, pady=10)


window.mainloop()