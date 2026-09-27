from connect_db import connection


async def add_bookses(title,author):
    conn=await connection()
    try:
        await conn.execute('''
        insert into books(title,author) values($1,$2)
        ''',title,author)
        print('книга добавлена')
        return True
    except Exception as err:
        print('у вас не добавлена книга ошибка в:',err)
        return False
    finally:
        await conn.close()
        
  
  
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
        insert into borrows(book_id,user_id,due_date) values($1,$2,now() + interval '14 days')
        ''',book_id,user_id)
        await conn.execute('''
        update books set is_available=false where id=$1
        ''',book_id)
        print('книга взята в аренду')
        return True
    except Exception as err:
        print('у вас не взята книга в аренду ошибка в:',err)
        
        
    
    
async def return_book(book_id,user_id):
    conn=await connection()
    try:
        await conn.execute('''
        update borrows set returned_at=now() where user_id=$1 and book_id=$2 and returned_at is null
        ''',user_id,book_id)
        await conn.execute('''
        update books set is_available=true where id=$1
        ''',book_id)
        print('книга возвращена в библиотеку')
        return True
    except Exception as err:
        print('у вас не возвращена книга в библиотеку ошибка в:',err)
        
        
    
    
async def my_books(user_id):
    conn=await connection()
    try:
        books=await conn.fetch('''
        select b.title,b.author,br.due_date from borrows br
        join books b on b.id=br.book_id
        where br.user_id=$1 and br.returned_at is null
        ''',user_id)
        return books
    except Exception as err:
        print('у вас не показаны книги в аренде ошибка в:',err)
        
        
async def overdue():
    conn=await connection()
    try:
        books=await conn.fetch('''
    select * from borrows where due_date<now() and returned_at is null
''')
        return books
    except Exception as err:
        print('у вас не показаны просроченные книги ошибка в:',err)