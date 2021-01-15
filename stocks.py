import csv

#constants
PERCENT_TO_DECIMAL = 0.01
COMPANY_SYMBOL = 0
STOCK_CAP = 1
STOCK_CHANGE = 2


class Stock:
    """class that defines the properites and behaviors of Stocks"""
    
    def __init__(self, symbol, cap, change):
        """
        Args:
            symbol (str): the actual stock symbol
            cap (int): market capitalization (the actual billion dollar number)
            change (float): the percent, where -20.5%  is -0.205
        """
        self.symbol = symbol
        self.cap = cap
        self.change = change
        
        # write definition here

    def __repr__(self):
        """returns the string representation of a Stock object"""
        return "Stock({}, {}, {})".format(self.symbol, self.cap, self.change)
    
    def get_symbol(self):
        return self.symbol


def stock_info_from(filename):
    """
    Takes a CSV file of the form

    COMPANY STOCK_SYMBOL, MARKET_CAP, PERCENT_CHANGE_50_DAYS

    where

    STOCK_SYMBOL is a string
    MARKET_CAP is a string of the form "XX.XXXB" where B = BILLION
    PERCENT_CHANGE_50_DAYS is a string of the form "[+,-]XXX.X%"

    and returns a list of Stocks

    where

    Stock.symbol is the stock symbol
    Stock.cap is an integer (the actuall billion dollar number) and
    Stock.change is is a float where -20.5%  is -0.205

    Args:
        filename (str): the path of a CSV file containing stock information

    """        
    def to_billion(s):
        """converts str object 's' to an integer""" 
        cap_float = float(s[:-1])
        cap_int = int(cap_float * 10**9)
        return cap_int
        
        # write def here

    def to_float(s):
        """converts str object 's' to a float"""
        percent_change = float(s[1:-1]) * PERCENT_TO_DECIMAL
        if s[0] == '-':
            percent_change *= -1
            #return "{0:.4f}".format(percent_change)
            return percent_change
        else:
            return percent_change    

    def row_to_stock(row):
        """given a row of a CSV file, returns a Stock object"""
        with open(filename, 'r') as stock_data:
            for data_row_number,data in enumerate(csv.reader(stock_data)):
                if data_row_number == row:
                    stock_instance = Stock(data[COMPANY_SYMBOL],
                                           to_billion(data[STOCK_CAP]),
                                           to_float(data[STOCK_CHANGE]))
                    return stock_instance
                
    with open(filename, 'r') as stock_data:
        iteration_limiter = len(stock_data.readlines())
    stock_list = [row_to_stock(i) for i in range(iteration_limiter)]
    
    sorted_stock_list = sorted(stock_list, key=lambda stock: stock.cap)
    
    market_caps = [sorted_stock_list[i].cap for i in range(iteration_limiter)]
    
    return sorted_stock_list


