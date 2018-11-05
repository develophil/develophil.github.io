import sqlite3
from collections import namedtuple

import tensorflow as tf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pickle
import gzip
from pandas import DataFrame

from SlippStockCrawler import SlippStockCrawler

# if __name__ == "__main__":
#     crawler = SlippStockCrawler()
#     end = datetime.today()
#     start = end - timedelta(days=7)
#     stock_data = crawler.get_kospi_stock_price(start, end)

# 랜덤에 의해 똑같은 결과를 재현하도록 시드 설정
# 하이퍼파라미터를 튜닝하기 위한 용도(흔들리면 무엇때문에 좋아졌는지 알기 어려움)
tf.set_random_seed(777)


# Standardization
def data_standardization(x):
    x_np = np.asarray(x)
    return (x_np - x_np.mean()) / x_np.std()


# 너무 작거나 너무 큰 값이 학습을 방해하는 것을 방지하고자 정규화한다
# x가 양수라는 가정하에 최소값과 최대값을 이용하여 0~1사이의 값으로 변환
# Min-Max scaling
def min_max_scaling(x):
    x_np = np.asarray(x)
    return (x_np - x_np.min()) / (x_np.max() - x_np.min() + 1e-7)  # 1e-7은 0으로 나누는 오류 예방차원


# 정규화된 값을 원래의 값으로 되돌린다
# 정규화하기 이전의 org_x값과 되돌리고 싶은 x를 입력하면 역정규화된 값을 리턴한다
def reverse_min_max_scaling(org_x, x):
    org_x_np = np.asarray(org_x)
    x_np = np.asarray(x)
    return (x_np * (org_x_np.max() - org_x_np.min() + 1e-7)) + org_x_np.min()


def get_stock_dictionary():
    # 데이터를 로딩한다.
    stock_file_name = 'kospi_stock_price.pickle'  # 아마존 주가데이터 파일
    with gzip.open(stock_file_name, 'rb') as f:
        return pickle.load(f)


# 모델(LSTM 네트워크) 생성
def lstm_cell():
    # LSTM셀을 생성
    # num_units: 각 Cell 출력 크기
    # forget_bias:  to the biases of the forget gate
    #              (default: 1)  in order to reduce the scale of forgetting in the beginning of the training.
    # state_is_tuple: True ==> accepted and returned states are 2-tuples of the c_state and m_state.
    # state_is_tuple: False ==> they are concatenated along the column axis.
    cell = tf.contrib.rnn.LSTMCell(num_units=rnn_cell_hidden_dim,
                                   forget_bias=forget_bias, state_is_tuple=True, activation=tf.nn.softsign)
    if keep_prob < 1.0:
        cell = tf.contrib.rnn.DropoutWrapper(cell, output_keep_prob=keep_prob)
    return cell


Stock = namedtuple("Stock", ["gain_rate", "code", "price"])

gain_rate_top_10 = [Stock(0, "0000", 0)]


def update_buy_list():
    with open("top10_buy_list.txt", "wt") as f:
        for stock in gain_rate_top_10:
            line = "buy;{};market;10;0;prebuy;{};{}\n".format(stock.code, stock.gain_rate, stock.price)
            f.write(line)


def append_gain_rate_top_10(gain_rate, code, price):

    if gain_rate > gain_rate_top_10[-1].gain_rate:
        if len(gain_rate_top_10) is 10:
            print("del stock : ", gain_rate_top_10[-1])
            del gain_rate_top_10[-1]
        print("append stock : ", gain_rate)
        gain_rate_top_10.append(Stock(gain_rate, code, price))
        gain_rate_top_10.sort(key=lambda s:s.gain_rate, reverse=True)


# 하이퍼파라미터
input_data_column_cnt = 9  # 입력데이터의 컬럼 개수(Variable 개수)
output_data_column_cnt = 1  # 결과데이터의 컬럼 개수

seq_length = 5  # 1개 시퀀스의 길이(시계열데이터 입력 개수)
rnn_cell_hidden_dim = 20  # 각 셀의 (hidden)출력 크기
forget_bias = 1.0  # 망각편향(기본값 1.0)
num_stacked_layers = 1  # stacked LSTM layers 개수
keep_prob = 1.0  # dropout할 때 keep할 비율

epoch_num = 100  # 에폭 횟수(학습용전체데이터를 몇 회 반복해서 학습할 것인가 입력)
learning_rate = 0.01  # 학습률

# 데이터를 로딩한다.
# raw_dataframe = get_raw_dataframe()
# stock_dict = get_stock_dictionary()

train_error_summary = []  # 학습용 데이터의 오류를 중간 중간 기록한다
test_error_summary = []  # 테스트용 데이터의 오류를 중간 중간 기록한다
test_predict = ''  # 테스트용데이터로 예측한 결과

sess = tf.Session()

# 텐서플로우 플레이스홀더 생성
# 입력 X, 출력 Y를 생성한다
X = tf.placeholder(tf.float32, [None, seq_length, input_data_column_cnt])
print("X: ", X)
Y = tf.placeholder(tf.float32, [None, 1])
print("Y: ", Y)

