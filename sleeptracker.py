import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import re
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

print(pd.__version__)
print(datetime.strftime(datetime.now(),'%#m/%#d/%y %#I:%M %p'))
                        
pattern = re.compile('((?P<hr>\d+) hrs*\s*)*((?P<min>\d+) mins*)*')

def parse_minutes(durationstr):
    x = re.match(pattern,durationstr)
    hrs = int(x.group('hr') or 0) or 0
    mins = int(x.group('min') or 0) or 0
    return timedelta(hours=hrs,minutes=mins)
      
def test_parse_minutes():
    print(parse_minutes('1 hr 30 mins'))
    print(parse_minutes('45 mins'))
    print(parse_minutes('1 hr'))
    print(parse_minutes(''))




test_parse_minutes()

sleep = pd.read_csv("C:/Users/Daniel/Pictures/Loah/babytracker/Loah Swanson_sleep.csv",na_filter=False)



sleep['datetime'] = [datetime.strptime(x,'%m/%d/%y %I:%M %p') for x in sleep['Time']]
sleep['durationminutes'] = [parse_minutes(x) for x in sleep['Duration']]
sleep['yyyymmdd'] = [datetime.strftime(x,'%Y%m%d') for x in sleep['datetime']]
sleep['datetime_prev'] = sleep['datetime'].shift(1)
sleep['durationminutes_prev'] = sleep['durationminutes'].shift(1)
sleep['wake_prev'] = sleep['datetime_prev'] + sleep['durationminutes_prev']
sleep['waketime'] =  sleep['datetime'] - sleep['wake_prev']
sleep['waketimehrs'] =  [x.seconds/3600 for x in sleep['waketime']]
latest_date = sleep['yyyymmdd'].iloc[-1]


sleep['waketimehrs2'] = [x if x < 12 else np.NaN for x in sleep['waketimehrs']]

sleep['age'] = sleep['datetime'] - datetime(2019,9,26)
sleep['age_months'] = [x / np.timedelta64(1, 'M') for x in sleep['age']]

plt.plot(sleep['age_months'],sleep['waketimehrs2'])
plt.title("Waketime " + str(latest_date))
plt.xlabel('Age (Months)')
plt.ylabel('Waketime')
plt.show()

sleep = sleep.dropna(how='any')
X = sleep['age_months'].values.reshape(-1,1)
y = sleep['waketimehrs2'].values.reshape(-1,1)

regressor = LinearRegression()  
regressor.fit(X,y)
y_pred = regressor.predict(X)
plt.plot(sleep['age_months'],y_pred)
print(regressor.intercept_)
print(regressor.coef_) 

#plt.savefig('C:/Users/Daniel/Desktop/' + str(latest_cases) + '_New_Cases.png')
#plt.close()