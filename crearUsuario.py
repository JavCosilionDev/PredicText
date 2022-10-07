from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout)
import sys
import sqlite3
import os

class Dialog(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self):
        super(Dialog, self).__init__()
        self.formularioGroupBox = QGroupBox("Formulario de registro")
        self.contraseniaLineEdit = QLineEdit()
        self.contraseniaLineEdit.setEchoMode(QLineEdit.Password)
        self.pagoLineEdit = QLineEdit()
        self.tipoUsuarioComboBox = QComboBox()
        self.tipoUsuarioComboBox.addItems(["Administrador", "Usuario"])
        self.usuarioLineEdit = QLineEdit()
        self.crearFormulario()

        self.btnBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btnBox.accepted.connect(self.obtenerInformacion)
        self.btnBox.rejected.connect(self.reject)

        self.btnBox.accepted.connect(self.crear_cuenta)

        principal = QVBoxLayout()
        principal.addWidget(self.formularioGroupBox)
        principal.addWidget(self.btnBox)
        self.setLayout(principal)

        self.setWindowTitle("Registrar usuario")

    def crear_cuenta(self):
        tbxCuenta = str(self.tipoUsuarioComboBox.currentText())
        tbxUsuario = str(self.usuarioLineEdit.text())
        tbxContrasenia = str(self.contraseniaLineEdit.text())
        tbxPago = str(self.pagoLineEdit.text())

        print(tbxCuenta)
        print(tbxUsuario)
        print(tbxContrasenia)

        informacion = [(tbxCuenta, tbxUsuario, tbxContrasenia)]
        
        conn = sqlite3.connect('bd/usuarios.db')
        c = conn.cursor()
        c.executemany("INSERT INTO usuarios (cuenta, usuario, contrasenia) VALUES  (?, ?, ?)", informacion)
        conn.commit()
        conn.close()
        self.close()
        os.system('python login.py')

    def obtenerInformacion(self):
        print("Tipo de usuario: {0}".format(self.tipoUsuarioComboBox.currentText()))        
        print("Usuario: {0}".format(self.usuarioLineEdit.text()))
        print("Contraseña: {0}".format(self.contraseniaLineEdit.text()))
        self.close()

    def crearFormulario(self):
        layout = QFormLayout()
        layout.addRow( QLabel("Tipo de usuario"),self.tipoUsuarioComboBox)
        layout.addRow(QLabel("Usuario"), self.usuarioLineEdit)
        layout.addRow( QLabel("Contraseña"), self.contraseniaLineEdit)
        layout.addRow( QLabel("Codigo de Pago"), self.pagoLineEdit)
      
        self.formularioGroupBox.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())