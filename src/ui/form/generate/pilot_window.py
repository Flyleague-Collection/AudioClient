# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pilot_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_ClientWindow(object):
    def setupUi(self, ClientWindow):
        if not ClientWindow.objectName():
            ClientWindow.setObjectName(u"ClientWindow")
        ClientWindow.resize(939, 413)
        font = QFont()
        font.setFamilies([u"Leelawadee UI"])
        font.setPointSize(12)
        ClientWindow.setFont(font)
        self.gridLayout_2 = QGridLayout(ClientWindow)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox = QGroupBox(ClientWindow)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font)
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(80, 0))
        self.label_2.setFont(font)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(80, 0))
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)

        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy1.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_2, 0, 3, 1, 1)

        self.pushButton_3 = QPushButton(self.groupBox)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy1.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_3, 1, 2, 1, 1)

        self.pushButton_4 = QPushButton(self.groupBox)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy1.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_4, 1, 3, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(ClientWindow)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font)
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.label_5)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.label_6)

        self.pushButton_5 = QPushButton(self.groupBox_2)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy1.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.pushButton_5)

        self.pushButton_6 = QPushButton(self.groupBox_2)
        self.pushButton_6.setObjectName(u"pushButton_6")
        sizePolicy1.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.pushButton_6)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.label_7)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.label_8)

        self.pushButton_7 = QPushButton(self.groupBox_2)
        self.pushButton_7.setObjectName(u"pushButton_7")
        sizePolicy1.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.pushButton_7)

        self.pushButton_8 = QPushButton(self.groupBox_2)
        self.pushButton_8.setObjectName(u"pushButton_8")
        sizePolicy1.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.pushButton_8)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.gridLayout_2.addWidget(self.groupBox_2, 0, 1, 3, 1)

        self.groupBox_3 = QGroupBox(ClientWindow)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font)
        self.gridLayout_5 = QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.tabWidget = QTabWidget(self.groupBox_3)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_5.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_3, 1, 0, 1, 1)


        self.retranslateUi(ClientWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ClientWindow)
    # setupUi

    def retranslateUi(self, ClientWindow):
        ClientWindow.setWindowTitle(QCoreApplication.translate("ClientWindow", u"PilotClient", None))
        self.groupBox.setTitle(QCoreApplication.translate("ClientWindow", u"\u901a\u8baf\u9762\u677f", None))
        self.label_2.setText(QCoreApplication.translate("ClientWindow", u"COM2:", None))
        self.label_4.setText(QCoreApplication.translate("ClientWindow", u"---.---", None))
        self.label.setText(QCoreApplication.translate("ClientWindow", u"COM1:", None))
        self.pushButton.setText(QCoreApplication.translate("ClientWindow", u"TX", None))
        self.label_3.setText(QCoreApplication.translate("ClientWindow", u"---.---", None))
        self.pushButton_2.setText(QCoreApplication.translate("ClientWindow", u"RX", None))
        self.pushButton_3.setText(QCoreApplication.translate("ClientWindow", u"TX", None))
        self.pushButton_4.setText(QCoreApplication.translate("ClientWindow", u"RX", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ClientWindow", u"\u5728\u7ebf\u7ba1\u5236\u5458", None))
        self.label_5.setText(QCoreApplication.translate("ClientWindow", u"UNICOM", None))
        self.label_6.setText(QCoreApplication.translate("ClientWindow", u"122.800", None))
        self.pushButton_5.setText(QCoreApplication.translate("ClientWindow", u"COM1", None))
        self.pushButton_6.setText(QCoreApplication.translate("ClientWindow", u"COM2", None))
        self.label_7.setText(QCoreApplication.translate("ClientWindow", u"EMER", None))
        self.label_8.setText(QCoreApplication.translate("ClientWindow", u"121.500", None))
        self.pushButton_7.setText(QCoreApplication.translate("ClientWindow", u"COM1", None))
        self.pushButton_8.setText(QCoreApplication.translate("ClientWindow", u"COM2", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("ClientWindow", u"\u6587\u5b57\u6d88\u606f", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("ClientWindow", u"UNICOM", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("ClientWindow", u"---.---", None))
    # retranslateUi

