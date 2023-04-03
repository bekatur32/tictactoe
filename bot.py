import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from config import TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class TicTacToeGame(StatesGroup):
    game = State()

game_board = [' ' for _ in range(9)]
players = ['X', 'O']
current_player = players[0]

def get_board():
    board = '```\n'
    for i in range(3):
        row = ' | '.join(game_board[i*3:(i+1)*3])
        board += f'{row}\n{"--+-"*2}--\n' if i != 2 else f'{row}\n'
    board += '```'
    return board

def is_winner(board, player):
    if (board[0] == player and board[1] == player and board[2] == player) or \
       (board[3] == player and board[4] == player and board[5] == player) or \
       (board[6] == player and board[7] == player and board[8] == player) or \
       (board[0] == player and board[3] == player and board[6] == player) or \
       (board[1] == player and board[4] == player and board[7] == player) or \
       (board[2] == player and board[5] == player and board[8] == player) or \
       (board[0] == player and board[4] == player and board[8] == player) or \
       (board[2] == player and board[4] == player and board[6] == player):
        return True
    else:
        return False

async def switch_player():
    global current_player
    if current_player == players[0]:
        current_player = players[1]
    else:
        current_player = players[0]

async def ai_move():
    global game_board
    empty_cells = [i for i in range(len(game_board)) if game_board[i] == ' ']
    if empty_cells:
        cell = random.choice(empty_cells)
        game_board[cell] = players[1]
    else:
        cell = None
    return cell

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('Привет! Я бот для игры в крестики-нолики. Для начала игры введи /play')

@dp.message_handler(commands=['play'])
async def play_command(message: types.Message):
    global game_board, current_player
    game_board = [' ' for _ in range(9)]
    current_player = players[0]
    await TicTacToeGame.game.set()
    board = get_board()
    await message.answer(f'Начинаем игру! Ты играешь за {current_player}. {board}')

@dp.message_handler(state=TicTacToeGame.game, content_types=types.ContentTypes.TEXT)
async def game_handler(message: types.Message, state: FSMContext):
    global game

if __name__=='__main__':
    executor.start_polling(dp)