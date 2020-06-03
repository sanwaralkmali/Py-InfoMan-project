from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(320)
        self.setFixedHeight(250)

        self.setWindowTitle("About Developer")

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("Salah Alkmali")
        font = title.font()

        font.setPointSize(14)
        title.setStyleSheet("color: blue")
        title.setFont(font)
        title.setAlignment(Qt.AlignCenter)

        labelpic = QLabel()
        labelpic.setFixedWidth(300)
        labelpic.setFixedHeight(100)
        labelpic.setAlignment(Qt.AlignCenter)

        self.target = QPixmap(100, 100)
        self.target.fill(Qt.transparent)

        pixmap = QPixmap('icon/author.jpg').scaled(100, 100,
                                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)

        painter = QPainter(self.target)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        path = QPainterPath()
        path.addRoundedRect(0, 0, 100, 100, 50, 50)

        painter.setClipPath(path)

        path = QPainterPath()

        painter.drawPixmap(0, 0, pixmap)

        labelpic.setPixmap(self.target)

        layout.addWidget(labelpic)
        layout.addWidget(title)

        layout.addWidget(
            QLabel("INFOMAN Version 1.1"))
        ver = QLabel("Copyright mtnshsalah@gmail.com $2020")
        font2 = ver.font()
        font2.setPointSize(8)
        ver.setFont(font2)
        layout.addWidget(ver)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
