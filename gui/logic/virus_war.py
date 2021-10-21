# -*- coding: utf-8 -*-


from games.virus_war import *
from gui.logic.reversi import *


class VirusCell(ReversiCell):
    # Paths to the icons
    ICONS = (None, ":/Icons/greenVirus.png", ":/Icons/greenDeadVirus.png",
             ":/Icons/purpleVirus.png", ":/Icons/purpleDeadVirus.png")
    INNER_COLOR1 = QtGui.QColor(150, 250, 250)
    INNER_COLOR2 = QtGui.QColor(150, 200, 250)
    OUTER_COLOR = QtGui.QColor(0, 0, 0)
    LAST_TURN_COLOR = QtGui.QColor(250, 0, 0)


class VirusForm(ReversiForm):
    DIFFICULTY_LEVELS = {'Легко': {'max_depth': 0, 'randomizing': 20}, 'Среднее': {'max_depth': 0, 'randomizing': 5},
                         'Сложно': {'max_depth': 0}}
    BOARD_SIZES = ('10', '11', '12', '13', '14', '15')
    PLAYERS = ('Зелёные', 'Фиолетовые')
    RULES = "Война вирусов.\n\n" \
            "Игра для двух игроков, которая имитирует развитие двух колоний вирусов, которые развиваются сами и " \
            "уничтожают друг друга. В игре используется прямоугольная доска любых размеров.\nИгра начинается с " \
            "пустой доски. У каждого игрока имеется неограниченное кол-во 'вирусов' своего цвета: Зелёного и " \
            "Фиолетового.\nИгроки ходят по очереди. Начинает игрок, играющий Зелёными 'вирусами'.\nКаждый ход " \
            "состоит из трёх 'шагов'. Каждый 'шаг' является либо размножением, либо поглощением (убийство):\n " \
            "'размножение' - это выставление нового 'вируса' своего цвета в любую 'доступную' пустую клетку доски;" \
            "\n 'поглощение' - это 'убийство' одного из вирусов противника, находящегося на 'доступной' клетке. В " \
            "этом случае 'вирус' противника в клетке заменяется на специальную 'мёртвую' фишку цвета игрока. 'Убитые'" \
            " остаются неизменными на доске до конца партии, т.е. они не могут быть 'оживлены', 'восстановлены' или" \
            " удалены с доски.\nКлетка является 'доступной' в следующих случаях:\n - если клетка непосредственно " \
            "соприкасается (по вертикали, горизонтали или диагонали) с живым 'вирусом' игрока (даже, если этот " \
            "'вирус' был помещен на доску одним из предыдущих 'шагов' в течение того же хода);\n - если между " \
            "клеткой и 'вирусом' игрока, уже находящимся на доске, есть цепочка из 'убитых' вирусов противника, т.е." \
            " цепочка из соприкасающихся (по вертикали, горизонтали или диагонали) 'мертвых' вирусов цвета игрока " \
            "(даже, если эти вирусы были убиты в результате одного из предыдущих 'шагов' в течение того же хода).\n" \
            "Игрок обязан сделать все 3 'шага' каждый ход. Если игрок не может сделать очередной 'шаг', то он " \
            "проигрывает партию."
    Board_Class = Virus_war
    Cell_Class = VirusCell

    def update_values(self):
        available_moves = set(self.party.board.legal_moves)
        for i in reversed(range(self.boardField.count())):
            w = self.boardField.itemAt(i).widget()
            value = self.party.board.get_value(w.x, w.y)
            w.value = value
            if value:
                w.isAvailable = False
            if (w.x, w.y) in available_moves:
                w.status = 1
                w.isAvailable = True
            else:
                w.isAvailable = False
                w.status = 0
            w.update()
        if self.party.board.last_move:
            x, y = self.party.board.last_move
            self.boardField.itemAtPosition(x, y).widget().status = 2
            self.boardField.itemAtPosition(x, y).widget().update()