# 검증용 측정지표를 산출하기 위한 targets, predictions를 생성한다
targets = tf.placeholder(tf.float32, [None, 1])
print("targets: ", targets)

predictions = tf.placeholder(tf.float32, [None, 1])
print("predictions: ", predictions)

# num_stacked_layers개의 층으로 쌓인 Stacked RNNs 생성
stackedRNNs = [lstm_cell() for _ in range(num_stacked_layers)]
multi_cells = tf.contrib.rnn.MultiRNNCell(stackedRNNs, state_is_tuple=True) if num_stacked_layers > 1 else lstm_cell()

# RNN Cell(여기서는 LSTM셀임)들을 연결
hypothesis, _states = tf.nn.dynamic_rnn(multi_cells, X, dtype=tf.float32)
print("hypothesis: ", hypothesis)

# [:, -1]를 잘 살펴보자. LSTM RNN의 마지막 (hidden)출력만을 사용했다.
# 과거 여러 거래일의 주가를 이용해서 다음날의 주가 1개를 예측하기때문에 MANY-TO-ONE형태이다
hypothesis = tf.contrib.layers.fully_connected(hypothesis[:, -1], output_data_column_cnt, activation_fn=tf.identity)

# 손실함수로 평균제곱오차를 사용한다
loss = tf.reduce_sum(tf.square(hypothesis - Y))
# 최적화함수로 AdamOptimizer를 사용한다
optimizer = tf.train.AdamOptimizer(learning_rate)
# optimizer = tf.train.RMSPropOptimizer(learning_rate) # LSTM과 궁합 별로임

train = optimizer.minimize(loss)

# RMSE(Root Mean Square Error)
# 제곱오차의 평균을 구하고 다시 제곱근을 구하면 평균 오차가 나온다
# rmse = tf.sqrt(tf.reduce_mean(tf.square(targets-predictions))) # 아래 코드와 같다
rmse = tf.sqrt(tf.reduce_mean(tf.squared_difference(targets, predictions)))

chk = tf.train.latest_checkpoint('checkpoints')
saver = tf.train.Saver()
saver = tf.train.import_meta_graph('./checkpoints/sentiment.ckpt.meta')
saver.restore(sess, chk)
# tf.reset_default_graph()

# current_stock_prices = {
#     'date': [1,2,3,4,5],
#     'open': [37400,36500,37200,37700,37450],
#     'high': [36100,35100,35700,36650,35000],
#     'low': [36650,36250,36200,36700,37100],
#     'close': [36450,35800,36650,37450,35350],
#     'adj close': [36450,35800,36650,37450,35350],
#     'MA5': [38430,37560,36950,36670,36340],
#     'MA20': [41380,40960,40622,40342,39950],
#     'MA60': [43389,43306,43225,43122,43000],
#     'volume': [210220,232572,116477,111172,266428]}
#
# df = DataFrame(current_stock_prices, columns=['open', 'high', 'low', 'close', 'adj close', 'MA5', 'MA20', 'MA60', 'volume'],
#                index=current_stock_prices['date'])

crawler = SlippStockCrawler()
end = datetime.today()
start = end - timedelta(days=seq_length)
stock_data = crawler.get_kospi_stock_price(start, end, seq_length)

for code in stock_data:
    df = stock_data[code]
    df = df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'MA5', 'MA20', 'MA60', 'Volume']]

    stock_info = df.values.astype(np.float)  # 금액&거래량 문자열을 부동소수점형으로 변환한다
    price = stock_info[:, 0:input_data_column_cnt - 1]
    volume = stock_info[:, -1:]

    norm_price = min_max_scaling(price)  # 가격형태 데이터 정규화 처리
    norm_volume = min_max_scaling(volume)  # 거래량형태 데이터 정규화 처리

    x = np.concatenate((norm_price, norm_volume), axis=1)  # axis=1, 세로로 합친다

    # sequence length만큼의 가장 최근 데이터를 슬라이싱한다
    recent_data = np.array([x[len(x) - seq_length:]])
    print("recent_data.shape:", recent_data.shape)
    print("recent_data:", recent_data)

    # 내일 종가를 예측해본다
    test_predict = sess.run(hypothesis, feed_dict={X: recent_data})[0][0]

    print("test_predict", test_predict)
    test_predict = reverse_min_max_scaling(price, test_predict)  # 금액데이터 역정규화한다
    print("Tomorrow's stock price", test_predict.round(2))  # 예측한 주가를 출력한다

    real_close_price = df['Adj Close'][-1]
    last_close_price = df['Adj Close'][-2]
    print("last close : ", last_close_price)
    print("real close : ", real_close_price)
    gain_rate = (test_predict / last_close_price * 100).round(2)
    print("gain rate : ", gain_rate)

    append_gain_rate_top_10(gain_rate, code, test_predict.round(2))

print("append_gain_rate_top_10 : ", gain_rate_top_10)
update_buy_list()


