# from collections import Counter
# import numpy as np
# import pandas as pd
# import tensorflow as tf
# from SlippStockCrawler import SlippStockCrawler
#
#
# input_data_column_cnt = 8  # 입력데이터의 컬럼 개수(Variable 개수)
# output_data_column_cnt = 1  # 결과데이터의 컬럼 개수
# seq_length = 5  # 1개 시퀀스의 길이(시계열데이터 입력 개수)
#
#
# def model_inputs():
#     """
#     Create the model inputs
#     """
#     inputs_ = tf.placeholder(tf.float32, [None, seq_length, input_data_column_cnt], name='inputs')
#     labels_ = tf.placeholder(tf.int32, [None, None], name='labels')
#     keep_prob_ = tf.placeholder(tf.float32, name='keep_prob')
#
#     return inputs_, labels_, keep_prob_
#
#
# def remove_none_value_row(stock_dict):
#
#     for code in stock_dict:
#         stock_dict[code] = stock_dict[code][
#             stock_dict[code]['MA60'] == stock_dict[code]['MA60']
#         ]  # 이동평균값이 존재하는 데이터만 취급
#
#     return stock_dict
#
#
# def remove_under_60_row_table(stock_dict):
#
#     for code in stock_dict:
#         if len(stock_dict[code]) < seq_length:
#             del stock_dict[code]
#
#     return stock_dict
#
#
# def preprocess_data(stock_dict):
#     """
#     데이터 전처리
#     :param stock_dict:
#     :return:
#     """
#     stock_dict = remove_none_value_row(stock_dict)
#     stock_dict = remove_under_60_row_table(stock_dict)
#     return stock_dict
#
#
# def list_data_split(data, split_frac):
#     """
#     학습용, 검증용, 평가용 ( ex. split_frac=0.7 -> 7 : 1.5 : 1.5 )
#     :param data: raw data
#     :param split_frac: 학습용 / 확인용 데이터 구분 비율
#     :return:
#     """
#     # make splits
#     split_idx = int(len(data) * split_frac)
#     train, valid = data[:split_idx], data[split_idx:]
#
#     test_idx = int(len(valid) * 0.5)
#     valid, test = valid[:test_idx], valid[test_idx:]
#
#     return train, valid, test
#
#
# def get_batches(x, y, batch_size=100):
#     """
#     Batch Generator for Training
#     :param x: Input array of x data
#     :param y: Input array of y data
#     :param batch_size: Input int, size of batch
#     :return: generator that returns a tuple of our x batch and y batch
#     """
#     n_batches = len(x) // batch_size
#     x, y = x[:n_batches * batch_size], y[:n_batches * batch_size]
#     for ii in range(0, len(x), batch_size):
#         yield x[ii:ii + batch_size], y[ii:ii + batch_size]
#
#
# def build_lstm_layers(lstm_sizes, inputs_, keep_prob_, batch_size):
#     """
#     Create the LSTM layers
#     """
#     forget_bias = 1.0  # 망각편향(기본값 1.0)
#
#     lstms = [tf.contrib.rnn.LSTMCell(size, forget_bias=forget_bias, activation=tf.nn.softsign) for size in lstm_sizes]
#     # Add dropout to the cell
#     drops = [tf.contrib.rnn.DropoutWrapper(lstm, output_keep_prob=keep_prob_) for lstm in lstms]
#     # Stack up multiple LSTM layers, for deep learning
#     cell = tf.contrib.rnn.MultiRNNCell(drops)
#     # Getting an initial state of all zeros
#     initial_state = cell.zero_state(batch_size, tf.float32)
#
#     lstm_outputs, final_state = tf.nn.dynamic_rnn(cell, inputs_, dtype=tf.float32, initial_state=initial_state)
#
#     return initial_state, lstm_outputs, cell, final_state
#
#
# def build_cost_fn_and_opt(lstm_outputs, labels_, learning_rate):
#     """
#     Create the Loss function and Optimizer
#     """
#     predictions = tf.contrib.layers.fully_connected(lstm_outputs[:, -1], output_data_column_cnt, activation_fn=tf.sparse_softmax)
#     loss = tf.losses.mean_squared_error(labels_, predictions)
#     optimzer = tf.train.AdadeltaOptimizer(learning_rate).minimize(loss)
#
#     return predictions, loss, optimzer
#
#
# def build_accuracy(predictions, labels_):
#     """
#     Create accuracy
#     """
#     correct_pred = tf.equal(tf.cast(tf.round(predictions), tf.int32), labels_)
#     accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
#
#     return accuracy
#
#
# def build_and_train_network(lstm_sizes, vocab_size, embed_size, epochs, batch_size,
#                             learning_rate, keep_prob, train_x, valid_x, train_y, val_y):
#     inputs_, labels_, keep_prob_ = model_inputs()
#     initial_state, lstm_outputs, lstm_cell, final_state = build_lstm_layers(lstm_sizes, embed, keep_prob_, batch_size)
#     predictions, loss, optimizer = build_cost_fn_and_opt(lstm_outputs, labels_, learning_rate)
#     accuracy = build_accuracy(predictions, labels_)
#
#     saver = tf.train.Saver()
#
#     with tf.Session() as sess:
#
#         sess.run(tf.global_variables_initializer())
#         n_batches = len(train_x) // batch_size
#         for e in range(epochs):
#             state = sess.run(initial_state)
#
#             train_acc = []
#             for ii, (x, y) in enumerate(utl.get_batches(train_x, train_y, batch_size), 1):
#                 feed = {inputs_: x,
#                         labels_: y[:, None],
#                         keep_prob_: keep_prob,
#                         initial_state: state}
#                 loss_, state, _, batch_acc = sess.run([loss, final_state, optimizer, accuracy], feed_dict=feed)
#                 train_acc.append(batch_acc)
#
#                 if (ii + 1) % n_batches == 0:
#
#                     val_acc = []
#                     val_state = sess.run(lstm_cell.zero_state(batch_size, tf.float32))
#                     for xx, yy in utl.get_batches(valid_x, val_y, batch_size):
#                         feed = {inputs_: xx,
#                                 labels_: yy[:, None],
#                                 keep_prob_: 1,
#                                 initial_state: val_state}
#                         val_batch_acc, val_state = sess.run([accuracy, final_state], feed_dict=feed)
#                         val_acc.append(val_batch_acc)
#
#                     print("Epoch: {}/{}...".format(e + 1, epochs),
#                           "Batch: {}/{}...".format(ii + 1, n_batches),
#                           "Train Loss: {:.3f}...".format(loss_),
#                           "Train Accruacy: {:.3f}...".format(np.mean(train_acc)),
#                           "Val Accuracy: {:.3f}".format(np.mean(val_acc)))
#
#         saver.save(sess, "checkpoints/sentiment.ckpt")
#
#
# def test_network(model_dir, batch_size, test_x, test_y):
#     inputs_, labels_, keep_prob_ = model_inputs()
#     embed = build_embedding_layer(inputs_, vocab_size, embed_size)
#     initial_state, lstm_outputs, lstm_cell, final_state = build_lstm_layers(lstm_sizes, inputs_, keep_prob_, batch_size)
#     predictions, loss, optimizer = build_cost_fn_and_opt(lstm_outputs, labels_, learning_rate)
#     accuracy = build_accuracy(predictions, labels_)
#
#     saver = tf.train.Saver()
#
#     test_acc = []
#     with tf.Session() as sess:
#         saver.restore(sess, tf.train.latest_checkpoint(model_dir))
#         test_state = sess.run(lstm_cell.zero_state(batch_size, tf.float32))
#         for ii, (x, y) in enumerate(utl.get_batches(test_x, test_y, batch_size), 1):
#             feed = {inputs_: x,
#                     labels_: y[:, None],
#                     keep_prob_: 1,
#                     initial_state: test_state}
#             batch_acc, test_state = sess.run([accuracy, final_state], feed_dict=feed)
#             test_acc.append(batch_acc)
#         print("Test Accuracy: {:.3f}".format(np.mean(test_acc)))
#
#
#
#
#
# '''
# 1. 데이터 준비
# 2. 네트워크 입력값 정의
# 3. 네트워크 구성
#   - LSTM
#   - 정규화(dropout) : 특정 노드 의존성을 줄여 오버피팅 억
#   - multi rnn : layer 연결
#   - dynamic rnn : 결과 및 상태값 반환
# 4. 손실함수 정의
# 5. optimizer 정의
# 6. 유효 결과 및 정확도 정의
# 7. 그래프 생성
# 8. 모델 하이퍼 파라미터 정의
# 9. 학습
#
# 활성화함수 :
#
# '''
#
# # 데이터 준비
# # sqlite에서 종목별 주가 데이터 조회.
# stock_dict = SlippStockCrawler().select_stock_price_model()
# stock_dict = preprocess_data(stock_dict)
#
# stock_codes = [*stock_dict]
#
# train_codes, valid_codes, test_codes = list_data_split(stock_codes, split_frac=0.70)
#
#
# # 입력값 및 하이퍼파라미터 정의
# lstm_sizes = [128, 64]
# epochs = 100
# batch_size = 256
# learning_rate = 0.1
# keep_prob = 0.7
#
#
# with tf.Graph().as_default():
#
#     for code in
#     train_x, valid_x, test_x
#     print("Data Set Size")
#     print("Train set: \t\t{}".format(train_x.shape),
#           "\nValidation set: \t{}".format(valid_x.shape),
#           "\nTest set: \t\t{}".format(test_x.shape))
#
#     build_and_train_network(lstm_sizes, epochs, batch_size, learning_rate, keep_prob, train_x, valid_x)
#
#
# with tf.Graph().as_default():
#     test_network('checkpoints', batch_size, test_x, test_y)
