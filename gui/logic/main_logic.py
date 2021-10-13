# -*- coding: utf-8 -*-
import os

from PyQt5 import QtCore, QtGui, QtWidgets

from gui.forms.main_form import Ui_MainWindow
from gui.logic.abstracts import AbstractGameForm
from gui.logic.five_in_a_row import FiveForm
from gui.logic.hare_and_wolves import HareForm
from gui.logic.reversi import ReversiForm
from gui.logic.checkers import CheckersForm
from gui.logic.flume import FlumeForm
from gui.logic.talpa import TalpaForm


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.gameArea.setLayout(QtWidgets.QGridLayout())

        # Connecting slots to action signals
        self.action_about.triggered.connect(self.about)
        self.action_Qt.triggered.connect(self.about_Qt)
        self.action_exit.triggered.connect(self.exit)

        # Toolbar setting
        self.toolBar.addAction(QtGui.QIcon(":/Icons/5-in-a-row.png"),  "Пять в ряд",
                               self.decorator_set_game(FiveForm()))
        self.toolBar.addAction(QtGui.QIcon(":/Icons/Hare&Wolves.png"), "Заяц и волки",
                               self.decorator_set_game(HareForm()))
        self.toolBar.addAction(QtGui.QIcon(":/Icons/reversi.png"), "Реверси",
                               self.decorator_set_game(ReversiForm()))
        self.toolBar.addAction(QtGui.QIcon(":/Icons/Checkers.png"), "Английские шашки",
                               self.decorator_set_game(CheckersForm()))
        self.toolBar.addAction(QtGui.QIcon(":/Icons/Flume.png"), "Флюм",
                               self.decorator_set_game(FlumeForm()))
        self.toolBar.addAction(QtGui.QIcon(":/Icons/talpa.png"), "Тальпа",
                               self.decorator_set_game(TalpaForm()))

    def decorator_set_game(self, game_form: AbstractGameForm):
        def wrapper():
            return self.set_game(game_form)
        return wrapper

    def set_game(self, game_form: AbstractGameForm):
        if self.gameArea.layout().count() == 1:
            self.gameArea.layout().itemAt(0).widget().setParent(None)
        self.gameArea.layout().addWidget(game_form)
        game_form.resizeSignal.connect(self.resize)

    def about(self):
        QtWidgets.QMessageBox.information(self, "О программе",
                                          "Программа 'Коллекция игр', Бакаев А.И., 2021.\n\n"
                                          "Содержит реализации некоторых настольных игр.\n\n"
                                          "Программа разработана на языке Python при использовании библиотеки PyQt.",
                                          buttons=QtWidgets.QMessageBox.Ok,
                                          defaultButton=QtWidgets.QMessageBox.Ok)

    def about_Qt(self):
        QtWidgets.QMessageBox.aboutQt(self)

    @staticmethod
    def exit():
        QtWidgets.qApp.quit()
