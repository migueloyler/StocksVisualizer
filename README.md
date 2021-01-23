# StocksVisualizer
A Web Scraper that fetches stock data from yahoo (deprecated) and generates a picture with squares with their area corresponding to their market cap, green if going up, red if going down

Project 3: Stock Visualization
This lab explores visualizing stock data by market cap and percentage changes over small spans of time. The data comes from yahoo finance and is downloaded in CSV format. Our visualization be a treemap, which are ubiquitous in finance.
The visualization is based on a binary tree. We will produce something very similar in our lab, starting from scratch. We’ll read the data off the internet, scrub it and eventually visualize it.
Step 1: Software Needed
You’ll need several packages to do this project. Some of them you should already have from the previous assignment: virtualenv (optional), and pillow. Another that you will need is an HTTP library called requests. You can install this using pip like so:
$ pip install requests
 
 Step 2: Grabbing Data
The file fetch.py contains skeleton code to download a CSV file containing stock symbols, market capitalization, and price change percentages over a 50 day moving average. Here is how it works.
•
•
The function nasdaq_top_100 grabs some CSV information about the NASDAQ 100 stocks using the requests library, parses it, and returns a list
of stock symbols. This function is provided.
The function from_url takes a list of stock symbols and constructs a URL to download symbol, market cap, and percentage change data in CSV format. Here is an example URL to grab information about Apple, Google, and Facebook. The f parameter in the URL asks for data about the stock symbol (s), the market cap (j1) and the percentage change in the 50-day moving average (m8)
http://download.finance.yahoo.com/d/quotes.csv?s=AAPL,GOOG,FB&f=sj1m8 
You need to write the function so it returns the appropriately formatted URL. In other words, you'll return the above string, but with the correct stock symbols inserted and formatted properly.
The main function is provided. It grabs the CSV file from the URL that you built and prints it to straight to standard out.
Running
$ python3 fetch.py 
will print out this data in CSV format to the terminal. You can (and should) redirect this output to a file by typing
$ python3 fetch.py > data.csv
The first few lines of the data should look similar to this:
"ATVI",32.65B,+2.205%
"ADBE",54.36B,+5.32% “AKAM",9.68B,+3.79%
•
•
•
Step 3: Scrubbing Data
The file stocks.py contains a function called stock_info_from that takes a filename for a file in CSV format and returns a list of stocks where each Stock is an instance of a Stock that contains a stock symbol, market cap, and percentage increase.
You should start by defining a simple Stock class with three member variables symbol, cap, and change.

 Next implement stock_info_from. You should open the file using the with syntax and make use of csv.reader to parse the CSV.
You will need to massage the market cap and percentage data as described in the docstring. You will need to define three helper functions inside the definition of stock_info_from:
to_billion(s), which converts a string of the form XX.XXB into an appropriately sized integer, and
to_float(s), which converts a string of the form [+,-]XXX.X% and returns floating point number representing the rate (i.e., 25.2% becomes .252), and
row_to_stock, which converts a row returned by the CSV reader (i.e., a list of three strings) into a stock
The stocks stocks should be sorted by market cap. To do this, make sure to read up on using the key parameter to the sort method along with the operator.attrgetter function. Also, remember that sorting is a side- effecting operation on lists; it does not return a new list
Make sure to test your function out in Python. Your data should look similar to the following:
>>> import stocks
>>> stocks.stock_info_from("data.csv") [Stock(ATVI, 32650000000, 0.02205), Stock(ADBE,
54360000000, 0.053200000000000004), ..., ] >>>
Step 4: Making Rectangles
Recall from lecture how we could view the tree produced from build_treemap as partitioning the unit square into a series of rectangles that collectively tile the square.
Our goal in this step is to write a function generate_rects that when given a Tree tree, a Rectangle rect, and an orientation (either 'H' or 'V') returns the tiling list of rectangles.
This function will be similar to the inorder_leaves method of the tree class. It will recursively construct a list of rectangles that correspond to the partition of
  
 the unit square induced by the tree. Each level of the recursion splits the given rectangle along the given orientation according to the weights of its left and right children. Consider the figure below where the grey nodes correspond to leaves of the tree (i.e., stocks) with corresponding caps. You can view the rectangle generation process as starting at the top with the rectangle in all black, and splitting that rectangle into two rectangles corresponding to a 3/7 and 4/7 split along the horizontal axis. This process continues until you reach a leaf, which yields one of the rectangles.
 
 Let’s break our recursive function down into the base case and the recursive case.
• Base case: Like with inorder_leaves, if tree is a leaf, then we want to
generate a rectangle. In this case, the rectangle we want to generate is the
one passed to the function, so we return it in a list.
• Recursive case: If we are at an internal node, then we need to split the
given rectangle into two new rectangles along the given orientation. You can do this with the provided split_rect function. Call the first rectangle the left_rect and the second rectangle right_rect. Now you should make two recursive calls to generate_rects: one with tree.left, left_rect, and the opposite orientation (i.e. 'V' if 'H' or 'H' if 'V') and one with the symmetric call for the right tree. Both of these recursive calls will return lists of rects, which you can combine and return.
You are given skeleton code for the function with the base case already filled in. You can test the code with the following:
>>> from stocks import Stock
>>> from viz import generate_rects
>>> from tree import build_treemap
>>> generate_rects(build_treemap([Stock('',5,0),
Stock('',10,0), Stock('',20,0)])) [Rectangle(0, 0, 0.3333333333333333,
0.42857142857142855), Rectangle(0.3333333333333333, 0, 1, 0.42857142857142855),
Rectangle(0, 0.42857142857142855, 1, 1)] >>>
Step 5: Visualizing Rectangles
At this point most of the hard work is done. The draw_rects function takes an image, a list of N rectangles that collectively tile the unit square, and a list of N colors and draws a projection of each rectangle, filled with the appropriate color, onto the image.
Some notes:
• Image objects have a size attribute that returns a tuple (width,height)
so you can always get dimensions from the object using w, h = im.size.

 • Any point (x,y) of the unit square corresponds to the point (x × width, y × height) in your image. Use this to map your rectangles onto the image appropriately.
• Consider using zip to pair your rectangles with their appropriate colors. Step 6: Putting it all Together
The function draw should perform the following:
1. Create a Tree using the build_treemap function from the tree module.
2. Use the inorder_leaves of the tree to create a list of the N stocks in an
order corresponding to the leaves of the tree.
3. Generate N rectangles using generate_rects function. These rectangles
collectively tile the unit square and are ordered to correspond to the stocks in
the leaves of the tree.
4. Generate a list of N colors using the create_color function, which is
provided. Consider using a list comprehension here that iterates over the
stocks corresponding to the leaves of the tree.
5. Use draw_rects and then draw_symbols to create the final image.
To run your code from the command line use:
$ python viz.py data.csv stocks.png 1024 1024
I will post instructions for submitting your code in the coming days.
This project will be at collaboration level 2, but with one exception. You are allowed to talk to the TAs. However, the help they provide may be limited to advice for debugging and the like.
Your visualization should look like this:

 
