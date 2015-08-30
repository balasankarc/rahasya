#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Inspired from the code snippet provided at https://goo.gl/L4J728
# Licensed under GPL 
# TODO: Clarify license

from PySide.QtCore import QDate
from PySide.QtGui import QCalendarWidget, QPalette, QColor
import glob


class WeekCalendar(QCalendarWidget):

    def __init__(self, *args):

        QCalendarWidget.__init__(self, *args)
        self.color = QColor(self.palette().color(QPalette.Highlight))
        self.color.setAlpha(64)
        self.selectionChanged.connect(self.updateCells)

    def paintCell(self, painter, rect, date):

        QCalendarWidget.paintCell(self, painter, rect, date)
        filelist = glob.glob('journal_[0-9]*')
        datelist = []
        for i in filelist:
            l = tuple(i[i.index('_') + 1:].split('_'))
            datelist.append(QDate(int(l[2]), int(l[1]), int(l[0])))
        if date in datelist:
            painter.fillRect(rect, self.color)
