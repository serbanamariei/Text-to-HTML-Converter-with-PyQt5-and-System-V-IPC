import sys
import os
from PyQt5 import QtWidgets, uic
import sysv_ipc

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        uic.loadUi('interfata.ui', self)

        self.btn_browse.clicked.connect(self.choose_file)
        self.btn_convert.clicked.connect(self.convert_text_to_html)
        self.btn_send.clicked.connect(self.send_to_c)
        self.show()

    def choose_file(self):
        filename, _=QtWidgets.QFileDialog.getOpenFileName(self, 'Selecteaza fisier text')
        if filename:
            self.line_path.setText(filename)

    def convert_text_to_html(self):
        path=self.line_path.text()
        if not os.path.exists(path):
            return

        with open(path,'r',encoding='utf-8') as f:
            lines=f.readlines()

        html = f"<h1>{lines[0].strip()}</h1>\n"
        for line in lines[1:]:
            if line.strip():
                html += f"<p>{line.strip()}</p>\n"

        self.text_preview.setPlainText(html)

    def send_to_c(self):
        try:
            key=1234
            queue=sysv_ipc.MessageQueue(key,sysv_ipc.IPC_CREAT)
            continut=self.text_preview.toPlainText()
            queue.send(continut.encode('utf-8'),type=1)

            print(f"mesajul a fost pus in coada {key}")
        except Exception as e:
            print(f"Eroare: {e}")

app = QtWidgets.QApplication(sys.argv)
window = App()
sys.exit(app.exec_())