import pyupbit
from pyupbit import WebSocketManager as WM
# import pymysql
# from datetime import datetime
import pandas as pd
# import time
import csv


def merge_csv():
    reader = csv.reader(open("./temp_data.csv"))
    f = open("./dataset.csv", 'a', newline='')
    wr = csv.writer(f)
    for row in reader:
        wr.writerow(row)
    f.close()
    print("merge 완료")
    return


def real_time_orderbook():
    # tickers = pyupbit.get_tickers(fiat="KRW")
    wm = WM("orderbook", ['KRW-BTC'])
    # ask-매도 bid-매수

    data_list = []
    orderli = []
    count_for_50 = 50
    index_for_50 = 0
    count_for_500 = 500
    index_for_500 = 0
    count_for_1200 = 1200
    index_for_1200 = 0
    while True:
        data = wm.get()
        # 양수면 파는사람이 많다
        orderli = []
        for unit in data['orderbook_units']:
            orderli.append(round(unit['ask_size']-unit['bid_size'], 8))
        current_price = pyupbit.get_current_price('KRW-BTC')
        orderli.append(current_price)
        data_list.append(orderli)
        if count_for_50 == 0:
            data_list[index_for_50].append(current_price
                                           - data_list[index_for_50][15])
            index_for_50 += 1
        else:
            count_for_50 -= 1

        if count_for_500 == 0:
            data_list[index_for_500].append(current_price
                                            - data_list[index_for_500][15])
            index_for_500 += 1
        else:
            count_for_500 -= 1

        if count_for_1200 == 0:
            data_list[index_for_1200].append(current_price -
                                             data_list[index_for_1200][15])
            # print(data_list[index_for_1200][15:])
            index_for_1200 += 1
        else:
            count_for_1200 -= 1

        if index_for_1200 == 1000:
            df = pd.DataFrame(data_list[:1000]).drop([15], axis=1)
            del data_list[:1000]
            index_for_50 -= 1000
            index_for_500 -= 1000
            index_for_1200 -= 1000
            df.to_csv('./temp_data.csv', header=False, index=False)
            merge_csv()
    wm.terminate()


real_time_orderbook()

