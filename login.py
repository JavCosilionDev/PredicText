import sys
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFrame, QLabel, QComboBox, QLineEdit, QPushButton)
import sqlite3
import os
import analisisDeTexto
# ===================== CLASE ventanaLogin =========================

class ventanaLogin(QMainWindow):
    def __init__(self, parent=None):
        super(ventanaLogin, self).__init__(parent)
        
        self.setWindowTitle("Iniciar sesión")
        self.setWindowIcon(QIcon("assets/icono.png"))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(400, 350)

        paleta = QPalette()
        paleta.setColor(QPalette.Background, QColor(243, 243, 243))
        self.setPalette(paleta)

        self.initUI()

    def initUI(self):

      # ==================== FRAME ENCABEZADO ====================

        paleta = QPalette()
        paleta.setColor(QPalette.Background, QColor(2, 76, 152))

        frame = QFrame(self)
        frame.setFrameShape(QFrame.NoFrame)
        frame.setFrameShadow(QFrame.Sunken)
        frame.setAutoFillBackground(True)
        frame.setPalette(paleta)
        frame.setFixedWidth(400)
        frame.setFixedHeight(100)
        frame.move(0, 0)

        labelIcono = QLabel(frame)
        labelIcono.setFixedWidth(70)
        labelIcono.setFixedHeight(70)
        labelIcono.setPixmap(QPixmap("assets/icono.png").scaled(70, 70, Qt.KeepAspectRatio,
                                                         Qt.SmoothTransformation))
        labelIcono.move(37, 22)

        fuenteTitulo = QFont()
        fuenteTitulo.setPointSize(16)
        fuenteTitulo.setBold(True)

        labelTitulo = QLabel("<font color='white'>Predict Text</font>", frame)
        labelTitulo.setFont(fuenteTitulo)
        labelTitulo.move(140, 20)

        fuenteSubtitulo = QFont()
        fuenteSubtitulo.setPointSize(9)

        labelSubtitulo = QLabel("<font color='white'>Analizador de texto "
                                "(Python).</font>", frame)
        labelSubtitulo.setFont(fuenteSubtitulo)
        labelSubtitulo.move(140, 46)

      # ===================== WIDGETS LOGIN ======================

        # labelCuenta = QLabel("Cuenta", self)
        # labelCuenta.move(60, 110)

        # self.comboBoxCuenta = QComboBox(self)
        # self.comboBoxCuenta.addItems(["Administrador", "Usuario"])
        # self.comboBoxCuenta.setCurrentIndex(-1)
        # self.comboBoxCuenta.setFixedWidth(280)
        # self.comboBoxCuenta.setFixedHeight(26)
        # self.comboBoxCuenta.move(60, 136)

        # ========================================================

        labelUsuario = QLabel("Usuario", self)
        labelUsuario.move(60, 130)

        frameUsuario = QFrame(self)
        frameUsuario.setFrameShape(QFrame.StyledPanel)
        frameUsuario.setFixedWidth(280)
        frameUsuario.setFixedHeight(28)
        frameUsuario.move(60, 156)

        imagenUsuario = QLabel(frameUsuario)
        imagenUsuario.setPixmap(QPixmap("assets/usuario.png").scaled(20, 20, Qt.KeepAspectRatio,
                                                              Qt.SmoothTransformation))
        imagenUsuario.move(10, 4)

        self.lineEditUsuario = QLineEdit(frameUsuario)
        self.lineEditUsuario.setFrame(False)
        self.lineEditUsuario.setTextMargins(8, 0, 4, 1)
        self.lineEditUsuario.setFixedWidth(238)
        self.lineEditUsuario.setFixedHeight(26)
        self.lineEditUsuario.move(40, 1)

        # ========================================================

        labelContrasenia = QLabel("Contraseña", self)
        labelContrasenia.move(60, 184)

        frameContrasenia = QFrame(self)
        frameContrasenia.setFrameShape(QFrame.StyledPanel)
        frameContrasenia.setFixedWidth(280)
        frameContrasenia.setFixedHeight(28)
        frameContrasenia.move(60, 210)

        imagenContrasenia = QLabel(frameContrasenia)
        imagenContrasenia.setPixmap(QPixmap("assets/contrasena.png").scaled(20, 20, Qt.KeepAspectRatio,
                                                                     Qt.SmoothTransformation))
        imagenContrasenia.move(10, 4)

        self.lineEditContrasenia = QLineEdit(frameContrasenia)
        self.lineEditContrasenia.setFrame(False)
        self.lineEditContrasenia.setEchoMode(QLineEdit.Password)
        self.lineEditContrasenia.setTextMargins(8, 0, 4, 1)
        self.lineEditContrasenia.setFixedWidth(238)
        self.lineEditContrasenia.setFixedHeight(26)
        self.lineEditContrasenia.move(40, 1)

      # ================== WIDGETS QPUSHBUTTON ===================

        buttonLogin = QPushButton("Iniciar sesión", self)
        buttonLogin.setFixedWidth(135)
        buttonLogin.setFixedHeight(28)
        buttonLogin.move(60, 256)

        buttonCancelar = QPushButton("Cancelar", self)
        buttonCancelar.setFixedWidth(135)
        buttonCancelar.setFixedHeight(28)
        buttonCancelar.move(205, 256)

        buttonCrear = QPushButton("Crear Cuenta", self)
        buttonCrear.setFixedWidth(135)
        buttonCrear.setFixedHeight(28)
        buttonCrear.move(135, 300)

        # tbxCuenta = QLineEdit()

      # ==================== MÁS INFORMACIÓN =====================

        # labelInformacion = QLabel("Más información.", self)
        # labelInformacion.setOpenExternalLinks(True)
        # labelInformacion.setToolTip("Predict Text")
        # labelInformacion.move(15, 344)

      # ==================== SEÑALES BOTONES =====================

        buttonLogin.clicked.connect(self.Login)
        buttonCancelar.clicked.connect(self.close)
        buttonCrear.clicked.connect(self.crearUsuario)
        
  # ======================= FUNCIONES ============================
    def crearUsuario(self):
        self.close()
        os.system('python crearUsuario.py')

    def Login(self):
        # cuenta = self.comboBoxCuenta.currentText()
        usuario = self.lineEditUsuario.text()
        contrasenia = self.lineEditContrasenia.text()

        conn = sqlite3.connect('bd/usuarios.db')
        c = conn.cursor()
        
        usuarioBD = [col[2] for col in c.execute('SELECT * FROM usuarios WHERE usuario = "' + usuario + '"')]
        contraseniaBD = [col[3] for col in c.execute('SELECT * FROM usuarios WHERE contrasenia = "' + contrasenia + '"')]
        # cuentaBD = [col[1] for col in c.execute('SELECT * FROM usuarios WHERE cuenta = "' + cuenta + '"')]

        usuarioBaseDatos = analisisDeTexto.AnalizarTexto.eliminar_simbolos_bd(str(usuarioBD))
        contraseniaBaseDatos = analisisDeTexto.AnalizarTexto.eliminar_simbolos_bd(str(contraseniaBD))
        # cuentaBaseDatos = analisisDeTexto.AnalizarTexto.eliminar_simbolos(str(cuentaBD))

        conn.close()
        #validacion
        print(usuarioBaseDatos)
        print(contraseniaBaseDatos) 
        if usuario == usuarioBaseDatos:
            
            if contrasenia == contraseniaBaseDatos:
                print("Correcto inicio de sesion")
                self.close()
                os.system('python analisisdeTexto.py')
            else:
                print("Contraseña Incorrecta")
        else:
            print("Usuario no Encontrado")

        # print("Cuenta:", cuenta)
        # print("Usuario:", usuario)
        # print("Contraseña:", contrasenia)
        # print("UsuarioBD:", usuarioBaseDatos)
        # print("ContraseñaBD:", contraseniaBaseDatos)

        # self.comboBoxCuenta.setCurrentIndex(-1)
        self.lineEditUsuario.clear()
        self.lineEditContrasenia.clear()


# ================================================================

if __name__ == '__main__':
  aplicacion = QApplication(sys.argv)

  fuente = QFont()
  fuente.setPointSize(10)
  fuente.setFamily("Bahnschrift Light")

  aplicacion.setFont(fuente)
  
  ventana = ventanaLogin()
  ventana.show()
  
  sys.exit(aplicacion.exec_())
