from aiogram import Bot,Dispatcher,types
from connect_db import create_table
from aiogram.filters import Command
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN=os.getenv('BOT_TOKEN')
dp=Dispatcher()

@dp.message(Command('start'))
async def starts(message:types.Message):
    await message.answer('''Привет, я бот библиотеки,
    я могу помочь тебе найти книгу и взять её в аренду. 
    Для начала работы напиши /help''')
    await create_table()
    
@dp.message(Command('help'))
async def helps(message:types.Message):
    await message.answer('''Вот что я умею:
    /start - начать работу со мной
    /help - помощь по командам
    /add_book - добавить книгу в библиотеку
    /books - посмотреть все книги в библиотеке
    /borrow - взять книгу в аренду
    /return_book - вернуть книгу в библиотеку
    /my_books - посмотреть свои книги в аренде''')
    
@dp.message(Command('add_book'))
async def add_books(message:types.Message):
    books=await add_books()
    await message.answer('вот список всех книг в библиотеке:\n'+books)
    
    
@dp.message(Command('books'))
async def books(message:types.Message):
    show_books=await show_books()
    await message.answer('вот список всех книг в библиотеке:\n'+show_books)
    

