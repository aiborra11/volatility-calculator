
# Volatility Index Calculator

_The scope of this project is to calculate and obtain the historic volatility for any currency, commodity, security, etc._

Risk management is one of the key points at every trading strategy and volatility plays a key role in here. 
We can use it to expect specific fluctuations in the returns of the underlying asset that might happen on the determined timeframe. 


The way I calculate it is throughout logarithmic percentage change of the currency spot price at every minute during X periods of time. 

![volatility_formula](https://github.com/aiborra11/volatility-calculator/blob/main/output/images/volatility_formula.png)

It makes a lot of sense to me using the natural logarithm to decrease the growth as time goes by. Volatility can't (or shouldn't) grow at a high rate during long periods of time.


## Script Execution
You will need to input a dataframe containing the closing 1 min spot prices  of the asset you are analysing.
**Make sure you locate the correct csv file into your data folder and name it as "1min_XXXXX".**

Then, execute the script and you will generate a new csv file conatining a new column for the volatility index. 
Also, you can group the volatility in your desired timeframe (Daily, Hourly, 5min, etc.).

It will automatically detect either you already have volatility and then, avoid calculating it from scratch (time consuming),
either you are already up to date. 

Finally, you will be able to analyse the volatility and use it for SL/TP calculations, backtest and realise if you are cutting wins/loses, etc.

Here is a sample of the volatility XBT experienced the previous month at the moment of publishing this repo (27/10/2020):

![volatility_index](https://github.com/aiborra11/volatility-calculator/blob/main/output/images/volatility_index.png)

In this case I calculated the Historic Volatility using a daily basis, but feel free to modify the window param to calculate 
at a weekly, Daily, Monthly, etc., level. 
        
        window:
            a) Daiy = 1440 (minutes in a day)
            b) Weekly = 10080 (minutes in a week)
            ...

### Bonus
_In case you need the raw data to implement this calculations, I developed a crypto-scraper in this other repository that will
help you to create and populate your database with any available cryptocurrency in Bitmex. You will also find some other features 
I considered interesting to develop a better analysis_

https://github.com/aiborra11/crypto-scraper

Soon, I will include the volatility-calculator into the crypto-scraper.





