#!/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import io

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QToolBar,
    QPushButton, QWidget,
    QMessageBox, QFileDialog, QDialog, QDialogButtonBox,
    QPlainTextEdit, QLineEdit, QCheckBox,
    QTableView,
    QHBoxLayout, QVBoxLayout
    )

from PySide6.QtCore import Qt, QSize, QDir, QSettings
from PySide6.QtGui import QKeySequence, QIcon, QAction

import logging

from synomail_ui import _ROOT, CONFIG
from synomail_ui.models import FileModel

from libsynomail.syneml import read_eml
from libsynomail.get_mail import get_notes_in_folders, generate_register, manage_files_despacho, register_notes
from libsynomail.send_mail import init_send_mail
import libsynomail.connection as con

# Uncomment below for terminal log messages
# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

class FileDialog(QDialog):
    def __init__(self, files, parent = None):
        super(FileDialog, self).__init__()
        self.files = files
        self.model = FileModel(files)
        self.initUI()

    def initUI(self):
        view = QTableView()
        view.setModel(self.model)
        #view.horizontalHeader().adjustPositions()
        #view.verticalHeader().hide()
        view.resizeColumnsToContents()
        view.setAlternatingRowColors(True)
        view.setContentsMargins(0, 0, 0, 0)
        
        button_box = QDialogButtonBox()
        ok_button = button_box.addButton("OK", QDialogButtonBox.AcceptRole)
        cancel_button = button_box.addButton("Cancel", QDialogButtonBox.RejectRole)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout = QVBoxLayout(self)
        layout.addWidget(view)
        layout.addWidget(button_box)

        

