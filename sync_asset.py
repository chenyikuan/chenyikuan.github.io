import numpy as np
import sys
import pandas as pd

if sys.platform.startswith('win'):
    fn = 'D:/ws/qt_ws/worker002/daily_amount/nav_history_log.csv'
    income_df = pd.read_csv('D:/ws/qt_ws/income.csv')
else:
    fn = '/home/yikuan/ws/qt_ws/worker002/daily_amount/nav_history_log.csv'
    income_df = pd.read_csv('/home/yikuan/ws/qt_ws/income.csv')
history_df = pd.read_csv(fn, header=0)
history_df = history_df.drop_duplicates(subset=['date'], keep='last').reset_index(drop=True)
net_df = history_df.copy()

hi = 0
ii = 0
bi = income_df.iloc[ii,:]
next_ajust = False
while hi < len(history_df):
    if hi == 0:
        net_df.loc[hi, 'nav'] = 0.0
        hi += 1
        continue
    ai = history_df.iloc[hi,:]
    if next_ajust:
        print(bi['date'], bi['timestamp'][11:16] < '15:00')
        if bi['timestamp'][11:16] < '15:00':
            # net_df.loc[hi, 'nav'] = (ai['nav'] - history_df.loc[hi-1, 'nav']) / history_df.loc[hi-1, 'nav']
            net_df.loc[hi, 'nav'] = (ai['nav'] - history_df.loc[hi-1, 'nav']) / (history_df.loc[hi-1, 'nav'] - bi['income'])
            print(ai['nav'], history_df.loc[hi-1, 'nav'])
            print(net_df.loc[hi, 'nav'])
        else:
            # net_df.loc[hi, 'nav'] = (ai['nav'] - history_df.loc[hi-1, 'nav']) / (history_df.loc[hi-1, 'nav'] - bi['income'])
            net_df.loc[hi, 'nav'] = (ai['nav'] - history_df.loc[hi-1, 'nav']) / history_df.loc[hi-1, 'nav']
        ii += 1
        if ii < len(income_df):
            bi = income_df.loc[ii,:]
        next_ajust = False
    else:
        net_df.loc[hi, 'nav'] = (ai['nav'] - history_df.loc[hi-1, 'nav']) / history_df.loc[hi-1, 'nav']

    if ai['date'][:10] == bi['date'][:10]:
        next_ajust = True
        # TODO 这里如果入仓，手续费减除
        net_df.loc[hi, 'nav'] = (ai['nav'] - history_df.loc[hi-1, 'nav'] - bi['income']) / history_df.loc[hi-1, 'nav']
    hi += 1

net_df['nav'] += 1
net_df['nav'] = net_df['nav'].cumprod()
print(net_df)
net_df.to_csv('data/nav_history_net.csv', index=False)
print('net asset updated.')