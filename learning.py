import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
from pyupbit import WebSocketManager as WM
import pyupbit


data = pd.read_csv('./dataset.csv')
feature_list = list(data)[:-3]

data_input = data[feature_list].to_numpy()
data_target_50 = data['d50'].to_numpy()
data_target_500 = data['d500'].to_numpy()
data_target_1200 = data['d1200'].to_numpy()
data_target = data[['d50', 'd500', 'd1200']].to_numpy()

train_input, test_input, train_target, test_target = train_test_split(data_input, data_target_500, train_size=0.99)

mlr = LinearRegression()
mlr.fit(train_input, train_target)
print(mlr.score(test_input, test_target))

joblib.dump(mlr, './ML-model.pkl')
print("pkl파일에 학습 모델 저장 완료, 검증 시작")


count_for_500 = 500
index_for_500 = 0
wm = WM("orderbook", ['KRW-BTC'])
data_list = []
corc = 0
while True:
    data = wm.get()
    # 양수면 파는사람이 많다
    orderli = []
    for unit in data['orderbook_units']:
        orderli.append(round(unit['ask_size']-unit['bid_size'], 8))
    current_price = pyupbit.get_current_price('KRW-BTC')
    orderli.append(current_price)
    data_list.append(orderli)
    if count_for_500 == 0:
        if (mlr.predict([data_list[index_for_500][:15]])[0])*(current_price - data_list[index_for_500][15]) >= 0:
            corc += 1
            print(corc/(index_for_500 + 500))
        index_for_500 += 1
    else:
        count_for_500 -= 1

wm.terminate()
