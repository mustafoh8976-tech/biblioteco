from dotenv import load_dotenv
import asyncpg
import os

async def connection():
    try:
        conn = await asyncpg.connect(
            username=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT'),
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME')
        )
        print('подключено в БД')
    except Exception as err:
        print('у вас ошибка в БД:',err)
        
        
async def create_table():
    conn=await connection()
    try:
        conn.execute('''
        create table if not exists users(
        id serial primary key,
        tg_id serial primary key, 
        username varchar(100) not null  
    );          
        create table if not exists books(
        id serial primary key,
        title varchar(150) not null,
        author varchar(150) not null,
        is_available bool default now()
    );
        create table if not exists borrows(
        id serial primary key,
        user_id int referensec users(id),
        book_id int referensec books(id),
        borrowed_at timestamp default now(),
        due_date date not null,
        returned_at timestamp not null
    );
        ''')
        print('таблицы созданы')
    except Exception as error:
        print('у вас не созданы таблицы ошибка в:',error) 