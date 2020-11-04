import pandas as pd
import numpy as np
import math
import os

from datetime import datetime




def volatility(df):
    """
    Daily Historical Volatility Index calculated using the logarithmic percentage change taken from spot price
    of the currency at every minute and converting it to the desired interval (modify the window param in case you
    want to use a different interval.).
        window:
            a) Daiy = 1440 (minutes in a day)
            b) Weekly = 10080 (minutes in a week)
            ...
        Formula:
            Stdev(Ln(P1/P0), Ln(P2/P1), ..., Ln(P1440/P1439)) * Sqrt(1440)
    Arguments:
    ----------
        df {[DataFrame]} -- dataframe containing the historic 1min closing price.
    Returns:
    --------
        {[float]}
            Volatility percentage of the currency at the closing price calculated after the window historic prices.
    """

    window = 1440

    prices = pd.DataFrame(df).rename(columns={0: 'Close'})
    prices['Close'] = prices['Close'].ffill()
    prices['LagClose'] = prices['Close'].shift(1).bfill()
    prices = prices[1:]
    volatility = ((np.log(prices['LagClose'] / prices['Close'])).std() * np.sqrt(window))
    return volatility


def time_indexer(df):
    """
    Converting timestamp column into datetime format and indexing

    Arguments:
    ----------
        df {[DataFrame]} -- dataframe containing the historic data.

    Returns:
    --------
        {[DataFrame]}
            Timestamp indexed as a datetime format.
    """
    df['Timestamp'] = df['Timestamp'].map(lambda t: datetime.strptime(str(t), '%Y-%m-%d %H:%M:%S'))
    return df.set_index('Timestamp')



def get_volatility(frequency, window=1441):
    """
    To avoid recalculating the volatility fot the whole dataframe, we detect the last calculated index position and
    apply the volatility function for this missing period. In case any is detected we will calculate the volatility for
    the whole dataframe.
    Arguments:
    ----------
        df {[DataFrame]} -- dataframe containing the historic 1min closing price.
        frequency {[str]} -- Timeframe we'd like to receive the data
        window {[int]} -- Over which period do we want to calculate the volatility
                        a) Daiy = 1440 (minutes in a day)
                        b) Weekly = 10080 (minutes in a week)
                        ...
    Returns:
    --------
        {[DataFrame]}[0]
            Dataframe containing all the data + the volatility at 1 min intervals.
            csv file containing all the data + the volatility at 1 min intervals.
        {[DataFrame]}[1]
            Dataframe containing the volatility grouped at a desired interval
    """

    # Checking if you have the required file (1min closing price data) to execute this script.
    valid_files = [file for file in os.listdir("./data.nosync/raw_data") if file.endswith(".csv")
                                                                        and file.split('_')[0] == '1min']
    if valid_files:
        print('Perfect! You have a file containing 1min closing price data.')
        print('Now, checking if the file has previous volatility...')
        data = pd.read_csv("./data.nosync/raw_data/1min_general.csv")

        existing_volatility = [x for x in data.columns if x == 'Volatility']

        # Continue from previous volatility calculation
        if existing_volatility:
            print('There is volatility. Checking if an update is needed...')
            # Finding missing values for volatility so we know the row we should use as a starting point
            data_nan = data[window:]
            try:
                index = data_nan[data_nan['Volatility'].isnull()].index.tolist()[0]
                print('First NaN value in volatility column is at position: ', index)
                print('Updating your volatility column...')

                # Creating dataframe for the missing volatility
                df = pd.DataFrame(data['Timestamp'][(index - window):])

                # Executing volatility function
                vol = (data['Close'][(index - window):]).rolling(window, min_periods=window).apply(volatility)
                df = pd.concat([df.reset_index(drop=True), vol.reset_index(drop=True)], axis=1) \
                                                                                .rename(columns={'Close': 'Volatility'})

                # Merging with original dataframe and calculating volatility column
                data_vol = data.merge(df, right_on='Timestamp', left_on='Timestamp', how='left')
                data_vol['Volatility'] = data_vol['Volatility_x'].fillna(0) + data_vol['Volatility_y'].fillna(0)

                # Indexing Timestamp to use the grouper function and obtain data at a desired timeframe
                data_vol = time_indexer(data_vol)

                data_vol.to_csv(f'./data.nosync/raw_data/1min_general.csv')

                print('Check your output folder!')

                return data_vol, data_vol['Volatility'].groupby(pd.Grouper(freq=frequency)).mean()


            except:
                print('Seems you are up to date! We cannot find a valid missing value for volatility.')
                data = time_indexer(data)

                return data, data['Volatility'].groupby(pd.Grouper(freq=frequency)).mean()


        # Calculate volatility from scratch
        else:
            print('Calculating volatility from scratch!')

            #Executing volatility function
            data['Volatility'] = data['Close'].rolling(window, min_periods=window).apply(volatility)

            #Indexing Timestamp to receive data at a desired timeframe
            data = time_indexer(data)

            data.to_csv(f'./data.nosync/raw_data/1min_general.csv')

            return data, data['Volatility'].groupby(pd.Grouper(freq=frequency)).mean()

    else:
        print('You need to input 1 minute closing price data to run this algorithm')
