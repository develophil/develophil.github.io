import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from pandas import DataFrame
import matplotlib.pyplot as plt

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()
        self._set_variable()

    def _set_variable(self):
        self.trade_item_code = "6EZ18"
        print('code : ', self.trade_item_code)

    def _create_kiwoom_instance(self):
        self.setControl("KFOPENAPI.KFOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)
        self.OnReceiveChejanData.connect(self._receive_chejan_data)
        self.OnReceiveMsg.connect(self._receive_msg)
        self.OnReceiveRealData.connect(self._receive_real_data)

    def comm_connect(self):
        self.dynamicCall("CommConnect(1)")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def get_connect_state(self):
        ret = self.dynamicCall("GetConnectState()")
        return ret

    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _get_comm_data(self, tr_code, record_name, index, item_name):
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code,
                               record_name, index, item_name)
        return ret

    def _get_comm_real_data(self, type, fid):
        ret = self.dynamicCall("GetCommRealData(QString, long)", type, fid  )
        return ret

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, stop, hoga, order_no):
        return self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString, QString)",
                         [rqname, screen_no, acc_no, order_type, code, quantity, price, stop, hoga, order_no])

    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    def _receive_msg(self, screen_no, rqname, trcode, msg):
        print(screen_no)
        print(rqname)
        print(trcode)
        print(msg)

    def _receive_real_data(self, sJongmokCode, sRealType, sRealData):
        print(sJongmokCode)
        print(sRealType)
        print(sRealData)

    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        print(gubun)
        print(self.get_chejan_data(9203))
        print(self.get_chejan_data(302))
        print(self.get_chejan_data(900))
        print(self.get_chejan_data(901))

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next):
        print(rqname, " : ", trcode)
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)
        elif rqname == "opw00001_req":
            self._opw00001(rqname, trcode)
        elif rqname == "opw30009_req":
            self._opw30009(rqname, trcode)
        elif rqname == "opw30011_req":
            self._opw30011(rqname, trcode)
        elif rqname == "opw50001_req":
            self._opw50001(rqname, trcode)
        elif rqname == "opw60003_req":
            self._opw60003(rqname, trcode)
        elif rqname == "opw30019_req":
            self._opw30019(rqname, trcode)
        elif rqname == "opc10001_req":
            self._opc10001(rqname, trcode)
        elif rqname == "opc10002_req":
            self._opc10001(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    @staticmethod
    def change_format(data):
        strip_data = data.lstrip('-0')
        if strip_data == '' or strip_data == '.00':
            strip_data = '0'

        format_data = format(int(strip_data), ',d')
        if data.startswith('-'):
            format_data = '-' + format_data

        return format_data

    @staticmethod
    def change_format2(data):
        strip_data = data.lstrip('-0')

        if strip_data == '':
            strip_data = '0'

        if strip_data.startswith('.'):
            strip_data = '0' + strip_data

        if data.startswith('-'):
            strip_data = '-' + strip_data

        return strip_data

    def _opc10001(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            # date = self._get_comm_data(trcode, rqname, i, "영업일자")
            time = self._get_comm_data(trcode, rqname, i, "체결시간")
            open = self._get_comm_data(trcode, rqname, i, "시가")
            high = self._get_comm_data(trcode, rqname, i, "고가")
            low = self._get_comm_data(trcode, rqname, i, "저가")
            price = self._get_comm_data(trcode, rqname, i, "현재가")
            volume = self._get_comm_data(trcode, rqname, i, "거래량")

            # self.ohlcv['date'].append(date)
            self.ohlcv['time'].append(time)
            self.ohlcv['open'].append(open)
            self.ohlcv['high'].append(high)
            self.ohlcv['low'].append(low)
            self.ohlcv['price'].append(price)
            self.ohlcv['volume'].append(volume)

        df = DataFrame(self.ohlcv, columns=['open', 'high', 'low', 'price', 'volume'], index=kiwoom.ohlcv['time'])
        df.sort_index(inplace=True)
        self.append_moving_average(df, 5)
        self.append_moving_average(df, 20)
        self.append_moving_average(df, 60)

        df = df[df['MA60'] == df['MA60']]

        # 결과 그래프 출력
        # plt.figure(1)
        # plt.xlabel('time')
        # plt.ylabel('dollor')
        # plt.show()

        plt.figure(2)
        plt.plot(df['MA5'], 'r', label='5')
        plt.plot(df['MA20'], 'g', label='20')
        plt.plot(df['MA60'], 'b', label='60')
        plt.plot(df['price'], 'k', label='price')
        plt.xlabel('time')
        plt.ylabel('dollor')
        plt.legend(loc=0)
        plt.show()
        print(df)

    @staticmethod
    def append_moving_average(df, days):
        ma = df['price'].rolling(window=days).mean().round(6)
        df.insert(len(df.columns), "MA" + str(days), ma)

        return df

    def get_available_order_count(self, account_number, sell_buy):
        self.set_input_value("계좌번호", account_number)
        self.set_input_value("종목코드", '6EZ18')
        self.set_input_value("비밀번호입력매체", '00')
        self.set_input_value("매도수구분", '1')
        self.set_input_value("해외주문유형", '1')
        self.set_input_value("주문표시가격", '1')
        self.comm_rq_data("opw30011_req", "opw30011", 0, "3000")

    def get_chart_data(self, type, value):
        # opt10012 : 분 단위 데이터 조회.... 이걸로 바꿔야 할듯..
        tr_code = ''
        item_code = '6EZ18'

        if type == 'tick':
            tr_code = 'opc10001'
        elif type == 'minute':
            tr_code = 'opc10002'

        self.set_input_value("종목코드", item_code)
        self.set_input_value("시간단위", value)

        self.ohlcv = {'time': [], 'open': [], 'high': [], 'low': [], 'price': [], 'volume': []}

        self.comm_rq_data(tr_code+"_req", tr_code, 0, "화면번호")

    def reset_opw30009_output(self):
        self.opw30009_output = []

    def _opw30009(self, rqname, trcode):
        # single data
        currency_code = self._get_comm_data(trcode, rqname, 0, "통화코드")
        foreign_currency_deposit = self._get_comm_data(trcode, rqname, 0, "외화예수금")
        receivables = self._get_comm_data(trcode, rqname, 0, "미수금")
        aa= self._get_comm_data(trcode, rqname, 0, "선물청산손익")
        bb= self._get_comm_data(trcode, rqname, 0, "옵션청산손익")
        cc= self._get_comm_data(trcode, rqname, 0, "옵션결제차금")
        dd= self._get_comm_data(trcode, rqname, 0, "선물평가손익")
        ee= self._get_comm_data(trcode, rqname, 0, "옵션평가손익")
        ff= self._get_comm_data(trcode, rqname, 0, "옵션평가차금")
        gg= self._get_comm_data(trcode, rqname, 0, "증거금율")
        hh= self._get_comm_data(trcode, rqname, 0, "원화대용평가금액")
        ii= self._get_comm_data(trcode, rqname, 0, "예탁자산평가")
        jj= self._get_comm_data(trcode, rqname, 0, "익일예탁금")
        kk= self._get_comm_data(trcode, rqname, 0, "위탁증거금")
        ll= self._get_comm_data(trcode, rqname, 0, "미체결증거금")
        mm= self._get_comm_data(trcode, rqname, 0, "포지션증거금")
        nn= self._get_comm_data(trcode, rqname, 0, "유지증거금")
        oo= self._get_comm_data(trcode, rqname, 0, "추가증거금")
        pp= self._get_comm_data(trcode, rqname, 0, "수수료")
        qq= self._get_comm_data(trcode, rqname, 0, "주문가능금액")
        rr= self._get_comm_data(trcode, rqname, 0, "인출가능금액")
        ss= self._get_comm_data(trcode, rqname, 0, "위험도")

        self.opw00018_output.append(currency_code)
        self.opw00018_output.append(Kiwoom.change_format(foreign_currency_deposit))
        self.opw00018_output.append(Kiwoom.change_format(receivables))
        self.opw00018_output.append(Kiwoom.change_format(aa))
        self.opw00018_output.append(Kiwoom.change_format(bb))
        self.opw00018_output.append(Kiwoom.change_format(cc))
        self.opw00018_output.append(Kiwoom.change_format(dd))
        self.opw00018_output.append(Kiwoom.change_format(ee))
        self.opw00018_output.append(Kiwoom.change_format(ff))
        self.opw00018_output.append(Kiwoom.change_format(gg))
        self.opw00018_output.append(Kiwoom.change_format(hh))
        self.opw00018_output.append(Kiwoom.change_format(ii))
        self.opw00018_output.append(Kiwoom.change_format(jj))
        self.opw00018_output.append(Kiwoom.change_format(kk))
        self.opw00018_output.append(Kiwoom.change_format(ll))
        self.opw00018_output.append(Kiwoom.change_format(mm))
        self.opw00018_output.append(Kiwoom.change_format(nn))
        self.opw00018_output.append(Kiwoom.change_format(oo))
        self.opw00018_output.append(Kiwoom.change_format(pp))
        self.opw00018_output.append(Kiwoom.change_format(qq))
        self.opw00018_output.append(Kiwoom.change_format(rr))
        self.opw00018_output.append(Kiwoom.change_format(ss))

    # 주문가능수량조회
    def _opw30011(self, rqname, trcode):
        self.available_buy_count = self._get_comm_data(trcode, rqname, 0, "주문가능수량")
        print('avaliable : {}'.format(self.available_buy_count))

    # 장운영정보조회
    def _opw50001(self, rqname, trcode):
        print('opw50001')

    # 원화외화예수금잔액조회
    def _opw60003(self, rqname, trcode):
        print('opw60003')

    # 해외옵션인수도신청
    def _opw30019(self, rqname, trcode):
        print('opw30019')

if __name__ == "__main__":
    accno = '7006265572'
    item_code = '6EZ18'
    app = QApplication(sys.argv) 
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    # kiwoom.reset_opw00018_output()
    kiwoom.get_chart_data('minute', 30)
    kiwoom.get_available_order_count(accno, '1')
    kiwoom.get_comm_real_data()

    time.sleep(10)
    print('sendorder!!!')
    sendorder = kiwoom.send_order("RQ_1", "4501", "7002650572", 1, "CLJ17", 1, "0", "1", "0", "0")
    print('order : ', sendorder)