class mainWindow(QMainWindow, QPlainTextEdit):
    def __init__(self):
        super(mainWindow,self).__init__()
        self.initUI()
    
    def new_action(self,icon_name,icon_path,name,status="",enable = True):
        #icon = QIcon.fromTheme(icon_name, QIcon(icon_path))
        icon = QIcon.fromTheme(icon_name, QIcon(os.path.join(_ROOT,icon_path)))
        act = QAction(icon, name.upper(), self)
        act.setObjectName(name)
        act.setShortcuts(QKeySequence.Open)
        act.setStatusTip(status)
        act.setEnabled(enable)
        act.triggered.connect(self.toolBarActions)

        return act
        
    def toolBar(self):
        self.toolBar = QToolBar(self.tr('File toolbar'), self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.toolBar.setIconSize(QSize(22,22))
        
        self.le_pass = QLineEdit()
        self.le_pass.setMaximumWidth(200)
        self.le_pass.setEchoMode(QLineEdit.Password)
        self.le_pass.setObjectName('pass_return')
        self.le_pass.returnPressed.connect(self.toolBarActions)
        self.toolBar.addWidget(self.le_pass)
        
        self.toolBar.addAction(self.new_action('key','icons/key.svg','pass','Password'))

        self.toolBar.addSeparator()

        buttons = [] 
        buttons.append(['vcs-pull','icons/email-download.svg','get_mail','Get mail from cg, asr, r y ctr'])
        buttons.append(['vcs-pull','icons/cabinet.svg','register','Register mail despacho and send message to d'])
        buttons.append('separator')
        buttons.append(['vcs-pull','icons/letter.svg','mail_from_dr','Get notes from dr'])
        buttons.append(['vcs-pull','icons/send.svg','send','Send mail to ctr'])
        buttons.append('separator')
        buttons.append(['vcs-pull','icons/block-up-bracket.svg','upload','Upload files from cg and asr'])

        for but in buttons:
            if but == 'separator':
                self.toolBar.addSeparator()
            else:
                self.toolBar.addAction(self.new_action(but[0],but[1],but[2],but[3],False))
        
        self.toolBar.addSeparator()
        self.ck_debug = QCheckBox("DEBUG")
        self.ck_debug.setObjectName('debug')
        self.ck_debug.stateChanged.connect(self.toolBarActions)
        self.toolBar.addWidget(self.ck_debug)
        

    def toolBarActions(self,rst = None):
        sender = self.sender().objectName()
        if sender in ['pass','pass_return']:
            self.PASS = self.le_pass.text()
            self.le_pass.clear()
            con.init_nas(CONFIG['user'],self.PASS) 
            for act in self.toolBar.actions():
                act.setEnabled(True)
        elif sender == 'get_mail':
            logging.info('-------------------------------------')
            logging.info('---- Starting searching new mail ----')

            files = get_notes_in_folders(CONFIG['teams'],CONFIG['ctrs'],CONFIG['DEBUG'])
            fd = FileDialog(files,self)
            if fd.exec() == 1:
                manage_files_despacho(f"{CONFIG['folders']['despacho']}/Inbox Despacho",fd.model._items)
            
            logging.info('----- Finish searching new mail -----')
            logging.info('-------------------------------------')    
            
        elif sender == 'mail_from_dr':
            logging.info('-------------------------------------')
            logging.info('---- Starting searching notes from dr ----')

            files = get_notes_in_folders(CONFIG['from_dr'],CONFIG['deps'],CONFIG['DEBUG'])
            fd = FileDialog(files,self)
            if fd.exec() == 1:
                manage_files_despacho(CONFIG['folders']['to_send'],fd.model._items,is_from_dr=True)
            
            logging.info('----- Finish searching notes from dr -----')
            logging.info('-------------------------------------') 
        elif sender == 'register':
            logging.info('-------------------------------------')
            logging.info('---- Start sending notes to dr and to register them ----')

            register_notes(CONFIG['folders']['despacho'],CONFIG['folders']['archive'],CONFIG['deps'])
            
            logging.info('----- Finish sending notes to dr and to register them -----')
            logging.info('-------------------------------------')
        elif sender == 'send':
            logging.info('-------------------------------------')
            logging.info('---- Start sending notes to cg, asr, r and ctr ----')

            register_notes(CONFIG['folders']['to_send'],CONFIG['folders']['archive'],CONFIG['ctrs']|CONFIG['r'],is_from_dr = True,path_download=CONFIG['folders']['local_folder'])
            
            logging.info('----- Finish sending notes to cg, asr, r and ctr -----')
            logging.info('-------------------------------------') 
        elif sender == 'debug':
            if rst == 2:
                logging.getLogger().setLevel(logging.DEBUG)
            else:
                logging.getLogger().setLevel(logging.INFO)
        elif sender == 'upload':
            logging.info('Uploading')
            folders = ['asr','r']
            
            for fd in folders:
                if fd == 'asr':
                    path_upload = f"{CONFIG['folders']['local_folder']}/asr_in"
                else:
                    path_upload = f"{CONFIG['folders']['local_folder']}/forti_in"

                notes = [f for f in os.listdir(path_upload) if os.path.isfile(os.path.join(path_upload, f))]
                for note in notes:
                    if fd == 'asr':
                        with open(f"{path_upload}/{note}",mode='rb') as nt:
                            file = io.BytesIO(nt.read())
                            file.name = note
                            logging.info(f"Uploading {note}")
                            con.nas.upload_file(file,f"/team-folders/Mail {fd}/Mail from {fd}")
                    else:
                        read_eml(f"{path_upload}/{note}")

            """
            mypath = f"{CONFIG['folders']['local_folder']}/inbox vc"
            notes = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
            for note in notes:
               with open(f"{mypath}/{note}",mode='rb') as nt:
                    file = io.BytesIO(nt.read())
                    file.name = note
                    logging.info(f"Uploading {note}")
                    con.nas.upload_file(file,f"/team-folders/Mail vc/New from Rome, r and asr to vc")
            """
            logging.info('Uploading is over')

        
    def initUI(self):
        self.toolBar()

        logTextBox = QTextEditLogger(self)
        # You can format what is printed to text box
        logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(logTextBox)
        # You can control the logging level
        logging.getLogger().setLevel(logging.INFO)

        self.centralWidget = QWidget()
        layout = QVBoxLayout(self.centralWidget)

        layout.addWidget(logTextBox.widget)
        
        self.setCentralWidget(self.centralWidget)
        self.statusBar().showMessage("Register Kamet")

def main():
    app = QApplication(sys.argv)
    #settings = QSettings("alloant","quotes")

    #app.setStyleSheet(qdarktheme.load_stylesheet())

    ex = mainWindow()
    ex.setGeometry(100, 100, ex.width()+600, 600)
    ex.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
