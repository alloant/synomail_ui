from libsynomail.classes import File
import re

from PySide6.QtCore import Qt,QAbstractTableModel, QModelIndex


class FileModel(QAbstractTableModel):
    def __init__(self, files=None):
        super(FileModel, self).__init__()
        self._items = []
        for file in files:
            num = re.findall('\d+',file['file'].name.replace(file['source'],''))
            num = int(num[0]) if num else ''
            self._items.append(file | {"num": num,"main": 0})
        

        self._items.sort(reverse=True,key = lambda file: f"{file['type']}_{file['source']}_{file['num']}_{file['file'].name}")
        
        self._header = ['Type','Source','Name','No','Main']

    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid():
           return None
        #elif role == Qt.CheckStateRole and index.column() == 4:
        elif index.column() == 4:
            if role == Qt.CheckStateRole:
                return str(list(self._items[index.row()].values())[index.column()])
        elif role == Qt.DisplayRole or role == Qt.EditRole:
            return str(list(self._items[index.row()].values())[index.column()])
        
        return None

    def flags(self,index):
        flags = super(FileModel,self).flags(index)
        if index.column() == 4:
            flags |= Qt.ItemIsUserCheckable|Qt.ItemIsEditable
        elif index.column() == 3:
            flags |= Qt.ItemIsEditable
        
        return flags


    def setData(self, index, value, role = Qt.EditRole):
        if value is not None and role == Qt.EditRole:
            self._items[index.row()][list(self._items[index.row()].keys())[index.column()]] = value
            return True
        elif Qt.CheckStateRole and index.column() == 4:
            self._items[index.row()][list(self._items[index.row()].keys())[index.column()]] ^= 1
            self._items[index.row()][list(self._items[index.row()].keys())[index.column()]] *= 2
            return True
        return False

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def columnCount(self, parent=QModelIndex()):
        if self._items:
            return len(list(self._items[0].keys()))
        else:
            return 0
