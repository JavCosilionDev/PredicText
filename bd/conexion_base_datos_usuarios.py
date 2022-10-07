import sqlite3

def crear_database():
    conn = sqlite3.connect('bd/usuarios.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE usuarios(id INTEGER PRIMARY KEY AUTOINCREMENT, cuenta varchar(15), usuario varchar(30), contrasenia varchar(30))''')
    conn.commit()
    conn.close()

def insertar():
    informacion = [ ('administrador', 'javier', 'xd123'), 
                    ('usuario', 'yadira', 'xd1234'),
                    ('usuario', 'fernando', 'xd1235')]

    conn = sqlite3.connect('bd/usuarios.db')
    c = conn.cursor()
    c.executemany("INSERT INTO usuarios (cuenta, usuario, contrasenia) VALUES  (?, ?, ?)", informacion)
    conn.commit()
    conn.close()

def leer():
    conn = sqlite3.connect('bd/usuarios.db')
    c = conn.cursor()

    for row in c.execute('SELECT * FROM usuarios'):
        print(row)
    conn.close()

# crear_database()
# insertar()
leer()