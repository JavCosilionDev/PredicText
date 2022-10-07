import sqlite3

def crear_database():
    conn = sqlite3.connect('bd/temas.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE palabras(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria varchar(30), palabra varchar(50))''')
    conn.commit()
    conn.close()

def insertar():
    informacion = [ ('deportes', 'deportes'), ('deportes', 'salto'), ('deportes', 'cuerpo'), ('deportes', 'pelota'), ('deportes', 'balon'), ('deportes', 'luchar'), ('deportes', 'motociclismo'), ('deportes', 'velocidad'), ('deportes', 'lanzamiento'), ('deportes', 'disciplinas'),
                    
                    ('politica', 'poder'), ('politica', 'politica'), ('politica', 'bien'), ('politica', 'politico'), ('politica', 'presidente'), ('politica', 'visepresidente'), ('politica', 'principe'), ('politica', 'distincion'), ('politica', 'estado'), ('politica', 'medios'),
                    
                    ('economia', 'economia'), ('economia', 'recursos'), ('economia', 'consumo'), ('economia', 'inversion'), ('economia', 'riquesa'), ('economia', 'costes'), ('economia', 'beneficio'), ('economia', 'produccion'), ('economia', 'bienes'), ('economia', 'ingresos'),
                    
                    ('naturaleza', 'naturaleza'), ('naturaleza', 'seres'), ('naturaleza', 'vivos'), ('naturaleza', 'animales'), ('naturaleza', 'vida'), ('naturaleza', 'natural'), ('naturaleza', 'naturales'), ('naturaleza', 'ciencia'), ('naturaleza', 'ecosistema'), ('naturaleza', 'plantas'),
                    
                    ('tecnologia', 'tecnologia'), ('tecnologia', 'tecnologias'), ('tecnologia', 'medio'), ('tecnologia', 'necesidades'), ('tecnologia', 'satisfacer'), ('tecnologia', 'servicios'), ('tecnologia', 'dispositivos'), ('tecnologia', 'conocimiento'), ('tecnologia', 'esenciales'), ('tecnologia', 'artefactos'),
                    
                    ('religion', 'religion'), ('religion', 'religiones'), ('religion', 'dinero'), ('religion', 'virgen'), ('religion', 'dios'), ('religion', 'verdad'), ('religion', 'madre'), ('religion', 'santo'), ('religion', 'salvador'), ('religion', 'divino')]

    conn = sqlite3.connect('bd/temas.db')
    c = conn.cursor()
    c.executemany("INSERT INTO palabras (categoria, palabra) VALUES  (?, ?)", informacion)
    conn.commit()
    conn.close()

def leer():
    conn = sqlite3.connect('bd/temas.db')
    c = conn.cursor()

    for row in c.execute('SELECT * FROM palabras'):
        print(row)

    number = [row[2] for row in c.execute('SELECT * FROM palabras')]
    conn.close()

crear_database()
insertar()
leer()



