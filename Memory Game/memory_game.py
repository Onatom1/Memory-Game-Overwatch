from functions_memory_game import MemoryGame

NUM_ROWS = 4 # Número de linhas no grid de cartas
NUM_COLS = 4 # Número de colunas no grid de cartas
CARD_SIZE_W = 100  # Largura das cartas em pixels
CARD_SIZE_H = 100  # Altura das cartas em pixels
BG_COLOR = '#42709E' # Cor de fundo da janela
FONT_COLOR = 'white' # Cor da fonte 
FONT_STYLE = ('Arial', 12, 'bold') # Estilo da fonte 
MAX_ATTEMPTS = 25 # Tentativas


game = MemoryGame(NUM_ROWS, NUM_COLS, CARD_SIZE_W, CARD_SIZE_H, BG_COLOR, FONT_COLOR, FONT_STYLE, MAX_ATTEMPTS)
game.run()