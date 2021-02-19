import pandas as pd
import numpy as np
import sys

import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize']=20,10

from keras.models import Sequential
from keras.layers import LSTM,Dropout,Dense

from sklearn.preprocessing import MinMaxScaler

from datetime import date, datetime, timedelta
from dateutil import relativedelta

def predict(df):
    # Clean data set
    print("Cleaning data frame...", file=sys.stdout)
    df = clean_data(df)
    # Eliminate unecessary fields from working set
    df_bl = df[['invoice_date', 'cases_sold']]
    # Format invoice date field
    print("Formatting dates...", file=sys.stdout)
    df_bl = format_dates(df_bl)
    # Get monthly sales differences
    print("Getting monthly sales differences...", file=sys.stdout)
    df_diff = get_diff(df_bl)
    # Get supervised data
    print("Getting supervised data...", file=sys.stdout)
    df_sup = get_sup(df_diff)

    # Create training sets
    print("Creating training sets...", file=sys.stdout)
    df_model = df_sup.drop(['cases_sold', 'invoice_date'], axis=1)
    # Split train and test set
    train_set, test_set = df_model[0:-6].values, df_model[-6:].values

    # Apply Min Max Scaler
    print("Scaling data...", file=sys.stdout)
    scaler = MinMaxScaler(feature_range=(-1,1))
    scaler = scaler.fit(train_set)

    # Reshape training set
    train_set = train_set.reshape(train_set.shape[0], train_set.shape[1])
    train_set_scaled = scaler.transform(train_set)

    # Reshape test set
    test_set = test_set.reshape(test_set.shape[0], test_set.shape[1])
    test_set_scaled = scaler.transform(test_set)

    # Scale train and test sets
    x_train, y_train = train_set_scaled[:, 1:], train_set_scaled[:, 0:1]
    x_train = x_train.reshape(x_train.shape[0], 1, x_train.shape[1])

    x_test, y_test = test_set_scaled[:, 1:], test_set_scaled[:, 0:1]
    x_test = x_test.reshape(x_test.shape[0],1, x_test.shape[1])

    # Get y_pred from LSTM model
    print("Generating data from LSTM model...", file=sys.stdout)
    y_pred = lstm(x_train, y_train, x_test)

    # Reshape y_pred
    y_pred = y_pred.reshape(y_pred.shape[0], 1, y_pred.shape[1])

    # Rebuild test set for inverse transform
    print("Rebuilding set...", file=sys.stdout)
    pred_test_set = []
    for index in range(0, len(y_pred)):
        pred_test_set.append(np.concatenate([y_pred[index], x_test[index]], axis=1))

    # Reshape pred_test_set
    pred_test_set = np.array(pred_test_set)
    pred_test_set = pred_test_set.reshape(pred_test_set.shape[0], pred_test_set.shape[2])

    # Inverse transform
    pred_test_set_inverted = scaler.inverse_transform(pred_test_set)

    # Generate future predictions data frame
    print("Generating futures data frame...", file=sys.stdout)
    d = get_fut(df_diff)

    # Get future predictions results
    print("Retrieving future prediction results...", file=sys.stdout)
    fut_data = get_fut_pred(d, pred_test_set_inverted)
    result_list = fut_data['result_list']
    predictions = fut_data['predictions']

    # Get forecasts
    print("Retrieving forecasted data...", file=sys.stdout)
    x_y_data = get_forecast(result_list)
    X = x_y_data['X']
    y = x_y_data['y']

    # Get future LSTM data
    print("Retriving future LSTM data...", file=sys.stdout)
    lstm_fut_data = lstm_fut(X, y, 4, predictions)
    x_input = lstm_fut_data['x_input']
    model = lstm_fut_data['model']
    currentStep = lstm_fut_data['currentStep']

    # Get next 12 months of predicted sales data
    print("Generating data for 2021...", file=sys.stdout)
    next_12 = get_next_pred(x_input, 4, 1, model, currentStep)

    # Get full data set including historical and predicted values
    print("Retrieving data for 2021...", file=sys.stdout)
    df_futures = get_next_12(next_12, df_bl)

    # Return futures data set
    print("Returning data set!", file=sys.stdout)
    return df_futures

def clean_data(df):
    # Remove unnecessary fields
    df = df[['brand','invoice_date', 'cases_sold']]

    # Convert data types (this may be redundent)
    df["brand"] = df["brand"].astype(str)
    df = df.astype({"cases_sold": int})
    df["invoice_date"] = pd.to_datetime(df.invoice_date, format="%Y-%m-%d")

    # Remove weekends from data set
    df['day_of_week'] = df['invoice_date'].dt.day_name()
    df = df.loc[(df['day_of_week'] != 'Saturday') & (df['day_of_week'] != 'Sunday')]

    return df

def format_dates(df_bl):
    # Represent month in date filed as its first day
    invoice_date_val = df_bl['invoice_date'].dt.year.astype('str') + '-' + df_bl['invoice_date'].dt.month.astype('str') + '-01'
    df_bl['invoice_date'] = invoice_date_val

    invoice_date_conv = pd.to_datetime(df_bl['invoice_date'])
    df_bl['invoice_date'] = invoice_date_conv

    # Group by date and sum the sales
    df_bl = df_bl.groupby('invoice_date').cases_sold.sum().reset_index()

    return df_bl

