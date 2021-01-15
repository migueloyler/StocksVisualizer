import csv

print('Hello World!')

def tester(row):
    with open('data.csv' , 'r') as stock_data:
        for rownum,info in enumerate(csv.reader(stock_data)):
            if row == rownum:
                return info[0]
            
def row_to_stock(row):
    """given a row of a CSV file, returns a Stock object"""
    with open('data.csv', 'r') as stock_data:
        for data_row_number,data in enumerate(csv.reader(stock_data)):
            if data_row_number == row:
                stock_instance = Stock(row[COMPANY_SYMBOL],
                                       row[STOCK_CAP],
                                       row[STOCK_CHANGE])
                print(stock_instance)
    