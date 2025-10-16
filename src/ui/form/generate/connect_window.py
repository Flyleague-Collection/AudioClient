# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'connect_window.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLayout,
    QLineEdit, QPushButton, QSizePolicy, QStackedWidget,
    QTextBrowser, QWidget)

from src.ui.component.indicator_button import IndicatorButton

class Ui_ConnectWindow(object):
    def setupUi(self, ConnectWindow):
        if not ConnectWindow.objectName():
            ConnectWindow.setObjectName(u"ConnectWindow")
        ConnectWindow.resize(710, 574)
        font = QFont()
        font.setFamilies([u"Leelawadee UI"])
        font.setPointSize(10)
        ConnectWindow.setFont(font)
        ConnectWindow.setStyleSheet(u"")
        self.gridLayout = QGridLayout(ConnectWindow)
        self.gridLayout.setObjectName(u"gridLayout")
        self.windows = QStackedWidget(ConnectWindow)
        self.windows.setObjectName(u"windows")

        self.gridLayout.addWidget(self.windows, 2, 0, 1, 2)

        self.layout_connect = QGridLayout()
        self.layout_connect.setObjectName(u"layout_connect")
        self.layout_connect.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.layout_connect.setContentsMargins(3, 3, 3, 3)
        self.label_tcp_port = QLabel(ConnectWindow)
        self.label_tcp_port.setObjectName(u"label_tcp_port")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_tcp_port.sizePolicy().hasHeightForWidth())
        self.label_tcp_port.setSizePolicy(sizePolicy)
        self.label_tcp_port.setMinimumSize(QSize(80, 0))

        self.layout_connect.addWidget(self.label_tcp_port, 1, 0, 1, 1)

        self.label_callsign_v = QLabel(ConnectWindow)
        self.label_callsign_v.setObjectName(u"label_callsign_v")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_callsign_v.sizePolicy().hasHeightForWidth())
        self.label_callsign_v.setSizePolicy(sizePolicy1)
        self.label_callsign_v.setMinimumSize(QSize(100, 23))

        self.layout_connect.addWidget(self.label_callsign_v, 2, 3, 1, 1)

        self.label_callsign = QLabel(ConnectWindow)
        self.label_callsign.setObjectName(u"label_callsign")
        sizePolicy.setHeightForWidth(self.label_callsign.sizePolicy().hasHeightForWidth())
        self.label_callsign.setSizePolicy(sizePolicy)
        self.label_callsign.setMinimumSize(QSize(40, 0))

        self.layout_connect.addWidget(self.label_callsign, 2, 2, 1, 1)

        self.line_edit_udp_port = QLineEdit(ConnectWindow)
        self.line_edit_udp_port.setObjectName(u"line_edit_udp_port")

        self.layout_connect.addWidget(self.line_edit_udp_port, 1, 3, 1, 1)

        self.layout_btn = QGridLayout()
        self.layout_btn.setObjectName(u"layout_btn")
        self.button_exit = QPushButton(ConnectWindow)
        self.button_exit.setObjectName(u"button_exit")

        self.layout_btn.addWidget(self.button_exit, 0, 0, 1, 1)

        self.button_connect = QPushButton(ConnectWindow)
        self.button_connect.setObjectName(u"button_connect")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.button_connect.sizePolicy().hasHeightForWidth())
        self.button_connect.setSizePolicy(sizePolicy2)

        self.layout_btn.addWidget(self.button_connect, 0, 1, 1, 1)


        self.layout_connect.addLayout(self.layout_btn, 3, 3, 1, 2)

        self.label_cid_v = QLabel(ConnectWindow)
        self.label_cid_v.setObjectName(u"label_cid_v")
        sizePolicy1.setHeightForWidth(self.label_cid_v.sizePolicy().hasHeightForWidth())
        self.label_cid_v.setSizePolicy(sizePolicy1)
        self.label_cid_v.setMinimumSize(QSize(100, 23))

        self.layout_connect.addWidget(self.label_cid_v, 2, 1, 1, 1)

        self.label_cid = QLabel(ConnectWindow)
        self.label_cid.setObjectName(u"label_cid")
        sizePolicy.setHeightForWidth(self.label_cid.sizePolicy().hasHeightForWidth())
        self.label_cid.setSizePolicy(sizePolicy)
        self.label_cid.setMinimumSize(QSize(40, 0))

        self.layout_connect.addWidget(self.label_cid, 2, 0, 1, 1)

        self.line_edit_address = QLineEdit(ConnectWindow)
        self.line_edit_address.setObjectName(u"line_edit_address")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.line_edit_address.sizePolicy().hasHeightForWidth())
        self.line_edit_address.setSizePolicy(sizePolicy3)

        self.layout_connect.addWidget(self.line_edit_address, 0, 1, 1, 4)

        self.label_udp_port = QLabel(ConnectWindow)
        self.label_udp_port.setObjectName(u"label_udp_port")
        self.label_udp_port.setMinimumSize(QSize(80, 0))

        self.layout_connect.addWidget(self.label_udp_port, 1, 2, 1, 1)

        self.button_rx = IndicatorButton(ConnectWindow)
        self.button_rx.setObjectName(u"button_rx")
        self.button_rx.setEnabled(False)
        self.button_rx.setCursor(QCursor(Qt.CursorShape.ForbiddenCursor))

        self.layout_connect.addWidget(self.button_rx, 2, 4, 1, 1)

        self.label_address = QLabel(ConnectWindow)
        self.label_address.setObjectName(u"label_address")
        sizePolicy.setHeightForWidth(self.label_address.sizePolicy().hasHeightForWidth())
        self.label_address.setSizePolicy(sizePolicy)
        self.label_address.setMinimumSize(QSize(80, 0))

        self.layout_connect.addWidget(self.label_address, 0, 0, 1, 1)

        self.line_edit_tcp_port = QLineEdit(ConnectWindow)
        self.line_edit_tcp_port.setObjectName(u"line_edit_tcp_port")
        sizePolicy3.setHeightForWidth(self.line_edit_tcp_port.sizePolicy().hasHeightForWidth())
        self.line_edit_tcp_port.setSizePolicy(sizePolicy3)

        self.layout_connect.addWidget(self.line_edit_tcp_port, 1, 1, 1, 1)

        self.button_tx = IndicatorButton(ConnectWindow)
        self.button_tx.setObjectName(u"button_tx")
        self.button_tx.setEnabled(False)
        self.button_tx.setCursor(QCursor(Qt.CursorShape.ForbiddenCursor))

        self.layout_connect.addWidget(self.button_tx, 1, 4, 1, 1)

        self.layout_info = QGridLayout()
        self.layout_info.setObjectName(u"layout_info")
        self.label_rx_callsign = QLabel(ConnectWindow)
        self.label_rx_callsign.setObjectName(u"label_rx_callsign")

        self.layout_info.addWidget(self.label_rx_callsign, 0, 0, 1, 1)

        self.label_rx_callsign_v = QLabel(ConnectWindow)
        self.label_rx_callsign_v.setObjectName(u"label_rx_callsign_v")

        self.layout_info.addWidget(self.label_rx_callsign_v, 0, 1, 1, 1)

        self.label_rx_freq = QLabel(ConnectWindow)
        self.label_rx_freq.setObjectName(u"label_rx_freq")

        self.layout_info.addWidget(self.label_rx_freq, 0, 2, 1, 1)

        self.label_rx_freq_v = QLabel(ConnectWindow)
        self.label_rx_freq_v.setObjectName(u"label_rx_freq_v")

        self.layout_info.addWidget(self.label_rx_freq_v, 0, 3, 1, 1)


        self.layout_connect.addLayout(self.layout_info, 3, 0, 1, 3)


        self.gridLayout.addLayout(self.layout_connect, 0, 0, 1, 1)

        self.text_browser_log = QTextBrowser(ConnectWindow)
        self.text_browser_log.setObjectName(u"text_browser_log")
        self.text_browser_log.setMaximumSize(QSize(16777215, 100))

        self.gridLayout.addWidget(self.text_browser_log, 3, 0, 1, 2)


        self.retranslateUi(ConnectWindow)

        QMetaObject.connectSlotsByName(ConnectWindow)
    # setupUi

    def retranslateUi(self, ConnectWindow):
        ConnectWindow.setWindowTitle(QCoreApplication.translate("ConnectWindow", u"AudioClient", None))
        self.label_tcp_port.setText(QCoreApplication.translate("ConnectWindow", u"TCP\u7aef\u53e3", None))
        self.label_callsign_v.setText(QCoreApplication.translate("ConnectWindow", u"----", None))
        self.label_callsign.setText(QCoreApplication.translate("ConnectWindow", u"\u547c\u53f7", None))
        self.button_exit.setText(QCoreApplication.translate("ConnectWindow", u"\u9000\u51fa\u767b\u5f55", None))
        self.button_connect.setText(QCoreApplication.translate("ConnectWindow", u"\u8fde\u63a5\u670d\u52a1\u5668", None))
        self.label_cid_v.setText(QCoreApplication.translate("ConnectWindow", u"----", None))
        self.label_cid.setText(QCoreApplication.translate("ConnectWindow", u"CID", None))
        self.label_udp_port.setText(QCoreApplication.translate("ConnectWindow", u"UDP\u7aef\u53e3", None))
        self.button_rx.setText(QCoreApplication.translate("ConnectWindow", u"RX", None))
        self.label_address.setText(QCoreApplication.translate("ConnectWindow", u"\u670d\u52a1\u5668\u5730\u5740", None))
        self.button_tx.setText(QCoreApplication.translate("ConnectWindow", u"TX", None))
        self.label_rx_callsign.setText(QCoreApplication.translate("ConnectWindow", u"\u53d1\u8a00\u4eba\u547c\u53f7", None))
        self.label_rx_callsign_v.setText(QCoreApplication.translate("ConnectWindow", u"---.---", None))
        self.label_rx_freq.setText(QCoreApplication.translate("ConnectWindow", u"\u63a5\u6536\u9891\u7387", None))
        self.label_rx_freq_v.setText(QCoreApplication.translate("ConnectWindow", u"---.---", None))
    # retranslateUi