def get_diff(df_bl):
    # Create a new dartaframe to model the difference
    df_diff = df_bl.copy()

    # Add previous sales to the next row
    df_diff['prev_sales'] = df_diff['cases_sold'].shift(1)

    # Dro the null values and calculate the difference
    df_diff = df_diff.dropna()
    df_diff['diff'] = df_diff['cases_sold'] - df_diff['prev_sales']

    return df_diff

def get_sup(df_diff):
    # Create dataframe for transformation from time series to supervised
    df_sup = df_diff.drop(['prev_sales'], axis=1)

    # Adding lags
    for inc in range(1,13):
        field_name = 'lag_' + str(inc)
        df_sup[field_name] = df_sup['diff'].shift(inc)

    # Drop null values
    df_sup = df_sup.dropna().reset_index(drop=True)

    return df_sup

def lstm(x_train, y_train, x_test):
    # Fit LSTM model
    model = Sequential()
    model.add(LSTM(4, batch_input_shape=(1, x_train.shape[1], x_train.shape[2]), stateful=True))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_train, y_train, epochs=100, batch_size=1, verbose=1, shuffle=False)

    # Predictions
    y_pred = model.predict(x_test, batch_size=1)

    return y_pred

def get_fut(df_diff):
    # Create dataframe for transformation from time series to supervised
    d = df_diff.drop(['prev_sales'], axis=1)

    # Adding lags
    for inc in range(1,13):
        field_name = 'lag_' + str(inc)
        d[field_name] = d['diff'].shift(inc)

    # Drop null values
    d = d.dropna().reset_index(drop=True)

    return d

def get_fut_pred(d, pred_test_set_inverted):
    result_list = []
    sales_dates = list(d[-9:].invoice_date)
    act_sales = list(d[-9:].cases_sold)
    for index in range(0,len(pred_test_set_inverted)):
        result_dict = {}
        result_dict['pred_value'] = int(pred_test_set_inverted[index][0] + act_sales[index]) #change to 0 ffrom act_sales[index]
        result_dict['invoice_date'] = sales_dates[index] #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>REVIEW
        result_list.append(result_dict)

    df_result = pd.DataFrame(result_list)
    predictions = list(df_result['pred_value'])

    fut_data = {'result_list': result_list, 'predictions': predictions}
    return fut_data

def get_forecast(result_list):
    forecasts = []
    result_list
    for i in range(len(result_list)):
        forecasts.append(result_list[i]['pred_value'])

    # choose a number of time steps
    n_steps = 4

    X, y = [], []
    for i in range(len(forecasts)):
        # find the end of this pattern
        end_ix = i + n_steps

        # check if we are beyond the sequence
        if end_ix > len(forecasts)-1:
            break

        # gather input and output parts of the pattern
        seq_x, seq_y = forecasts[i:end_ix], forecasts[end_ix]
        X.append(seq_x)
        y.append(seq_y)

    X = np.asarray(X)
    y = np.asarray(y)

    x_y_data = {'X': X, 'y': y}
    return x_y_data

def lstm_fut(X, y, n_steps, predictions):
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))

    # define model
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(n_steps, n_features)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    # fit model
    model.fit(X, y, epochs=500, verbose=0)

    # demonstrate prediction
    x_input = np.asarray(predictions[-4:])
    x_input = x_input.reshape((1, n_steps, n_features))
    yhat = model.predict(x_input, verbose=0)

    currentStep = yhat[:, -1:]

    lstm_fut_data = {'x_input': x_input, 'model': model, 'currentStep': currentStep}
    return lstm_fut_data

def get_next_pred(x_input, n_steps, n_features, model, currentStep):
    next_12 = []

    for i in range(12):
        if i == 0:
            x_input = x_input.reshape((1, n_steps, n_features))
            yhat = model.predict(x_input, batch_size=1, verbose=0)
            next_12.append(yhat[0][0])
        else:
            x0_input = np.append(x_input, [currentStep[i-1]])
            x0_input = x0_input.reshape((1, n_steps+1, n_features))
            x_input = x0_input[:,1:]
            yhat = model.predict(x_input, batch_size=1)
            currentStep = np.append(currentStep, yhat[:,-1:])
            next_12.append(yhat[0][0])

    return next_12

def get_next_12(next_12, df_bl):
    next_12_months = []
    next_12_months.append(date(2021, 1, 1))

    start_date = date(2021, 1, 1)
    end_date = date(2021, 12, 1)
    delta = relativedelta.relativedelta(months=1)
    current = start_date
    while current < end_date:
        current += delta
        next_12_months.append(current)

    pred_data = []
    for i in range(0, len(next_12_months)):
        pred_month = []
        pred_month.append(next_12_months[i])
        pred_month.append(next_12[i])
        pred_data.append(pred_month)

    df_next = pd.DataFrame(pred_data, columns = ['invoice_date', 'pred_value'])
    df_next = df_next.astype({"pred_value": int})
    df_next["invoice_date"] = pd.to_datetime(df_next.invoice_date, format="%Y-%m-%d")

    # Merge with actual sales data frame
    df_futures = pd.concat([df_bl, df_next], ignore_index=True, sort=False)

    return df_futures