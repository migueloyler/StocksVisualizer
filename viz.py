import sys
import image
from tree import Tree
from tree import build_treemap
from stocks import stock_info_from


class Rectangle:
    """
    A class that respresents a rectangle using two points (the top left
    and bottom right corners).

    """
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __repr__(self):
        template = "Rectangle({}, {}, {}, {})"
        return template.format(self.x1, self.y1, self.x2, self.y2)


def split_rect(rect, weight1, weight2, orient):
    """
    Takes a single rectangle and divides it into two rectangles.
    The split is made along direction specified by orient.
    The area of the resulting rectangles are proporitional to the weights
    
    Args:
        rect (Rectangle): the original rectangle to split
        weight1 (int): the weight of the left sub-Rectangle
        weight2 (int): the weight of the right sub-Rectangle
        orient (str): the direction to split 'rect' (either 'H' or 'V')

    Yields:
        a pair of Rectangle objects
    """
    r = weight1 / (weight1 + weight2)

    if orient == 'H':
        newpt = rect.y1 + (rect.y2 - rect.y1) * r
        rect1 = Rectangle(rect.x1, rect.y1, rect.x2, newpt)
        rect2 = Rectangle(rect.x1, newpt, rect.x2, rect.y2)
    else:
        newpt = rect.x1 + (rect.x2 - rect.x1) * r
        rect1 = Rectangle(rect.x1, rect.y1, newpt, rect.y2)
        rect2 = Rectangle(newpt, rect.y1, rect.x2, rect.y2)

    return rect1, rect2



def generate_rects(tree, rect=Rectangle(0, 0, 1, 1), orient='H'):
    """
    A function that takes a binary tree, a rectangle, and an orientation,
    and recursively divides the rectangle in proportion to the weights
    of the left and right subtrees.

    Consecutive rectangle splits alternate orientations.

    It returns an ordered list of Rectangle objects where each rectangle
    corresponds to a single Stock, and the list contains a Rectangle for
    each leaf in the tree.

    Args:
        tree (Tree): a binary tree of Stock objects
        rect (Rectangle): a rectangle to split
        orient (str 'H' or 'V'): the orientation to split rect
    Yields:
        a list of Rectangle objects
    """
    if tree.leaf():
        return [rect]
    else:
        left,right = split_rect(rect, tree.left.stock_weight_total(),
                   tree.right.stock_weight_total(), orient)
        return generate_rects(tree.left, left, orient = 'V' if orient == 'H' else 'H') + generate_rects(tree.right, right, orient = 'V' if orient == 'H' else 'H')

def scale_rects(im, rects):
    """
    Scales a list of rectangles creating from a unit Rectangle.
    The resulting list of rectangles is projected onto the dimentions
    of im (where w, h = image.size)
    
    Args:
        im (Image): an Image object where rectangles will be drawn
        rects (list of Rectangle): a list of N rectangles
    Yields:
        None - this function modifies the list of rectangles directly
    """
    w,h = im.size
    for i in range(len(rects)):
        rects[i].x1 = rects[i].x1 * w
        rects[i].y1 = rects[i].y1 * h
        rects[i].x2 = rects[i].x2 * w
        rects[i].y2 = rects[i].y2 * h


    
def draw_rects(im, rects, colors):
    """
    Create the overall visualization using the image.py module.
    
    Args:
        im (Image): an Image object where rectangles will be drawn
        rects (list of Rectangle): a list of N rectangles
        colors (list of (R, G, B, Opacity) tuples):  a list of N colors 
                                      corresponding to the N rectangles
    Yields:
        None
    """
    for rect,color in zip(rects,colors):
        image.draw_rect(im, rect, color,(0,0,0,255))
    #write def here


def draw_symbols(im, rects, stocks):
    """
    Writes each stock symbol name in the top-left corner
    of its respective rectangle.

    Args:
        im (Image): an Image object where symbols are drawn
        rects (list of Rectange): a list of N rectangles, one per Stock
        stocks (list of Stock):  a list of N Stock objects, one per rectangle
    Yields:
        None
    """

    for rect, stock in zip(rects, stocks):
        image.draw_text(im, stock.symbol, rect)


def create_color(pct):
    """Given a float (Stock.change), returns its rectangle's color"""
    weight = 10
    if (pct < 0.0):
        return (153, 0, 0, min(int(255 * weight * abs(pct)), 255))
    else:
        return (0, 153, 0, min(int(255 * weight * abs(pct)), 255))


def draw(stocks, im):
    """
    Creates the overall visualization by:
     - building a treemap of stocks,
     - proportionally dividing the unit rectangle according to the weights
    of the stocks (in the sort order of the treemap's leaves),
     - projecting those rectangles onto a larger image
     - drawing the scaled rectangles with color according to their change,
    and
     - drawing the symbols onto the rectangles
    
    Args:
        stocks (list of Stock): a list of stocks in arbitrary order
        im (Image): an image with width and height {w, h = image.size}
    """
    stock_treemap = build_treemap(stocks)
    inorder_stock_treemap = stock_treemap.inorder_leaves()
    rectangle_objects = generate_rects(stock_treemap)
    scale_rects(im, rectangle_objects)
    stock_percentage_list = []
    for i in inorder_stock_treemap:
        stock_percentage_list.append(i.change)
    rectangle_colors = [create_color(i) for i in stock_percentage_list]
    draw_rects(im, rectangle_objects, rectangle_colors)
    draw_symbols(im, rectangle_objects, inorder_stock_treemap)
    
    
    # write def here


def main(infile, outfile, width, height):

    stocks = stock_info_from(infile)
    im = image.create_image(width, height)
    draw(stocks, im)
    image.save_image(im, outfile)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
