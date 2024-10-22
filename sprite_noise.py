import sys
import matplotlib.pyplot as plt
import random

from noise import pnoise2
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QSlider, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Noise Generator')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.btn = QPushButton('Generate Noise', self)
        self.btn.clicked.connect(self.generate_noise)

        self.layout.addWidget(self.btn)

        self.pixel_size = 12

        self.graph_size = QLabel('Sprite Size' + '(' + str(self.pixel_size) + 'x' + ')')
        self.graph_size.setFont(QFont('Arial', 16))
        self.graph_size.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.graph_size)

        self.slider_size = QSlider(Qt.Horizontal)
        self.slider_size.setMinimum(8)
        self.slider_size.setMaximum(64)
        self.slider_size.setValue(self.pixel_size)
        self.slider_size.valueChanged.connect(self.update_noise)
        self.layout.addWidget(self.slider_size)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.seed_x = random.randint(0, 1000)
        self.seed_y = random.randint(0, 1000)

        self.labelx = QLabel('X-Axis Position')
        self.labelx.setFont(QFont('Arial', 16))
        self.labelx.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.labelx)

        self.slider_x = QSlider(Qt.Horizontal)
        self.slider_x.setMinimum(0)
        self.slider_x.setMaximum(1000)
        self.slider_x.setValue(self.seed_x)
        self.slider_x.valueChanged.connect(self.update_noise)

        self.layout.addWidget(self.slider_x)

        self.labely = QLabel('Y-Axis Position')
        self.labely.setFont(QFont('Arial', 16))
        self.labely.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.labely)

        self.slider_y = QSlider(Qt.Horizontal)
        self.slider_y.setMinimum(0)
        self.slider_y.setMaximum(1000)
        self.slider_y.setValue(self.seed_y)
        self.slider_y.valueChanged.connect(self.update_noise)

        self.layout.addWidget(self.slider_y)

        self.save_btn = QPushButton('Save Image', self)
        self.save_btn.clicked.connect(self.save_image)
        self.layout.addWidget(self.save_btn)

        self.noise = self.get_noise()
        self.ax = self.figure.add_subplot(111)
        self.im = self.ax.imshow(self.noise, interpolation='nearest')
    
    def generate_noise(self):
        self.seed_x = random.randint(0, 1000)
        self.seed_y = random.randint(0, 1000)
        self.slider_x.setValue(self.seed_x)
        self.slider_y.setValue(self.seed_y)
        img = self.get_noise()

        self.im.set_data(img)
        self.canvas.draw_idle()

    def update_noise(self):
        self.seed_x = self.slider_x.value()
        self.seed_y = self.slider_y.value()
        self.pixel_size = self.slider_size.value()
        img = self.get_noise()

        self.im.set_data(img)
        self.canvas.draw_idle()
    
    def get_noise(self):
        size = self.pixel_size
        self.graph_size.setText('Sprite Size' + '(' + str(self.pixel_size) + 'x' + ')')
        scale = 10 
        threshold = 0.08

        img = Image.new('L', (size, size))
        pixels = img.load()

        for y in range(size):
            for x in range(size):
                value = pnoise2((x + self.seed_x) / scale, (y + self.seed_y) / scale)
                if value > threshold:
                    pixels[x, y] = 255
                else:
                    pixels[x, y] = 0
        
        return img

    def save_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;All Files (*)", options=options)
        if file_path:
            self.get_noise().save(file_path)

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()