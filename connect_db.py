from dotenv import load_dotenv
import asyncpg
import os

load_dotenv()

async def connection():
    try:
        conn = await asyncpg.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT'),
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME')
        )
        print('подключено в БД')
        return conn
    except Exception as err:
        print('у вас ошибка в БД:',err)
        
        
async def create_table():
    conn=await connection()
    try:
        await conn.execute('''
        create table if not exists users(
        id serial primary key,
        tg_id bigint unique not null, 
        username varchar(100)  
    );          
        create table if not exists books(
        id serial primary key,
        title varchar(150) not null,
        author varchar(150) not null,
        is_available bool default true
    );
        create table if not exists borrows(
        id serial primary key,
        user_id int references users(id),
        book_id int references books(id),
        borrowed_at timestamp default now(),
        due_date date not null,
        returned_at timestamp
    );
        ''')
        print('таблицы созданы')
    except Exception as error:
        print('у вас не созданы таблицы ошибка в:',error) 
    finally:
        await conn.close()