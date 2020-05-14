from __future__ import print_function
import pickle
import os.path
from datetime import datetime
import sys

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt
from methods import load_from_vk
from prototype_ui import Ui_MainWindow
import pandas as pd

class DataFrameModel(QtCore.QAbstractTableModel):
    DtypeRole = QtCore.Qt.UserRole + 1000
    ValueRole = QtCore.Qt.UserRole + 1001

    def __init__(self, df=pd.DataFrame(), parent=None):
        super(DataFrameModel, self).__init__(parent)
        self._dataframe = df

    def setDataFrame(self, dataframe):
        self.beginResetModel()
        self._dataframe = dataframe.copy()
        self.endResetModel()

    def dataFrame(self):
        return self._dataframe

    dataFrame = QtCore.pyqtProperty(pd.DataFrame, fget=dataFrame, fset=setDataFrame)

    @QtCore.pyqtSlot(int, QtCore.Qt.Orientation, result=str)
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._dataframe.columns[section]
            else:
                return str(self._dataframe.index[section])
        return QtCore.QVariant()

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._dataframe.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return self._dataframe.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount() \
            and 0 <= index.column() < self.columnCount()):
            return QtCore.QVariant()
        row = self._dataframe.index[index.row()]
        col = self._dataframe.columns[index.column()]
        dt = self._dataframe[col].dtype

        val = self._dataframe.iloc[row][col]
        if role == QtCore.Qt.DisplayRole:
            return str(val)
        elif role == DataFrameModel.ValueRole:
            return val
        if role == DataFrameModel.DtypeRole:
            return dt
        return QtCore.QVariant()

    def roleNames(self):
        roles = {
            QtCore.Qt.DisplayRole: b'display',
            DataFrameModel.DtypeRole: b'dtype',
            DataFrameModel.ValueRole: b'value'
        }
        return roles



if __name__== "__main__":

	wtf = 'wtf'
	class mywindow(QtWidgets.QMainWindow):

		def __init__(self):
			super(mywindow, self).__init__()
			self.ui = Ui_MainWindow()
			self.ui.setupUi(self)
			self.ui.pushButton.clicked.connect(self.uploadData)
        
		def uploadData(self):

			data = load_from_vk(self.ui.lineEdit.text(),
				self.ui.date_from.date().toPyDate(),
				self.ui.date_to.date().toPyDate())
			model = DataFrameModel(data)
			self.ui.tableView.setModel(model)


	app = QtWidgets.QApplication([])
	application = mywindow()
	application.show()
	 
	sys.exit(app.exec())