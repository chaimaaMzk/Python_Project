from PyQt5.QtWidgets import QFileDialog, QLineEdit, QApplication, QPushButton, QDialog, QGroupBox, QVBoxLayout, QGridLayout, QLabel, QHBoxLayout
import sys
from PyQt5 import QtGui ,QtWidgets
from PyQt5.QtCore import QRect
from PyQt5 import QtCore
from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
import cv2
import pytesseract 
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.title = "Projet"
        self.left = 100
        self.top = 100
        self.width = 1000
        self.heigth = 600

        self.InitWindow()


    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.heigth)

        self.CreateLayout()
        

        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)
        
      

        self.show()

    def CreateLayout(self):
        self.groupBox = QGroupBox("")
        gridLayout = QGridLayout()

        label = QLabel("Choisir le CV a traiter :")
        gridLayout.addWidget(label,0,0)

        button = QPushButton("Telecharger", self)
        button.setMinimumHeight(30)
        button.setDefault(False)
        button.setAutoDefault(False)
        button.clicked.connect(self.Telecharger)
        gridLayout.addWidget(button,0,1)

        self.label1 = QLabel('Aucun fichier choisi',self)
        gridLayout.addWidget(self.label1,0,2)
        
        label = QLabel("les criteres demander :")
        gridLayout.addWidget(label,1,0)

        self.lineedit = QLineEdit(self)
        self.lineedit.setPlaceholderText("Criteres")
        self.lineedit.returnPressed.connect(self.Resultat)
        gridLayout.addWidget(self.lineedit,1,1)

        button1 = QPushButton("Traiter", self)
        button1.setMinimumHeight(30)
        button1.setDefault(False)
        button1.setAutoDefault(False)
        button1.clicked.connect(self.Resultat)
        gridLayout.addWidget(button1,3,0)

        self.label2 = QLabel(self)
        gridLayout.addWidget(self.label2,4,0)

        self.label3 = QLabel(self)
        gridLayout.addWidget(self.label3,5,0)
        
        self.groupBox.setLayout(gridLayout)

    def Telecharger(self):
        pathFileName = QtWidgets.QFileDialog.getOpenFileName(None,'test', '', 'pdf(*.pdf)')   
        nbrPage = 0
        if pathFileName:
            skip1 = True
            for i in pathFileName:
                if skip1 == True:
                    path = i
                    skip1 = False
            images = convert_from_path(path)
            for i, image in enumerate(images):
                fname="image\\Page"+str(i)+".png"
                image.save(fname,"PNG")
                nbrPage += 1
            pathlist = []
            pathList = path.split('/')
            name = pathList[-1]
            self.label1.setText(name)
        

        print("fin Telecharger")





    def Resultat(self):
        #ce que fais la button Resultat
        Critere = self.lineedit.text()
        listCritere = Critere.split()
        img = Image.open('image\page0.png')
        text = pytesseract.image_to_string(img)
        list = text.split("\n")
        for i , l in enumerate(list) :
            poste = list[0]
            nom = list[2]
            age = list[4]
            Diplome = list[19]
            Competence = list[33]
            experince = list[38]
        Resultat = nom  +' agé de '+ age +' titilaire de '+Diplome+ ' derniere experience est '+ experince+' a postule au poste '+poste
        self.label2.setText(Resultat)

        if poste in Critere :
            if Diplome in Critere:
                if Competence in Critere:
                    Compatible = nom +' est compatible au poste demender'
                else:
                    Compatible = nom +' n\'a pas les competences  demender'
            else:
                Compatible = nom +' n\'a pas le diplome demender'
        else:
            Compatible = nom +' n\'est pas compatible au poste demender'


            
        self.label3.setText(Compatible)
        print("Fin Resultat")



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())


