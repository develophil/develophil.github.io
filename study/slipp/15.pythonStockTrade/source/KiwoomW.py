from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from pandas import DataFrame
from enums.PyEnum import TradeFlags

class Kiwoom(QAxWidget):

    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()
        self._set_variable()
        self.reset_opw30009_output()
        self._set_start_time()

    def _set_variable(self):

        self.trade_item_code = '6EZ18'
        self.scr_no = '1001'
        self.rq_msg = ""
        self.remained_data = False
        self.tradable = True
        self.trade_flag = TradeFlags.BEFORE_BUY
        self.is_ma_status_changed = False

    def _set_start_time(self):
        self.dynamicCall("GetCommonFunc(QString, QString)", "SetStartTime", self.scr_no+";"+self.trade_item_code)

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
        print('rqname : {}, trcode : {}, next: {}, screenno: {}'.format(rqname, trcode, next, screen_no))
        self.dynamicCall("CommRqData(QString, QString, QString, QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _get_comm_func(self, func_name, params):
        ret = self.dynamicCall("GetCommonFunc(QString, QString)", func_name, params)
        return ret

    def _get_comm_data(self, tr_code, record_name, index, item_name):
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code,
                               record_name, index, item_name)
        return ret

    def _get_comm_full_data(self, tr_code, record_name, gubun):
        ret = self.dynamicCall("GetCommFullData(QString, QString, long)", tr_code,
                               record_name, gubun)
        return ret

    def _get_comm_real_data(self, type, fid):
        ret = self.dynamicCall("GetCommRealData(QString, long)", type, fid)
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
        print("_receive_msg screen_no:{}, rqname:{}, trcode:{}, msg:{}".format(screen_no, rqname, trcode, msg))
        self.rq_msg = msg

    '''
    # print("receive_real_data sJongmokCode:{}, sRealType:{}, sRealData:{}".format(sJongmokCode, sRealType, sRealData))
    - 화면번호(ScrNo), 화면명(RQName), 종목코드(JongCode), RealType(해외선물시세,해외옵션시세) 
    - 수신데이타
    전문(구분(1) + 날짜시간(20) + MA1(20) + MA2(20) + MA3(20) + MA4(20) + MA5(20)
    = > 구분        0: 기존        마지막시간에        업데이트, 1: 신규시간        추가

    - 예) Cstring strVal = GetCommonFunc("GetRealMA",1000;분차트;6AH17;해외선물시세");
    '''
    def _receive_real_data(self, sJongmokCode, sRealType, sRealData):
        real_val = self._get_comm_func("GetRealMA", self.scr_no + ";opc10002_req;"+sJongmokCode+";"+sRealType)
        print('real val : ', real_val)
        gubun = real_val[0:1]
        time = real_val[1:21].strip()
        ma5 = float(real_val[21:41])
        ma20 = float(real_val[41:61])
        ma60 = float(real_val[61:81])
        ma120 = float(real_val[81:101])
        ma250 = float(real_val[101:121])

        print('gubun : {}, time : {}, ma : {},{},{},{},{}'.format(gubun, time, float(ma5), float(ma20), float(ma60), float(ma120), float(ma250)))

        if self.trade_flag is TradeFlags.BEFORE_BUY:
            is_ascending = self.is_moving_average_order_ascending([ma5, ma20, ma60])
            print(is_ascending)
            if is_ascending is True:
                self.trade_flag = TradeFlags.BUY

        if self.trade_flag is TradeFlags.BEFORE_SELL:
            is_descending = self.is_moving_average_order_descending([ma5, ma20, ma60])
            print(is_descending)
            if is_descending is True:
                self.trade_flag = TradeFlags.SELL

    def is_moving_average_order_ascending(self, ma_list):
        before = -9999999
        for ma in ma_list:
            if ma <= before:
                return False
            else:
                before = ma
        return True

    def is_moving_average_order_descending(self, ma_list):
        return self.is_moving_average_order_ascending(reversed(ma_list))

    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        '''
          [ Real Name : 주문체결 ]

          [9201]      =     계좌번호
          [9203]      =     주문번호
          [9001]      =     종목코드
          [907]       =     매도수구분
          [905]       =     주문구분
          [904]       =     원주문번호
          [302]       =     종목명
          [906]       =     주문유형
          [900]       =     주문수량
          [901]       =     주문가격
          [13333]     =     조건가격
          [13330]     =     주문표시가격
          [13332]     =     조건표시가격
          [902]       =     미체결수량
          [913]       =     주문상태
          [919]       =     반대매매여부
          [8046]      =     거래소코드
          [947]       =     FCM코드
          [8043]      =     통화코드
          [908]       =     주문시간

        :param gubun:
        :param item_cnt:
        :param fid_list:
        :return:
        '''

        print("_receive_chejan_data - ", gubun, item_cnt, fid_list)
        print(self.get_chejan_data(9203))
        print(self.get_chejan_data(302))
        print(self.get_chejan_data(900))
        print(self.get_chejan_data(901))

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next):
        print('_receive_tr_data | screen_no:{}, rqname:{}, trcode:{}, record_name:{}, next:{}'.format(screen_no, rqname, trcode, record_name, next))
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False
        print('remained data : ', self.remained_data)

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
        elif rqname == "send_order_req":
            print('end')

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
        print('total count : ', data_cnt)

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

        df = DataFrame(self.ohlcv, columns=['open', 'high', 'low', 'price', 'volume'], index=self.ohlcv['time'])
        df.sort_index(inplace=True)
        # self.append_moving_average(df, 5)
        # self.append_moving_average(df, 20)
        # self.append_moving_average(df, 60)

        # df = df[df['MA60'] == df['MA60']]

        print('dataframe result : ', df)
        next_flag = '0'   # 0: 처음, 1: 다음
        ma_val = self._get_comm_func("GetMA", self.scr_no + ";" + rqname + ";"+next_flag+";5;20;60;120;250")
        # ma_val2 = self._get_comm_func("GetMA", "1001;" + rqname + ";1;0;5;20;60;120;250")
        print('ma val')
        print(ma_val)
        # print('ma val2')
        # print(ma_val2)

        # 결과 그래프 출력
        # plt.figure(1)
        # plt.xlabel('time')
        # plt.ylabel('dollor')
        # plt.show()

        # plt.figure(2)
        # plt.plot(df['MA5'], 'r', label='5')
        # plt.plot(df['MA20'], 'g', label='20')
        # plt.plot(df['MA60'], 'b', label='60')
        # plt.plot(df['price'], 'k', label='price')
        # plt.xlabel('time')
        # plt.ylabel('dollor')
        # plt.legend(loc=0)
        # plt.show()

    @staticmethod
    def append_moving_average(df, days):
        ma = df['price'].rolling(window=days).mean().round(6)
        df.insert(len(df.columns), "MA" + str(days), ma)

        return df

    def get_available_order_count(self, account_number, sell_buy):
        print('accno : {}, sell_buy : {}'.format(account_number, sell_buy))
        self.set_input_value("계좌번호", account_number)
        self.set_input_value("비밀번호", '0000')
        self.set_input_value("비밀번호입력매체", '00')
        self.set_input_value("종목코드", '6EZ18')
        self.set_input_value("매도수구분", '1')
        self.set_input_value("해외주문유형", '1')
        self.set_input_value("주문표시가격", '1')
        return self.comm_rq_data("opw30011_req", "opw30011", 0, "4868")

    def get_chart_data(self, type, value):
        # opt10012 : 분 단위 데이터 조회.... 이걸로 바꿔야 할듯..
        tr_code = ''

        if type == 'tick':
            tr_code = 'opc10001'
        elif type == 'minute':
            tr_code = 'opc10002'

        self.set_input_value("종목코드", self.trade_item_code)
        self.set_input_value("시간단위", value)

        self.ohlcv = {'time': [], 'open': [], 'high': [], 'low': [], 'price': [], 'volume': []}

        self.comm_rq_data(tr_code+"_req", tr_code, 0, '1001')

    def reset_opw30009_output(self):
        self.opw30009_output = []

    def _opw30009(self, rqname, trcode):
        print('full : ', self._get_comm_full_data(trcode, rqname, 0))
        # print('real : ', self._get_comm_real_data('해외옵션시세', 10))

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

        self.opw30009_output.append(currency_code)
        self.opw30009_output.append(int(foreign_currency_deposit))
        self.opw30009_output.append(int(receivables))
        self.opw30009_output.append(int(aa))
        self.opw30009_output.append(int(bb))
        self.opw30009_output.append(int(cc))
        self.opw30009_output.append(int(dd))
        self.opw30009_output.append(int(ee))
        self.opw30009_output.append(int(ff))
        self.opw30009_output.append(int(gg))
        self.opw30009_output.append(int(hh))
        self.opw30009_output.append(int(ii))
        self.opw30009_output.append(int(jj))
        self.opw30009_output.append(int(kk))
        self.opw30009_output.append(int(ll))
        self.opw30009_output.append(int(mm))
        self.opw30009_output.append(int(nn))
        self.opw30009_output.append(int(oo))
        self.opw30009_output.append(int(pp))
        self.opw30009_output.append(int(qq))
        self.opw30009_output.append(int(rr))
        self.opw30009_output.append(int(ss))

        print('300009 output : ', self.opw30009_output)


    # 주문가능수량조회
    def _opw30011(self, rqname, trcode):
        print('_opw30011 : ', rqname, trcode)
        print(self._get_comm_full_data(trcode, rqname, 0))
        self.available_buy_count = self._get_comm_data(trcode, rqname, 0, "주문가능수량")
        print('available : {}'.format(self.available_buy_count))


    # 장운영정보조회
    def _opw50001(self, rqname, trcode):
        print('opw50001')
        current_time = self._get_comm_data(trcode, rqname, 0, "현재시간")

        data_cnt = self._get_repeat_cnt(trcode, rqname)
        for i in range(data_cnt):
            code = self._get_comm_data(trcode, rqname, i, "파생품목코드")

            if code.startswith('6E'):
                opr_time = self._get_comm_data(trcode, rqname, i, "장운영시간1")
                start_opr_time = opr_time[:4]
                end_opr_time = opr_time[4:]

                if end_opr_time < current_time < start_opr_time:
                    self.tradable = False
                    return self.tradable
                else:
                    return self.tradable

        return self.tradable

    def is_available_trading_time(self):
        self.set_input_value("품목구분", 'CUR')
        self.comm_rq_data("opw50001_req", "opw50001", '0', "5001")
        print('tradable : ', self.tradable)

    # 원화외화예수금잔액조회
    def _opw60003(self, rqname, trcode):
        print('opw60003')

    # 해외옵션인수도신청
    def _opw30019(self, rqname, trcode):
        print('opw30019')

if __name__ == "__main__":
    accno = '7006265572'

    # app = QApplication(sys.argv)
    # kiwoom = Kiwoom()
    # kiwoom.comm_connect()

    # kiwoom.reset_opw30009_output()
    # kiwoom.get_chart_data('minute', 30)
    # print(kiwoom.get_available_order_count(accno, '1'))
    # print(kiwoom._get_comm_real_data("해외선물시세", 10))

    # time.sleep(20)
    # print(kiwoom.is_available_trading_time())

