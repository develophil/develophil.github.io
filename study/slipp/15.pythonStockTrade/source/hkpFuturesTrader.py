import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import time

from KiwoomW import Kiwoom

form_class = uic.loadUiType("hkpFuturesTrader.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.trade_stocks_done = False

        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)

        self.timer2 = QTimer(self)
        self.timer2.start(1000 *10)
        self.timer2.timeout.connect(self.timeout2)

        accouns_num = int(self.kiwoom.get_login_info("ACCOUNT_CNT"))
        accounts = self.kiwoom.get_login_info("ACCNO")

        accounts_list = accounts.split(';')[0:accouns_num]
        self.comboBox.addItems(accounts_list)

        self.lineEdit.textChanged.connect(self.code_changed)
        self.pushButton.clicked.connect(self.send_order)
        self.pushButton_2.clicked.connect(self.check_balance)
        self.pushButton_4.clicked.connect(self.kiwoom.is_available_trading_time)
        # self.pushButton_4.clicked.connect(self.check_available_order)

        # self.load_buy_sell_list()

    def trade_stocks(self):
        hoga_lookup = {'지정가': "00", '시장가': "03"}

        f = open("buy_list.txt", 'rt')
        buy_list = f.readlines()
        f.close()

        f = open("sell_list.txt", 'rt')
        sell_list = f.readlines()
        f.close()

        # account
        account = self.comboBox.currentText()

        # buy list
        for row_data in buy_list:
            split_row_data = row_data.split(';')
            hoga = split_row_data[2]
            code = split_row_data[1]
            num = split_row_data[3]
            price = split_row_data[4]

            if split_row_data[-1].rstrip() == '매수전':
                self.kiwoom.send_order("send_order_req", "0101", account, 1, code, num, price, hoga_lookup[hoga], "")

        # sell list
        for row_data in sell_list:
            split_row_data = row_data.split(';')
            hoga = split_row_data[2]
            code = split_row_data[1]
            num = split_row_data[3]
            price = split_row_data[4]

            if split_row_data[-1].rstrip() == '매도전':
                self.kiwoom.send_order("send_order_req", "0101", account, 2, code, num, price, hoga_lookup[hoga], "")

        # buy list
        for i, row_data in enumerate(buy_list):
            buy_list[i] = buy_list[i].replace("매수전", "주문완료")

        # file update
        f = open("buy_list.txt", 'wt')
        for row_data in buy_list:
            f.write(row_data)
        f.close()

        # sell list
        for i, row_data in enumerate(sell_list):
            sell_list[i] = sell_list[i].replace("매도전", "주문완료")

        # file update
        f = open("sell_list.txt", 'wt')
        for row_data in sell_list:
            f.write(row_data)
        f.close()

    def load_buy_sell_list(self):
        f = open("buy_list.txt", 'rt')
        buy_list = f.readlines()
        f.close()

        f = open("sell_list.txt", 'rt')
        sell_list = f.readlines()
        f.close()

        row_count = len(buy_list) + len(sell_list)
        self.tableWidget_4.setRowCount(row_count)

        # buy list
        for j in range(len(buy_list)):
            row_data = buy_list[j]
            split_row_data = row_data.split(';')
            split_row_data[1] = self.kiwoom.get_master_code_name(split_row_data[1].rsplit())

            for i in range(len(split_row_data)):
                item = QTableWidgetItem(split_row_data[i].rstrip())
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                self.tableWidget_4.setItem(j, i, item)

        # sell list
        for j in range(len(sell_list)):
            row_data = sell_list[j]
            split_row_data = row_data.split(';')
            split_row_data[1] = self.kiwoom.get_master_code_name(split_row_data[1].rstrip())

            for i in range(len(split_row_data)):
                item = QTableWidgetItem(split_row_data[i].rstrip())
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                self.tableWidget_4.setItem(len(buy_list) + j, i, item)

        self.tableWidget_4.resizeRowsToContents()

    def code_changed(self):
        code = self.lineEdit.text()
        name = self.kiwoom.get_master_code_name(code)
        self.lineEdit_2.setText(name)

    def send_order(self):
        order_type_lookup = {'신규매도': 1, '신규매수': 2, '매도취소': 3, '매수취소': 4, '매도정정': 5, '매수정정': 6}
        hoga_lookup = {'시장가': "1", '지정가': "2", 'STOP': "3", 'STOP LIMIT': "4"}

        account = self.comboBox.currentText()
        order_type = self.comboBox_2.currentText()
        code = self.lineEdit.text()
        hoga = self.comboBox_3.currentText()
        num = self.spinBox.value()
        price = self.doubleSpinBox.value()

        order_result = self.kiwoom.send_order("send_order_req", "0101", account, order_type_lookup[order_type], code, num, price, price, hoga_lookup[hoga], "")
        print('order : ', order_result)
        self.statusbar.showMessage(self.kiwoom.rq_msg)
        # self.check_balance()

    def timeout(self):
        market_start_time = QTime(9, 0, 0)
        current_time = QTime.currentTime()

        if current_time > market_start_time and self.trade_stocks_done is False:
            self.trade_stocks()
            self.trade_stocks_done = True

        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        state = self.kiwoom.get_connect_state()
        if state == 1:
            state_msg = "서버 연결 중"
        else:
            state_msg = "서버 미 연결 중"

        self.statusbar.showMessage(state_msg + " | " + time_msg)

    def timeout2(self):
        if self.checkBox.isChecked():
            # self.check_balance()
            self.kiwoom.get_chart_data('minute', 30)

    def check_available_order(self):
        order_type_lookup = {'신규매수': 1, '신규매도': 2, '매수취소': 3, '매도취소': 4}
        order_type = self.comboBox_2.currentText()
        account = self.comboBox.currentText()

        ret = self.kiwoom.get_available_order_count(account, order_type_lookup[order_type])
        print('available ret : ', ret)

        if ret is not None:
            self.spin_box.setText(self.kiwoom.available_buy_count)

    def check_balance(self):
        self.kiwoom.reset_opw30009_output()
        account_number = self.comboBox.currentText()
        account_number = account_number.split(';')[0]
        print('balance : ', account_number)
        self.kiwoom.set_input_value("계좌번호", account_number)
        self.kiwoom.set_input_value("비밀번호", '0000')
        self.kiwoom.set_input_value("비밀번호입력매체", '00')
        ret = self.kiwoom.comm_rq_data("opw30009_req", "opw30009", 0, "3009")
        print('check_balance ret : ', ret)

        # while self.kiwoom.remained_data:
        #     time.sleep(0.2)
        #     self.kiwoom.set_input_value("계좌번호", account_number)
        #     self.kiwoom.set_input_value("비밀번호", '0000')
        #     self.kiwoom.set_input_value("비밀번호입력매체", '00')
        #     self.kiwoom.comm_rq_data("opw30009_req", "opw30009", 2, "3009")

        output_length = len(self.kiwoom.opw30009_output)
        print('len : ', output_length)
        if output_length > 0:
            for i in range(1, 22):
                print(i, ' : ', self.kiwoom.opw30009_output[i - 1])
                item = QTableWidgetItem(str(self.kiwoom.opw30009_output[i - 1]))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.balanceTable.setItem(0, i, item)

            self.balanceTable.resizeRowsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()