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
from libsynomail.get_mail import init_config,get_notes_in_folders, manage_files_despacho, register_notes
from libsynomail.nas import init_connection
from libsynomail.register import join_registers

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
        #act = QAction(icon, name.upper(), self)
        act = QAction(icon, status, self)
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
        buttons.append(['outbox','icons/outbox.svg','mail_from_dr','Get mail from dr'])
        buttons.append(['mail-out','icons/mail-out.svg','send','Send mail to cg, asr, r y ctr'])
        #buttons.append('separator')
        #buttons.append(['join-out','icons/cyclone.svg','join-out','Join registers in ToSend'])
        buttons.append('separator')
        buttons.append(['up','icons/up.svg','upload','Upload files from local computer to their inbox'])
        buttons.append('separator')
        buttons.append(['mail-in','icons/mail-in.svg','get_mail','Get mail from cg, asr, r y ctr'])
        buttons.append(['join-in','icons/cyclone.svg','join-in','Join registers in Despacho/Inbox'])
        buttons.append(['inbox','icons/inbox.svg','register','Register mail and assign it to dr'])
        
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
            
            init_config(CONFIG)
            init_connection(CONFIG['user'],self.PASS)
            
            for act in self.toolBar.actions():
                act.setEnabled(True)
        elif sender == 'get_mail':
            logging.info('-------------------------------------')
            logging.info('---- Starting searching new mail ----')

            files = get_notes_in_folders(CONFIG['mail_in'],CONFIG['ctrs'])
            if files:
                fd = FileDialog(files,self)
                if fd.exec() == 1:
                    manage_files_despacho(f"{CONFIG['folders']['despacho']}/Inbox Despacho",fd.model._items)
            
            logging.info('----- Finish searching new mail -----')
            logging.info('-------------------------------------')    
            
        elif sender == 'mail_from_dr':
            logging.info('-------------------------------------')
            logging.info('---- Starting searching notes from dr ----')

            files = get_notes_in_folders(CONFIG['from_dr'],CONFIG['deps'])
            if files:
                fd = FileDialog(files,self)
                if fd.exec() == 1:
                    manage_files_despacho(CONFIG['folders']['to_send'],fd.model._items,is_from_dr=True)
            
            logging.info('----- Finish searching notes from dr -----')
            logging.info('-------------------------------------') 
        elif sender == 'register':
            logging.info('-------------------------------------')
            logging.info('---- Start sending notes to dr and to register them ----')

            register_notes()
            
            logging.info('----- Finish sending notes to dr and to register them -----')
            logging.info('-------------------------------------')
        elif sender == 'send':
            logging.info('-------------------------------------')
            logging.info('---- Start sending notes to cg, asr, r and ctr ----')

            register_notes(is_from_dr = True)
            
            logging.info('----- Finish sending notes to cg, asr, r and ctr -----')
            logging.info('-------------------------------------') 
        elif sender == 'debug':
            if rst == 2:
                logging.getLogger().setLevel(logging.DEBUG)
            else:
                logging.getLogger().setLevel(logging.INFO)
        elif sender == 'join-out':
            join_registers(f"{CONFIG['folders']['to_send']}",flow='out')
        elif sender == 'join-in':
            join_registers(f"{CONFIG['folders']['despacho']}/Inbox Despacho")
        elif sender == 'upload':
            logging.info('Uploading')
            folders = ['asr','r','vc']
            
            for fd in folders:
                if fd == 'asr':
                    path_upload = f"{CONFIG['folders']['local_folder']}/inbox asr"
                elif fd == 'vc':
                    path_upload = f"{CONFIG['folders']['local_folder']}/inbox vc"
                else:
                    path_upload = f"{CONFIG['folders']['local_folder']}/inbox forti"

                if not os.path.exists(path_upload): continue

                notes = [f for f in os.listdir(path_upload) if os.path.isfile(os.path.join(path_upload, f))]
                
                if not notes: continue

                for note in notes:
                    if fd in ['asr','vc']:
                        with open(f"{path_upload}/{note}",mode='rb') as nt:
                            file = io.BytesIO(nt.read())
                            file.name = note
                            logging.info(f"Uploading {note}")
                            if fd == 'asr':
                                dest = f"/team-folders/Mail {fd}/Mail from {fd}"
                            else:
                                dest = f"/team-folders/Mail vc/New from Rome, r and asr to vc"
                            #con.nas.upload_file(file,dest)
                    else:
                        read_eml(f"{path_upload}/{note}")

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
