# coding=utf-8
import sys
import text2mp3
import os
import asyncio
from mainui import QtWidgets, Ui_MainWindow, QtCore


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

per = {
    "度小萌": 111,
    "度小宇": 1,
    "度小美": 0,
    "度逍遥": 3,
    "度丫丫": 4,
    "度博文": 106,
    "度小童": 110,
    "度米朵": 103,
    "度小娇": 5,
}

files = {}


def log(s):
    ui.log.append(s)


# 初始化配音演员
for item in per.keys():
    ui.comboBox_per.addItem(item)


def slider_spd_changed(*args, **kargs):
    ui.v_spd.setText(str(ui.slider_spd.value()))


ui.v_spd.setText(str(ui.slider_spd.value()))
ui.slider_spd.valueChanged.connect(slider_spd_changed)


def slider_pit_changed(*args, **kargs):
    ui.v_pit.setText(str(ui.slider_pit.value()))


ui.v_pit.setText(str(ui.slider_pit.value()))
ui.slider_pit.valueChanged.connect(slider_pit_changed)


def slider_vol_changed(*args, **kargs):
    ui.v_vol.setText(str(ui.slider_vol.value()))


ui.v_vol.setText(str(ui.slider_vol.value()))
ui.slider_vol.valueChanged.connect(slider_vol_changed)


# 初始化文件拖拽


def dragEnterEvent_filelist(event):
    if event.mimeData().hasUrls:
        event.accept()
    else:
        event.ignore()


def dragMoveEvent_filelist(event):
    if event.mimeData().hasUrls:
        try:
            event.setDropAction(QtCore.Qt.CopyAction)
        except Exception as e:
            log(e)
        event.accept()
    else:
        event.ignore()


def dropEvent_filelist(event):
    try:
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                filePath = str(url.toLocalFile())
                if files.get(filePath):
                    continue
                files[filePath] = True
                ui.filelist.addItem(filePath)

                if ui.out_path.text() == "":
                    if os.path.isfile(filePath):
                        filePath = os.path.dirname(filePath)
                    ui.out_path.setText(filePath)
        else:
            event.ignore()
    except Exception as e:
        log(e)


def keyPressEvent_filelist(event):
    if event.key() == QtCore.Qt.Key_D:
        for item in ui.filelist.selectedItems():
            files.pop(ui.filelist.currentItem().text())
            ui.filelist.takeItem(ui.filelist.indexFromItem(item).row())


ui.filelist.setAcceptDrops(True)
# ui.filelist.setSelectionMode(QtWidgets.QListWidget.MultiSelection)
ui.filelist.dragEnterEvent = dragEnterEvent_filelist
ui.filelist.dragMoveEvent = dragMoveEvent_filelist
ui.filelist.dropEvent = dropEvent_filelist
ui.filelist.keyPressEvent = keyPressEvent_filelist


def dragEnterEvent_output(event):
    if event.mimeData().hasUrls:
        event.accept()
    else:
        event.ignore()


def dragMoveEvent_output(event):
    if event.mimeData().hasUrls:
        try:
            event.setDropAction(QtCore.Qt.CopyAction)
        except Exception as e:
            log(e)
        event.accept()
    else:
        event.ignore()


def dropEvent_output(event):
    try:
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()

            url = event.mimeData().urls()[0]
            targetPath = str(url.toLocalFile())

            if os.path.isfile(targetPath):
                targetPath = os.path.dirname(targetPath)

            ui.out_path.setText(targetPath)
        else:
            event.ignore()
    except Exception as e:
        log(e)


ui.out_path.setAcceptDrops(True)
ui.out_path.dragEnterEvent = dragEnterEvent_output
ui.out_path.dragMoveEvent = dragMoveEvent_output
ui.out_path.dropEvent = dropEvent_output


async def generate():
    ui.log.setText("")
    outPath = ui.out_path.text()
    if outPath == "" or not os.path.exists(outPath):
        log("输出目录为空")
        return
    text2mp3.options['per'] = int(per[ui.comboBox_per.currentText()])
    text2mp3.options['spd'] = ui.slider_spd.value()
    text2mp3.options['pit'] = ui.slider_pit.value()
    text2mp3.options['vol'] = ui.slider_vol.value()
    try:
        for filename in files.keys():
            log("正在处理" + filename)
            fileEncoding = ui.lineEdit_code.text()
            fileEncoding = fileEncoding == "" and 'utf8' or fileEncoding
            filecontent = await text2mp3.get_file_content(filename, fileEncoding)
            filecontent = text2mp3.make_data(filecontent)
            filename = os.path.split(filename)[-1]
            filename = os.path.splitext(filename)[0]
            try:
                mp3FileContent = await text2mp3.text2mp3str(filecontent)
                with open(ui.out_path.text() + '/' + filename + '.mp3', 'wb') as fp:
                    fp.write(mp3FileContent)
                    fp.close()
                    log("处理完成")
            except Exception as e:
                log(e)

    except Exception as e:
        log(e)


def gen_clicked(*args, **kargs):
    asyncio.run(generate())


ui.btn_gen.clicked.connect(gen_clicked)

def btn_clear_onclick(*args, **kargs):
    ui.filelist.clear()
    files.clear()

ui.btn_clear.clicked.connect(btn_clear_onclick)

if __name__ == "__main__":
    MainWindow.show()
    sys.exit(app.exec_())
