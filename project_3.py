print('Hello World!')

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


class Tree:

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        
    def __str__(self):
        return "{0}".format(self.value)

    def leaf(self):
        return self.left is None and self.right is None

    def inorder_leaves(self):
        """
        Yields:
           list of type(self.value): list of all values in sorted order
        """
        if self.leaf():
            return [self.value]
        else:
            left_leaves = self.left.inorder_leaves()
            right_leaves = self.right.inorder_leaves()
            return left_leaves + right_leaves
        
    def stock_weight_total(self):
        total_stock_value = 0
        for i in self.inorder_leaves():
            total_stock_value += i.cap
        return total_stock_value
            

def build_treemap(stocks):
    """
    Takes a list of Stocks and returns a binary tree, constructed greedily,
    where each internal node represents the market cap of its two children,
    and each leaf is a Stock.
    
    Leaves contain the original Stock objects.
    Internal nodes store "Super" stocks that represent the sum of the
    market caps of all Stocks in their subtree.
    
    Args:
        stocks (list of Stock): a list of Stock objects

    Yields:
        Tree: the root node of the binary tree
    """
    trees = [Tree(stock) for stock in stocks]
    trees.sort(reverse=True, key=lambda t: t.value.cap)
    while len(trees) > 1:
        tree1 = trees.pop()
        tree2 = trees.pop()
        t1value = tree1.value
        t2value = tree2.value
        superstock = Stock(t1value.symbol + " " + t2value.symbol,
                           t1value.cap + t2value.cap,
                           t1value.change + t2value.change)
        trees.append(Tree(superstock, tree1, tree2))
        trees.sort(reverse=True, key=lambda t: t.value.cap)
    print(trees[0])
    


