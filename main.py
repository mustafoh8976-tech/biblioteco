from aiogram import Bot,Dispatcher,types
from connect_db import create_table
from aiogram.filters import Command
from dotenv import load_dotenv
from serial import add_bookses,show_books,borrow_book,return_book,my_books,overdue
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
import asyncio
import os

knop=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='add_book'),KeyboardButton(text='show_books')],
        [KeyboardButton(text='borrow_book'),KeyboardButton(text='return_book')],
        [KeyboardButton(text='my_books'),KeyboardButton(text='overdue')],
        [KeyboardButton(text='help')]
    ]
)

load_dotenv()
BOT_TOKEN=os.getenv('BOT_TOKEN')
bot=Bot(token=BOT_TOKEN)
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
    /add_book Название | Автор - добавить книгу в библиотеку
    /books - посмотреть все книги в библиотеке
    /borrow book_id - взять книгу в аренду
    /return_book book_id - вернуть книгу в библиотеку
    /my_books - посмотреть свои книги в аренде
    /overdue - посмотреть просроченные книги''',reply_markup=knop)
    

@dp.message(Command('add_book'))
async def add_books(message:types.Message):
    args=message.text.split(maxsplit=1)
    parts=args[1].split('|',maxsplit=1)
    title=parts[0].strip()
    author=parts[1].strip()
    result=await add_bookses(title,author)
    if result:
        await message.answer(f'Книга добавлена: {title}',reply_markup=knop)
    else:
        await message.answer('Не удалось добавить книгу',reply_markup=knop)

   
@dp.message(Command('books'))
async def books(message:types.Message):
    books_list=await show_books()
    text=''
    for b in books_list:
        text=text+b['title']+' - '+b['author']+'\n'
    await message.answer('вот список всех книг в библиотеке:\n'+text,reply_markup=knop)
    

@dp.message(Command('borrow'))
async def borrow(message:types.Message):
    args=message.text.split(maxsplit=1)
    book_id=int(args[1])
    user_id=message.from_user.id
    result=await borrow_book(book_id,user_id)
    if result:
        await message.answer('книга взята в аренду',reply_markup=knop)
    else:
        await message.answer('не удалось взять книгу',reply_markup=knop)



@dp.message(Command('return_book'))
async def return_books(message:types.Message):
    args=message.text.split(maxsplit=1)
    book_id=int(args[1])
    user_id=message.from_user.id
    result=await return_book(book_id,user_id)
    if result:
        await message.answer('книга возвращена в библиотеку',reply_markup=knop)
    else:
        await message.answer('не удалось вернуть книгу',reply_markup=knop)


@dp.message(Command('my_books'))
async def my_books_mun(message:types.Message):
    user_id=message.from_user.id
    books_list=await my_books(user_id)
    text=''
    for b in books_list:
        text=text+b['title']+' - '+b['author']+'\n'
    await message.answer('вот список вашик книг из библиотеке:\n'+text,reply_markup=knop)

    
@dp.message(Command('overdue'))
async def overdue_mun(message:types.Message):
    overdue_list=await overdue()
    text=''
    for b in overdue_list:
        text=text+str(b['book_id'])+' - '+  +'\n'
    await message.answer('вот список всех просроченных книг:\n'+text,reply_markup=knop)

    
async def main():
    print('Start bot')
    await dp.start_polling(bot)
    
    
if __name__=='__main__':
    asyncio.run(main())