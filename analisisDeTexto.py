#librerias graficas
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


#librerias logicas
#from unidecode import unidecode
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from collections import Counter
from collections import OrderedDict
import sqlite3
import math
import os


class AnalizarTexto(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Abrir Archivo de texto...'
        self.setWindowIcon(QIcon("assets/icono.png"))
        self.left = 360
        self.top = 170
        self.width = 640
        self.height = 480
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.abrirArchivo()
        self.show()
    
    def abrirArchivo(self):
        options = QFileDialog.Options()
        options = QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(self, "Abrir archivo de texto...", "", "Text Files (*.txt)", options=options)
        if fileName:
            ruta = str(fileName[0])
            print("ruta del archivo: " + ruta + "\n")
            textoFiltrado = AnalizarTexto.abrir_archivo(ruta)
            datos = AnalizarTexto.calcular(textoFiltrado, 33)
            print("datos: ")
            print(datos)
            print("\n")
            AnalizarTexto.calcular_tema(datos)
            

    #abrir y leer el archivo de texto
    def abrir_archivo(ruta):
        with open(ruta, 'r') as archivoTexto:
            texto = archivoTexto.read()
        textoLimpio = AnalizarTexto.limpiar_texto_simbolos(texto)
        textoFiltrado = AnalizarTexto.tokenizar_texto(textoLimpio)
        return textoFiltrado

    #tokenizar el texto
    def tokenizar_texto(texto):
        stop_words = set(stopwords.words('spanish'))
        word_tokens = word_tokenize(texto)
        word_tokens = list(filter(lambda token: token not in string.punctuation, word_tokens))
        filtrado = []
        for palabra in word_tokens:
            if palabra not in stop_words:
                filtrado.append(palabra)
        return filtrado

    #calcular las reppeticiones que hacen cada palabra
    def calcular(filtro, precision):
        c = Counter(filtro)
        if (precision == 0): 
            datos = OrderedDict(c.most_common())
        else: 
            datos = OrderedDict(c.most_common(precision))
        return datos

    #se calcula el porcentaje de cada tema
    def calcular_tema(datos):
        #comparar cada palabra con las palabras en las bases de datos, y sacar la categoría de cada una 
        conn = sqlite3.connect('bd/temas.db')
        c = conn.cursor()

        #inicializar variables contadoras
        politica = 0
        deporte = 0
        naturaleza = 0
        tecnologia = 0
        religion = 0
        economia = 0
        resultados = []

        #hacer consulta a la base de datos de cada elemento de la coleccion
        for palabra, repeticion in datos.items():
            print("Palabra: " + palabra)

            #consultar solo a la columna 1 (categoria) de la tabla de la base de datos
            categoria = [col[1] for col in c.execute('SELECT * FROM palabras WHERE palabra = "' + palabra + '"')]
            
            #convertir categoria de <list> a str ademas de quitar los simbolos extra y dejar solo texto
            categoriaStr = AnalizarTexto.eliminar_simbolos_bd(str(categoria))
            
            #imprimir la categoria de la palabra y las repeticiones en el texto de la misma
            if(categoriaStr == ""):
                print("categoria: NO CATEGORIZADA")
            else:
                print("categoria: " + categoriaStr)

            print("repeticiones: " + str(repeticion))

            #si aparece una palabra que se relacione con la categoria condicionada sumar 1 a su contador
            if(categoriaStr == "politica"):
                politica = politica + 1 
            if(categoriaStr == "deportes"):
                deporte = deporte + 1 
            if(categoriaStr == "naturaleza"):
                naturaleza = naturaleza + 1 
            if(categoriaStr == "tecnologia"):
                tecnologia = tecnologia + 1 
            if(categoriaStr == "religion"):
                religion = religion + 1 
            if(categoriaStr == "economia"):
                economia = economia + 1 
            
            print("\n")
        #cantCategorias es la suma de todos los contadores
        cantCategorias = politica + deporte + naturaleza + tecnologia + religion + economia
        
        #se divide el 100% por la cantidad de las categorias en el texto
        a = 100 / cantCategorias

        #redondear abajo la variable para trabajar mejor
        aR = math.floor(a) 
        #aR = round(a)
        # print(aR)
        # print(naturaleza)

        #se multiplica el numero de repeticiones por la cantidad de particiones de 100
        rP = aR * politica
        rD = aR * deporte
        rN = aR * naturaleza
        rT = aR * tecnologia
        rR = aR * religion
        rE = aR * economia

        #sumar los resultados para verificar que sea cercano a 100
        precision = rP + rD + rN + rT + rR + rE
        print("Presicion total: " + str(precision) + '%')
        print("\t")

        #imprimir los resultados individualmente 
        print("Politica:   " + str(rP) + '%')
        print("Deportes:   " + str(rD) + '%')
        print("Naturaleza: " + str(rN) + '%')
        print("Tecnologia: " + str(rT) + '%')
        print("Religion:   " + str(rR) + '%')
        print("Economia:   " + str(rE) + '%')

        AnalizarTexto.imprimir(datos, "resultadosAnalisis", "repeticiones", rP, rD, rN, rT, rR, rE, precision)
        
        AnalizarTexto.mostrar_grafica_pastel(rP, rD, rN, rT, rR, rE, precision)
        AnalizarTexto.mostrar_grafica_barras(rP, rD, rN, rT, rR, rE, precision)
        
        # os.system('python analisisDeTexto.py')
        
        #retornar arreglo de los resultados
        resultados = [rP, rD, rN, rT, rR, rE]
        return resultados

    def mostrar_grafica_barras(politica, deportes, naturaleza, tecnologia, religion, economia , precision):
        temas = ['Política', 'Deportes', 'Naturaleza', 'Tecnología', 'Religión', 'Economia']
        porcentaje = [politica, deportes, naturaleza, tecnologia, religion, economia]
        fig, ax = plt.subplots()
        #etiqueta en el eje Y
        ax.set_ylabel('%')
        #etiqueta en el eje X
        ax.set_title('Resultados del Analisis (Presición: ' + str(precision) + '%)')

        plt.bar(temas, porcentaje)
        plt.savefig('resultados/ResultadoAnalisis.png')
        plt.show()

    def mostrar_grafica_pastel(politica, deportes, naturaleza, tecnologia, religion, economia , precision):
        temas = ['Política', 'Deportes', 'Naturaleza', 'Tecnología', 'Religión', 'Economia']
        porcentaje = [politica, deportes, naturaleza, tecnologia, religion, economia]
        #resaltar algun valor
        explode = (0, 0, 0, 0, 0, 0)

        fig1, ax1 = plt.subplots()
        #creacion de grafica
        ax1.pie(porcentaje, explode=explode, labels=temas, autopct='%1.1f%%',
                shadow=True, startangle=90)
       
        ax1.axis('equal')
        plt.title('Resultados de Analisis (Presición: ' + str(precision) + '%)')
        plt.legend()
        plt.savefig('resultados/grafica_pastel.png')
        plt.show()

    def eliminar_simbolos_bd(string):
        characters = "'[]"
        for x in range(len(characters)):
            string = string.replace(characters[x],"")
        return string
    
    #eliminar los simbolos
    def limpiar_texto_simbolos(string):
        simbolos = "'[],.:;‘áéíóúABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚñÑ"
        sinSimbo = "        aeiouabcdefghijklmnopqrstuvwxyzaeiounn"
        for x in range(len(simbolos)):
            string = string.replace(simbolos[x], sinSimbo[x])
        return string


    #imprimir archivo txt
    def imprimir(datos, archivoResultados, archivoRepeticiones, politica, deportes, naturaleza, tecnologia, religion, economia, precision):
        with open('resultados/' + archivoRepeticiones + '.txt', 'w') as f:
            f.write(f'Palabra-> Repeticiones\n\n')
            for palabra, repeticiones in datos.items():
                f.write(f'{palabra}-> {repeticiones}\n')

        with open('resultados/' + archivoResultados + '.txt', 'w') as f:
            f.write(f'Resultado de analisis:\n\n')
            f.write(f'Presicion Total: %' + str(precision) + '\n')
            f.write(f'Politica:   %' + str(politica) + '\n')
            f.write(f'Deportes:   %' + str(deportes) + '\n')
            f.write(f'Naturaleza: %' + str(naturaleza) + '\n')
            f.write(f'Tecnologia: %' + str(tecnologia) + '\n')
            f.write(f'Religion:   %' + str(religion) + '\n')
            f.write(f'Economia:   %' + str(economia))
    def obtener_datos():
        nombre = "todo"
        precision = 10
        datos = AnalizarTexto.calcular(AnalizarTexto.abrir_archivo(nombre), precision)
        resultados = AnalizarTexto.calcular_tema(datos)
        return resultados

#ejecutar archivo
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = AnalizarTexto()
    sys.exit()