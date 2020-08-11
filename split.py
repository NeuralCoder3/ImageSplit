from PIL import Image
import os
import itertools
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def pairwise(iterable):
    # "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return list(zip(a, b))

def split(img,xs,ys,page):
    img=Image.open(img)
    width=img.size[0]
    height=img.size[1]
    xs2=[0]+xs+[width]
    ys2=[0]+ys+[height]
    xs2.sort()
    ys2.sort()
    k=0
    for x0,x1 in pairwise(xs2):
        for y0,y1 in pairwise(ys2):
            k+=1
            box=(x0,y0,x1,y1)
            a = img.crop(box)
            a.save(os.path.join("./Out",f"PNG{page}_IMG-{k}.png"))
    if False:
        alert = QMessageBox()
        alert.setText('Finished')
        alert.exec_()
    print("Finished")

xs=[]
ys=[]
imgList=[]
pos=0

# print(pairwise([1,2,3]))

def showImage():
    global pos
    global imgList
    global imgLabel
    global imgWidth
    global imgHeight
    global img
    global imgRatio
    pixmap = QPixmap(imgList[pos])
    # imgLabel.setPixmap(pixmap)
    # print(imgLabel.size())
    img=Image.open(imgList[pos])
    imgWidth=img.size[0]
    imgHeight=img.size[1]
    imgRatio=imgWidth/imgLabel.width()

    imgLabel.setMinimumHeight(imgHeight/imgRatio)
    # pixmap=pixmap.scaled(imgLabel.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation)
    pixmap=pixmap.scaled(imgLabel.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation)
    imgLabel.setPixmap(pixmap)
    # imgLabel.setScaledContents(True)
    # imgLabel.setSizePolicy( QSizePolicy.Ignored, QSizePolicy.Ignored )

    drawGrid()

def drawGrid():
    global imgLabel
    global imgRatio
    painter = QPainter(imgLabel.pixmap())
    pen=QPen()
    pen.setColor(QColor(255,0,0))
    painter.setPen(pen)
    imgLabelHeight=imgLabel.height()-1
    imgLabelWidth=imgLabel.width()-1
    for x in xs:
        x2=int(x/imgRatio)
        painter.drawLine(x2, 0, x2, imgLabelHeight)
    for y in ys:
        y2=int(y/imgRatio)
        painter.drawLine(0, y2, imgLabelWidth, y2)
    painter.end()
    imgLabel.update()

def clearGrid():
    global xs
    global ys
    xs=[]
    ys=[]
    showImage()


def callSplit():
    global xs
    global ys
    global imgList
    global pos
    split(imgList[pos],xs,ys,pos)

def open_file():
    global window
    global pos
    global imgList
    # path = QFileDialog.getOpenFileName(window, "Open")[0]
    # path = QFileDialog.getExistingDirectory(window, "Open")[0]
    path = QFileDialog.getExistingDirectory(window, "Open")
    # dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
    if path:
        # text.setPlainText(open(path).read())
        file_path = path
        imgList2=[]
        for img in os.listdir(path):
            if img.endswith(".png") or \
                img.endswith(".jpeg") or \
                img.endswith(".jpg") or \
                img.endswith(".gif") :
                imgList2.append(os.path.join(path,img))
        if len(imgList2)>0:
            pos=0
            imgList=imgList2
            showImage()
            print("Loaded",path)
        else:
            print("There are no images")

def nextImg():
    global pos
    global imgList
    pos+=1
    pos=pos%len(imgList)
    showImage()

def prevImg():
    global pos
    global imgList
    pos-=1
    if pos<0:
        pos+=len(imgList)
    showImage()

def addPoint(event):
    # print(event)
    # print(dir(event))
    # print(dir(event.x))
    # print(int(event.x))
    # print(int(event.y))
    global xs
    global ys
    global imgRatio
    # print(event.x(),event.y())
    xpos=event.x()
    ypos=event.y()
    xpos=int(event.x()*imgRatio)
    ypos=int(event.y()*imgRatio)
    xs.append(xpos)
    ys.append(ypos)
    print(xpos,ypos)

    # global imgLabel
    # global img
    # print(imgLabel.width(),img.size[0])
    drawGrid()

app = QApplication([])
window = QWidget()
hlayout = QHBoxLayout()
vlayout = QVBoxLayout()

openBtn=QPushButton("Locate Images")
openBtn.clicked.connect(open_file)
clearBtn=QPushButton("Clear Grid")
clearBtn.clicked.connect(clearGrid)
splitBtn=QPushButton("Split")
splitBtn.clicked.connect(callSplit)
prevBtn=QPushButton("<")
prevBtn.clicked.connect(prevImg)
nextBtn=QPushButton(">")
nextBtn.clicked.connect(nextImg)
imgLabel = QLabel("Image")
imgLabel.mousePressEvent=addPoint

# pixmap = QPixmap('image.jpeg')
# imgLabel.setPixmap(pixmap)

hlayout.addWidget(openBtn)
hlayout.addWidget(clearBtn)
hlayout.addWidget(splitBtn)
hlayout.addWidget(prevBtn)
hlayout.addWidget(nextBtn)

vlayout.addLayout(hlayout)
vlayout.addWidget(imgLabel)

window.setLayout(vlayout)
window.show()
app.exec_()