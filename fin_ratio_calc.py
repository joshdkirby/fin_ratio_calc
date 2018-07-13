import pandas as pd
import requests
from bs4 import BeautifulSoup
import sys

# Input stock ticker as argument
ticker = sys.argv[1]

# Read in nasdaq page for stock using BeautifulSoup
r = requests.get('https://www.nasdaq.com/symbol/'+ticker+'')

soup = BeautifulSoup(r.text, 'lxml')

# Check that ticker entered is a valid stock ticker by checking for an error on the Nasdaq site
# Will display an error message and exit the script if ticker is invalid
ticker_check = soup.find('div', class_='notTradingIPO')
if ticker_check == None:
    pass
else:
    print('The ticker you have entered is invalid')
    sys.exit()

# Get the latest price from Nasdaq
price = soup.find('div', id='qwidget_lastsale').text[1:]

# Read in balance sheet and income statement from Yahoo Finance and format dataframes for analysis
bs_page = pd.read_html('https://finance.yahoo.com/quote/'+ticker+'/balance-sheet/')
is_page = pd.read_html('https://finance.yahoo.com/quote/'+ticker+'/financials')

bal_sheet = pd.DataFrame(bs_page[0])

bal_sheet.set_index(0, inplace=True)

inc_state = pd.DataFrame(is_page[0])

inc_state.set_index(0, inplace=True)

# Calculate ratios using the income statement and balance sheet imported above
debt_to_equity = int(bal_sheet.loc['Total Liabilities', 1]) / int(bal_sheet.loc['Total Stockholder Equity', 1])
current_ratio = int(bal_sheet.loc['Total Current Assets', 1]) / int(bal_sheet.loc['Total Current Liabilities', 1])
quick_ratio = (int(bal_sheet.loc['Total Current Assets', 1]) - int(bal_sheet.loc['Inventory', 1])) / int(bal_sheet.loc['Total Current Liabilities', 1])
roe = int(inc_state.loc['Net Income Applicable To Common Shares', 1]) / int(bal_sheet.loc['Total Stockholder Equity', 1])
net_profit_margin = int(inc_state.loc['Net Income Applicable To Common Shares', 1]) / int(inc_state.loc['Total Revenue', 1])

# Print results and round to 4 decimal places
print('Price: $',price)
print('Debt to Equity: ',round(debt_to_equity,4))
print('Current Ratio: ',round(current_ratio,4))
print('Quick Ratio: ',round(quick_ratio,4))
print('Return on Equity: '+'{:.4%}'.format(roe))
print('Net Profit Margin: '+'{:.4%}'.format(net_profit_margin))
