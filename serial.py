from connect_db import create_table,connection
import asyncpg


async def add_books(title,author):
    conn=await connection()
    try:
        await conn.execute('''
        insert into books(title,author) values($1,$2)
        ''',title,author)
        print('книга добавлена')
    except Exception as err:
        print('у вас не добавлена книга ошибка в:',err)
        
  
  
async def show_books():
    conn=await connection()
    try:
        books=await conn.fetch('''
        select * from books
        ''')
        return books
    except Exception as err:
        print('у вас не показаны книги ошибка в:',err)
        
        
        
async def borrow_book(book_id,user_id):
    conn=await connection()
    try:
        await conn.execute('''
        insert into borrowed_books(book_id,user_id) values($1,$2)
        ''',book_id,user_id)
        print('книга взята в аренду')
    except Exception as err:
        print('у вас не взята книга в аренду ошибка в:',err)
        
        
    
    
async def return_book(book_id,user_id):
    conn=await connection()
    try:
        await conn.execute('''
        delete from borrowed_books where user_id=$1 and book_id=$2
        ''',user_id,book_id)
        print('книга возвращена в библиотеку')
    except Exception as err:
        print('у вас не возвращена книга в библиотеку ошибка в:',err)
        
        
    
    
async def my_books(user_id):