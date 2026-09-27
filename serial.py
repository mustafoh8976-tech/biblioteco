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
        
        
        
