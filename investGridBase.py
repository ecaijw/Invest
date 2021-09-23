# -*- coding: utf-8 -*-

import wx
import wx.grid as gridlib

class InvestGridBase(gridlib.Grid):
    class Const:
        FONT_SIZE_CONTENT = 14
        FONT_NAME = "微软雅黑"

    FONT_SIZE_SEPARATOR = 12
    COLOR_LIGHT_YELLOW = wx.Colour(255, 255, 180)
    COLOR_BACKGROUND_LIGHT_GRAY = wx.Colour(245, 245, 245)
    COLOR_DARK_GREEN = wx.Colour(0, 128, 64)

    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)
        self.EnableEditing(False)

    def GetColorByUpDown(self, number):
        if (number > 0.0):
            return self.COLOR_DARK_GREEN
        return wx.RED

    def SetCellNumberAndColor(self, row, col, argNumber, fieldWidth = -1):
        textNumber = ''
        floatNumber = 0.0
        if (type(argNumber) is str):
            textNumber = argNumber
            if (argNumber.find('%') != -1):
                argNumber = argNumber.strip('%')
            floatNumber = float(argNumber)
        else:
            textNumber = str(argNumber)
            floatNumber = argNumber

        if (fieldWidth != -1): # set field with
            textNumber = "{0:.{1}f}".format(floatNumber, fieldWidth)

        self.SetCellValue(row, col, textNumber)
        self.SetCellTextColour(row, col, self.GetColorByUpDown(floatNumber))

    def setCellFont(self, row, fontColor = wx.BLACK, fontSize = Const.FONT_SIZE_CONTENT, fontName = Const.FONT_NAME):
        # 设置字体格式
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(fontColor)
        font = wx.Font(fontSize, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, fontName)
        attr.SetFont(font)
        self.SetRowAttr(row, attr)


