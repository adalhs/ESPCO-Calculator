'''The ESPCO Calculator calculates the package size and weight of an order.  The package size is
determined by accumulating the space of each item the user clicks into the order inside
a counter (total_space_counter).  If the counter exceeds the space available in a box, it goes
up to the next box size.  The values for the space available in each box, as well as the space
each items takes are imaginary numbers that were determined through in-person experimentation
packaging different items inside different size boxes.

For example, 8 wheelhouse (.28 space) and a sauce (.18 space) fit into a small box (12x12x4),
so the small box was given a maximum space of 2.42 (.28 * 8 + .18 = 2.42).

The weight of each item and box size was determined by weighing these in person, passing
them to the calculator and adding up the values of every item the user clicks in a counter
(weight_count). Box weight is added at the end once the program knows what box size is needed
for the space of the items added, since each box size has a different weight.

Because the weight needs to be reported in the
format of "x lb., y oz.", and there are 16 oz. in a lb., all item weights are added in oz. to the
counter (weight_count), and before reporting the weight, it is divided by 16 to give the
lbs. (weight_count_lb), and then divided by modulo of 16 to give the oz. (weight_count_oz).  It
is then reported as (weight in oz. / 16)lb., (weight in oz. % 16)oz, in other words,
(weight_count_lb / 16)lb., (weight_count_oz % 16)oz.

Each time the user wants to calculate the size and weight of an order, they must press the 'ENTER
NEW ORDER' button to reset the counters to 0 (reset_order()).  It is possible that the space and
weight values in this program will have to be changed in the future due to things like change
in pretzel weight, how much air is in pretzel bags, etc.'''

import tkinter as tk
from tkinter import ttk

class Item():
    def __init__(self, space, weight):
        self.space = space
        self.weight = weight

mustard_box = Item(0, 4.00) #packaging included in all box weights
small_box = Item(0, 9.00)
medium_box = Item(0, 10.00)
large_box = Item(0, 12.00)
twelve_by_10 = Item(0, 14.00)
xlarge_box = Item(0, 18.00)
case_1 = Item(0, 17.00)
case_3 = Item(0, 22.00)

wh = Item(0.28, 4.00)
tb = Item(0.50, 9.00)
bite = Item(0.50, 12.50)
slider = Item(0.50, 9.00)
topknot = Item(0.37, 6.50)
fourseam = Item(0.57, 8.50)
ribbon = Item(0.37, 4.00)
salt = Item(0.00, 1.00)
mustard = Item(0.18, 9.00)
waffle = Item(0.134, 3.20)

root = tk.Tk()
root.title("ESPCO Calculator")

INSTRUCTIONS = """***IMPORTANT***\nCalculate button must be clicked ONLY after ALL items have
been added for correct package size and weight calculations."""

total_space_counter = tk.DoubleVar(0.00) #accumulates space of all item for appropiate package size
gb_space_counter = tk.DoubleVar(0.00) #accumulates space of gift boxes
package_size = tk.StringVar() #will display package size depending on space accumulated
weight_count = tk.DoubleVar(0.00)  #accumulates weight of all items for appropiate package weight
weight_count_lb = tk.DoubleVar(0.00) #weight_count divided by 16 to present lb.
weight_count_oz = tk.DoubleVar(0.00) #weight_count divided by modulo 16 to present oz. (16oz. in 1lb.)
gift_box_counter = tk.DoubleVar(0.00) #counter used for package size when more than 1 gift box added
calculate_counter = tk.IntVar(0) #counter used to add box weight at the end and finish calculations
gb_box_weight_counter = tk.IntVar(0) #counter used to add the weight of the box of gift boxes added

'''The adder function adds the space and weight of every item added, every button has a space
and weight associated with it that gets passed to the function as its first and second parameter
respectively.  Every button also sends a third parameter, "calc". This calc parameter is 0 for every
button with the exception of the Calculate button which sends a 1, indicating to the function adder
that the user has finished entering the last item in the order and to go to the calculate function
and do the necessary calculations to present the user with their order's package size and weight.
Gift box buttons also send a fourth parameter, gift_box_code, this is used to determine how many
gift boxes are in an order.  The values it can have are 8, 10, 12, etc. until 24.  Representing
the space different combinations of gift boxes would take. 8 representing the 8 vertical inches that
the smallest combination of gift boxes that has to be packed separately can have (2 12x4s), and 24
representing the 24 vertical inches that the biggest combinations of gift boxes that must be packed
separately can have (several combinations of boxes can measure that).'''
def adder(space, gift_box_space, weight, gift_box_code, calculate_code, string1, gbweight):
    '''in tkinter .get() has to be used to "get" something's value and .set() to "set" it,
    it's not enough to simply use the variable names'''
    #keeps track of gift boxes by vertical inches
    gift_box_counter.set(round(gift_box_counter.get(), 2) + gift_box_code)
    #totals package size and weight when switched to 1
    calculate_counter.set(calculate_code)
    #keeps track of order space when one or no gift boxes have been added
    total_space_counter.set(round(total_space_counter.get(), 3) + space + gift_box_space)
    #rounded to 3 because of waffle space, if round to two package size was not completely accurate
    #keeps track of space taken by gift boxes when only one gift box has been added, this is done
    #so that A) the space of the ITEMS inside the gift boxes can be added normally to the order
    #when there is only one gift box (since it gets packed together with the rest of the order)
    #and for B) so that space can be subtracted in the gift box management IF statement
    #from the total_space_counter when there is more than one gift box, since they are packed in
    #separate boxes, and in that case, the space of the items in the box don't count, what counts
    #is the vertical inches of the gift box (gift_box_counter) that count
    gb_space_counter.set(round(gb_space_counter.get(), 2) + gift_box_space)
    #This counter adds the weights of the boxes of gift boxes, and this weight will only be added
    #if the order has two or more gift boxes in the gift box IF statement.  Otherwise it will not
    #do anything, as if there is only one, or no gift boxes, no additional box weights are needed
    gb_box_weight_counter.set(gb_box_weight_counter.get() + gbweight)
    #round is used in the counters above to avoid situation where a value had many decimals
    #throwing off the counters above 2 decimal places

    items_list.insert("end", string1)  #adds item at end of list?
    items_list.see("end")    #scrollbar automatically scrolls to last item added (item at end)

    '''This IF gives package size depending on space of items when there are no gift boxes, or only
    one gift box in order.  It also adds the weight of the box for the respective package size.
    The package size when an order has more than one gift box has to be calculated on a different
    IF statement (located below this one), due to the differences in which those orders are packed
    when compared to orders with one, or no gift boxes.'''
    #explanation of why I had to add gb_box_weight_counter is on the IF statemente after this one
    if (gift_box_counter.get() <= 8.00 and calculate_counter.get() == 1 and gb_box_weight_counter.get() <= 12):
        if total_space_counter.get() == 0.00:
            weight += 2
            package_size.set("Package: Salt Envelope")
        elif .72 >= total_space_counter.get() > 0.00:
            weight += 4
            package_size.set("Package: Mustard Box (6x6x4)")
        elif 2.42 >= total_space_counter.get() > .72:
            weight += 9
            package_size.set("Package: Small Box (12x12x4)")
        elif 4.00 >= total_space_counter.get() > 2.42:
            weight += 10
            package_size.set("Package: Medium Box (12x12x6)")
        elif 6.00 >= total_space_counter.get() > 4.00:
            weight += 12
            package_size.set("Package: Large Box (12x12x8)")
        elif 8.00 >= total_space_counter.get() > 6.00:
            weight += 14
            package_size.set("Package: 12x12x10 Box")
        elif 10.10 >= total_space_counter.get() > 8.00:
            weight += 18
            package_size.set("Package: Extra Large Box (12x12x12)")
        elif 12.00 >= total_space_counter.get() > 10.10:
            weight += 17
            package_size.set("Package: Case 1 (16x13x10)")
        #elif 20.16 >= total_space_counter.get() > 12.00:         Case 3s will no
            #weight += 22                                         longer be an option
            #package_size.set("Package: Case 3 (12x12x24)")       for multiple packaging
        else:
            package_size.set("Needs multiple packaging.")


    '''Overrides package size handled by IF statement above if more than one gift box and adds
    weight of all the boxes to the package.  Since there is more than one combination of gift boxes
    that adds to the same vertical inch measurement (gift_box_counter), the weight that is added to
    the order at the end is that of the HEAVIEST COMBINATION OF BOXES.  This is done to make the
    code much smaller and simpler to understand, since the other solution would be to have a nested
    elif for every possible box combination.  Regardless, the weight should not be off by more than
    a few ounces in any case.'''
    #if there is more than one gift box... gb_box_weight_counter had to be added, otherwise just one 12x8 was
    #triggering the 8 inches more than one gift box, but one 12x8 is just one gift box.  Added the weight because
    #if there is more than one gift box the weight parameter that accumulates from them will be > 12
    if (gift_box_counter.get() >= 8.00 and calculate_counter.get() == 1 and gb_box_weight_counter.get() > 12):
        #takes off the space the ITEMS inside the gift boxes take from the space counter, so I can
        #see only if there are other non-gift boxes along with the gift boxes, since this will let
        #me see what box size I need
        total_space_counter.set(total_space_counter.get() - gb_space_counter.get())

        #if there are any gift box combination that don't fit in a Case 3 (> 24.00)
        if gift_box_counter.get() > 24.00:
            package_size.set("Needs multiple packaging.")

        #if there are two 12x4 gift boxes (8 inches) and...
        elif gift_box_counter.get() == 8.00:
            #...no other pretzels (smallest pretzel order is two bites/turnbuckles (1.00))
            if total_space_counter.get() < 1.00:
                package_size.set("Package: 12x12x10 Box")
                weight += gb_box_weight_counter.get() + 14 #adds weight of order boxes and a 12x10
            #...another 12x4 in the order
            elif (total_space_counter.get() >= 1.00 and total_space_counter.get() <= 2.42):
                package_size.set("Package: Extra Large Box (12x12x12)")
                weight += gb_box_weight_counter.get() + 18 #adds weight of order boxes and a 12x12
            #...another 12x6 in the order
            elif (total_space_counter.get() > 2.42 and total_space_counter.get() <= 4.00):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x8 in the order
            elif (total_space_counter.get() > 4.00 and total_space_counter.get() <= 6.00):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x10 in the order
            elif (total_space_counter.get() > 6.00 and total_space_counter.get() <= 8.00):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x12 in the order
            elif (total_space_counter.get() > 8.00 and total_space_counter.get() <= 10.10):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...something bigger than a 12x12 in the order, will not fit
            else:
                package_size.set("Needs multiple packaging.")

        #if there is one 12x4 and one 12x6 gift boxes (10 inches) and...
        elif gift_box_counter.get() == 10.00:
            #...no other pretzels (smallest pretzel order is two bites/turnbuckles (1.00))
            if total_space_counter.get() < 1.00:
                package_size.set("Package: 12x12x10 Box")
                weight += gb_box_weight_counter.get() + 14 #adds weight of a 12x4, a 12x6 and a 12x10 box
            #...another 12x4 in the order
            elif (total_space_counter.get() >= 1.00 and total_space_counter.get() <= 2.42):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x6 in the order
            elif (total_space_counter.get() > 2.42 and total_space_counter.get() <= 4.00):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x8 in the order
            elif (total_space_counter.get() > 4.00 and total_space_counter.get() <= 6.00):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x10 in the order
            elif (total_space_counter.get() > 6.00 and total_space_counter.get() <= 8.00):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x12 in the order
            elif (total_space_counter.get() > 8.00 and total_space_counter.get() <= 10.10):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...something bigger than a 12x12 in the order, will not fit
            else:
                package_size.set("Needs multiple packaging.")

        #if there is are three 12x4 gift boxes (12 inches), or
        #two 12x6 gift boxes (12 inches), or one 12x4 and one 12x8 gift boxes (12 inches) and...
        elif gift_box_counter.get() == 12.00:
            #...no other pretzels (smallest pretzel order is two bites/turnbuckles (1.00))
            if total_space_counter.get() < 1.00:
                package_size.set("Package: Extra Large Box (12x12x12)")
                weight += gb_box_weight_counter.get() + 18 #adds weight of order boxes and a 12x12
            #...another 12x4 in the order
            elif (total_space_counter.get() >= 1.00 and total_space_counter.get() <= 2.42):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x6 in the order
            elif (total_space_counter.get() > 2.42 and total_space_counter.get() <= 4.00):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x8 in the order
            elif (total_space_counter.get() > 4.00 and total_space_counter.get() <= 6.00):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x10 in the order
            elif (total_space_counter.get() > 6.00 and total_space_counter.get() <= 8.00):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x12 in the order
            elif (total_space_counter.get() > 8.00 and total_space_counter.get() <= 10.10):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...something bigger than a 12x12 in the order, will not fit
            else:
                package_size.set("Needs multiple packaging.")

        #if there are two 12x4 and one 12x6 gift boxes (14 inches), or
        #one 12x8 and one 12x6 gift boxes (14 inches) and...
        elif gift_box_counter.get() == 14.00:
            #...no other pretzels (smallest pretzel order is two bites/turnbuckles (1.00))
            if total_space_counter.get() < 1.00:
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x4 in the order
            elif (total_space_counter.get() >= 1.00 and total_space_counter.get() <= 2.42):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x6 in the order
            elif (total_space_counter.get() > 2.42 and total_space_counter.get() <= 4.00):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x8 in the order
            elif (total_space_counter.get() > 4.00 and total_space_counter.get() <= 6.00):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x10 in the order
            elif (total_space_counter.get() > 6.00 and total_space_counter.get() <= 8.00):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...something bigger than a 12x10 in the order, will not fit
            else:
                package_size.set("Needs multiple packaging.")

        #if there are four 12x4 gift boxes (16 inches), or one 12x4 and two 12x6
        #gift boxes (16 inches), or two 12x4 and one 12x8 gift boxes (16 inches)...
        elif gift_box_counter.get() == 16.00:
            #...no other pretzels (smallest pretzel order is two bites/turnbuckles (1.00))
            if total_space_counter.get() < 1.00:
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x4 in the order
            elif (total_space_counter.get() >= 1.00 and total_space_counter.get() <= 2.42):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x6 in the order
            elif (total_space_counter.get() > 2.42 and total_space_counter.get() <= 4.00):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x8 in the order
            elif (total_space_counter.get() > 4.00 and total_space_counter.get() <= 6.00):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...something bigger than a 12x8 in the order, will not fit
            else:
                package_size.set("Needs multiple packaging.")

        #if there are three 12x4 and one 12x6 gift boxes (18 inches), or three 12x6 gift boxes
        #(18 inches), or one 12x4, one 12x6 and one 12x8 gift boxes (18 inches)...
        elif gift_box_counter.get() == 18.00:
            #...no other pretzels (smallest pretzel order is two bites/turnbuckles (1.00))
            if total_space_counter.get() < 1.00:
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x4 in the order
            elif (total_space_counter.get() >= 1.00 and total_space_counter.get() <= 2.42):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x6 in the order
            elif (total_space_counter.get() > 2.42 and total_space_counter.get() <= 4.00):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...something bigger than a 12x6 in the order, will not fit
            else:
                package_size.set("Needs multiple packaging.")

        #if there are five 12x4 gift boxes (20 inches), or two 12x4 and two 12x6 gift boxes
        #(20 inches), or three 12x4 and one 12x8 gift boxes (20 inches), or two 12x6 and one
        #12x8 gift boxes (20 inches), or one 12x4 and two 12x8 gift boxes (20 inches)...
        elif gift_box_counter.get() == 20.00:
            #...no other pretzels (smallest pretzel order is two bites/turnbuckles (1.00))
            if total_space_counter.get() < 1.00:
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...another 12x4 in the order
            elif (total_space_counter.get() >= 1.00 and total_space_counter.get() <= 2.42):
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...something bigger than a 12x4 in the order, will not fit
            else:
                package_size.set("Needs multiple packaging.")

        #if there are four 12x4 and one 12x6 gift boxes (22 inches), or one 12x4 and three
        #12x6 gift boxes (22 inches), or two 12x4, one 12x6 and one 12x8 gift boxes
        #(22 inches), or one 12x6 and two 12x8 gift boxes (22 inches)...
        elif gift_box_counter.get() == 22.00:
            #...no other pretzels (smallest pretzel order is two bites/turnbuckles (1.00))
            if total_space_counter.get() < 1.00:
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...no other box fits in the order
            else:
                package_size.set("Needs multiple packaging.")

        #if there are six 12x4 gift boxes (24 inches), or three 12x4 and two 12x6 gift boxes
        #(24 inches), or three 12x8 gift boxes (24 inches), or four 12x6 gift boxes (24
        #inches), or four 12x4 and one 12x8 gift boxes (24 inches), or one 12x4, two 12x6,
        #and one 12x8 gift boxes (24 inches), or two 12x4 and two 12x8 gift boxes (24 inches)...
        elif gift_box_counter.get() == 24.00:
            #...no other pretzels (smallest pretzel order is two bites/turnbuckles (1.00))
            if total_space_counter.get() < 1.00:
                package_size.set("Package: Case 3 (12x12x24)")
                weight += gb_box_weight_counter.get() + 22 #adds weight of order boxes and a Case 3
            #...no other box fits in the order
            else:
                package_size.set("Needs multiple packaging.")

    #this will need space count to add final container weight if there are gift boxes
    weight_count.set(weight_count.get() + weight)
    weight_count_lb.set(int(weight_count.get() / 16))
    #int() is used above so the lb number has no decimals as those would belong to the oz part of the weight
    weight_count_oz.set(int(weight_count.get() % 16))

def reset_order():
    total_space_counter.set(0.00)
    gb_space_counter.set(0.00)
    weight_count.set(0)
    weight_count_lb.set(0)
    weight_count_oz.set(0)
    package_size.set("Package: ")
    gift_box_counter.set(0.00)
    calculate_counter.set(0)
    
    items_list.delete(0, "end")
    gb_box_weight_counter.set(0)


right_side_frame = ttk.Frame(root) #contains calculate and new order buttons/instruction and items labels
right_side_frame.grid(row = 0, column = 1, sticky = "N", padx = (30, 20))

instructions_label = ttk.Label(right_side_frame, text = INSTRUCTIONS)
instructions_label.grid(row = 0, column = 0, sticky = "N", pady = (5, 10))
calculate_button = ttk.Button(right_side_frame, text = "CALCULATE", command = lambda: adder(0, 0, 0, 0, 1, "", 0))
calculate_button.grid(row = 1, column = 0, padx = (200, 0))
#erase_button resets everything to 0 and box size to "No items entered"
erase_button = ttk.Button(right_side_frame, text = "ENTER NEW ORDER", command = lambda: reset_order())
erase_button.grid(row = 1, column = 0, padx = (0, 200))

output_frame1 = ttk.Frame(right_side_frame) #contains output labels
output_frame1.grid(row = 2, column = 0, pady = 20)

space_frame = ttk.Frame(output_frame1) #contains package size label
space_frame.grid(row = 0, column = 0)
space_label = ttk.Label(space_frame, textvariable = package_size)
space_label.grid(row = 0, column = 0)
space_label.config(font = 16)

output_frame2 = ttk.Frame(right_side_frame) #contains output labels
output_frame2.grid(row = 3, column = 0, pady = (0, 20))
weight_text_label = ttk.Label(output_frame2, text = "Package weight: ")
weight_text_label.grid(row = 2, column = 0)
weight_text_label.config(font = 16)
weight_in_lb_label = ttk.Label(output_frame2, textvariable = weight_count_lb)
weight_in_lb_label.grid(row = 2, column = 1)
weight_in_lb_label.config(font = 16)
lb_text_label = ttk.Label(output_frame2, text = "lb.")
lb_text_label.grid(row = 2, column = 2)
lb_text_label.config(font = 16)
weight_in_oz_label = ttk.Label(output_frame2, textvariable = weight_count_oz)
weight_in_oz_label.grid(row = 2, column = 3)
weight_in_oz_label.config(font = 16)
oz_text_label = ttk.Label(output_frame2, text = "oz.")
oz_text_label.grid(row = 2, column = 4)
oz_text_label.config(font = 16)

items_frame = ttk.Frame(right_side_frame) #contains items label
items_frame.grid(row = 4, column = 0)

list_scrollbar = tk.Scrollbar(items_frame, orient = "vertical")
items_list = tk.Listbox(items_frame, width = 32, height = 14, font = 10, yscrollcommand = list_scrollbar.set)
list_scrollbar.config(command = items_list.yview)
list_scrollbar.pack(side = "right", fill = "y")
items_list.pack(side = "left", fill = "both", expand = True)


left_side_frame = ttk.Frame(root) #container for all buttons except erase and calculate
left_side_frame.grid(row = 0, column = 0, sticky = "N")

buttonframe_1 = ttk.Frame(left_side_frame) #container WH, TB, BITE, SD, TK and FS frames
buttonframe_1.grid(row = 0, column = 0)

fs_frame = ttk.Frame(buttonframe_1) #container for FS (fourseam) buttons
fs_frame.grid(row = 0, column = 0, padx = 10, pady = 10)
fs_label = ttk.Label(fs_frame, text = "FOURSEAM", font = 16)
fs_label.grid(row = 0, column = 0)

tk_frame = ttk.Frame(buttonframe_1) #container for TK (topknots) buttons
tk_frame.grid(row = 0, column = 1, padx = 10, pady = 10)
tk_label = ttk.Label(tk_frame, text = "TOPKNOT", font = 16)
tk_label.grid(row = 0, column = 0)

wh_frame = ttk.Frame(buttonframe_1) #container for WH (wheelhouse) buttons
wh_frame.grid(row = 0, column = 2, padx = 10, pady = 10)
wh_label = tk.Label(wh_frame, text = "WHEELHOUSE", font = 16)
wh_label.grid(row = 0, column = 0)

tb_frame = ttk.Frame(buttonframe_1) #container for TB (turnbuckle) buttons
tb_frame.grid(row = 0, column = 3, padx = 10, pady = 10)
tb_label = ttk.Label(tb_frame, text = "TURNBUCKLE", font = 16)
tb_label.grid(row = 0, column = 0)

bite_frame = ttk.Frame(buttonframe_1) #container for BITE (bites) buttons
bite_frame.grid(row = 0, column = 4, padx = 10, pady = 10)
bite_label = ttk.Label(bite_frame, text = "BITES", font = 16)
bite_label.grid(row = 0, column = 0)

sd_frame = ttk.Frame(buttonframe_1) #container for SD (sliders) buttons
sd_frame.grid(row = 0, column = 5, padx = 10, pady = 10)
sd_label = ttk.Label(sd_frame, text = "SLIDERS", font = 16)
sd_label.grid(row = 0, column = 0)

buttonframe_2 = ttk.Frame(left_side_frame) #container for GB frames
buttonframe_2.grid(row = 1, column = 0)

gb1_frame = ttk.Frame(buttonframe_2) #container for GB (gift boxes) buttons
gb1_frame.grid(row = 0, column = 1, padx = 10, pady = 10)
gb1_label = ttk.Label(gb1_frame, text = "GIFT BOXES 1", font = 16)
gb1_label.grid(row = 0, column = 0)

gb2_frame = ttk.Frame(buttonframe_2) #container for GB (gift boxes) buttons
gb2_frame.grid(row = 0, column = 2, padx = 10, pady = 10)
gb2_label = ttk.Label(gb2_frame, text = "GIFT BOXES 2", font = 16)
gb2_label.grid(row = 0, column = 0)

gb3_frame = ttk.Frame(buttonframe_2) #container for GB (gift boxes) buttons
gb3_frame.grid(row = 0, column = 3, padx = 10, pady = 10)
gb3_label = ttk.Label(gb3_frame, text = "GIFT BOXES 3", font = 16)
gb3_label.grid(row = 0, column = 0)

buttonframe_3 = ttk.Frame(left_side_frame) #container for TOPPING, SAUCE and WAFFLE frames
buttonframe_3.grid(row = 2, column = 0)

salt_frame = ttk.Frame(buttonframe_3) #container for salts/sugars/toppers buttons
salt_frame.grid(row = 0, column = 0, padx = 10, pady = 10)
salt_label = ttk.Label(salt_frame, text = "SALTS / SUGARS / TOPPERS", font = 16)
salt_label.grid(row = 0, column = 0)

mustard_frame = ttk.Frame(buttonframe_3) #container for mustards/sauces buttons
mustard_frame.grid(row = 0, column = 1, padx = 10, pady = 10)
mustard_label = ttk.Label(mustard_frame, text = "MUSTARDS / SAUCES", font = 16)
mustard_label.grid(row = 0, column = 0)

waffle_frame = ttk.Frame(buttonframe_3) #container for waffles buttons
waffle_frame.grid(row = 0, column = 2, padx = 10, pady = 10)
waffle_label = ttk.Label(waffle_frame, text = "WAFFLES", font = 16)
waffle_label.grid(row = 0, column = 0)


#wh_frame buttons
wh_6 = ttk.Button(wh_frame, text = "6 WHEELHOUSE", command = lambda: adder(wh.space * 6, 0, wh.weight * 6 + 1, 0, 0, "6 Wheelhouse added\n", 0))
wh_6.grid(row = 1, column = 0, sticky = "EW", pady = 3)
wh_12 = ttk.Button(wh_frame, text = "12 WHEELHOUSE", command = lambda: adder(wh.space * 12, 0, wh.weight * 12 + 2, 0, 0, "12 Wheelhouse added\n", 0))
wh_12.grid(row = 2, column = 0, sticky = "EW", pady = 3)
wh_18 = ttk.Button(wh_frame, text = "18 WHEELHOUSE", command = lambda: adder(wh.space * 18, 0, wh.weight * 18 + 3, 0, 0, "18 Wheelhouse added\n", 0))
wh_18.grid(row = 3, column = 0, sticky = "EW", pady = 3)
wh_24 = ttk.Button(wh_frame, text = "24 WHEELHOUSE", command = lambda: adder(wh.space * 24, 0, wh.weight * 24 + 4, 0, 0, "24 Wheelhouse added\n", 0))
wh_24.grid(row = 4, column = 0, sticky = "EW", pady = 3)

#tb_frame buttons
tb_12 = ttk.Button(tb_frame, text = "12 TURNBUCKLE", command = lambda: adder(tb.space * 2, 0, tb.weight * 2 + 1, 0, 0, "12 Turnbuckle added\n", 0))
tb_12.grid(row = 1, column = 0, sticky = "EW", pady = 3)
tb_24 = ttk.Button(tb_frame, text = "24 TURNBUCKLE", command = lambda: adder(tb.space * 4, 0, tb.weight * 4 + 2, 0, 0, "24 Turnbuckle added\n", 0))
tb_24.grid(row = 2, column = 0, sticky = "EW", pady = 3)
tb_36 = ttk.Button(tb_frame, text = "36 TURNBUCKLE", command = lambda: adder(tb.space * 6, 0, tb.weight * 6 + 3, 0, 0, "36 Turnbuckle added\n", 0))
tb_36.grid(row = 3, column = 0, sticky = "EW", pady = 3)
tb_48 = ttk.Button(tb_frame, text = "48 TURNBUCKLE", command = lambda: adder(tb.space * 8, 0, tb.weight * 8 + 4, 0, 0, "48 Turnbuckle added\n", 0))
tb_48.grid(row = 4, column = 0, sticky = "EW", pady = 3)

#bite_frame buttons
bite_2 = ttk.Button(bite_frame, text = "2 BITES", command = lambda: adder(bite.space * 2, 0, bite.weight * 2 + 1, 0, 0, "2 Bites added\n", 0))
bite_2.grid(row = 1, column = 0, sticky = "EW", pady = 3)
bite_4 = ttk.Button(bite_frame, text = "4 BITES", command = lambda: adder(bite.space * 4, 0, bite.weight * 4 + 2, 0, 0, "4 Bites added\n", 0))
bite_4.grid(row = 2, column = 0, sticky = "EW", pady = 3)
bite_6 = ttk.Button(bite_frame, text = "6 BITES", command = lambda: adder(bite.space * 6, 0, bite.weight * 6 + 3, 0, 0, "6 Bites added\n", 0))
bite_6.grid(row = 3, column = 0, sticky = "EW", pady = 3)
bite_8 = ttk.Button(bite_frame, text = "8 BITES", command = lambda: adder(bite.space * 8, 0, bite.weight * 8 + 4, 0, 0, "8 Bites added\n", 0))
bite_8.grid(row = 4, column = 0, sticky = "EW", pady = 3)

#sd_frame buttons
sd_12 = ttk.Button(sd_frame, text = "12 SLIDERS", command = lambda: adder(slider.space * 2, 0, slider.weight * 2 + 1, 0, 0, "12 Sliders added\n", 0))
sd_12.grid(row = 1, column = 0, sticky = "EW")
sd_24 = ttk.Button(sd_frame, text = "24 SLIDERS", command = lambda: adder(slider.space * 4, 0, slider.weight * 4 + 2, 0, 0, "24 Sliders added\n", 0))
sd_24.grid(row = 2, column = 0, sticky = "EW")
sd_36 = ttk.Button(sd_frame, text = "36 SLIDERS", command = lambda: adder(slider.space * 6, 0, slider.weight * 6 + 3, 0, 0, "36 Sliders added\n", 0))
sd_36.grid(row = 3, column = 0, sticky = "EW")

#tk_frame buttons
tk_4 = ttk.Button(tk_frame, text = "4 TOPKNOT", command = lambda: adder(topknot.space * 4, 0, topknot.weight * 4 + 1, 0, 0, "4 Topknot added\n", 0))
tk_4.grid(row = 1, column = 0, sticky = "EW", pady = 3)
tk_8 = ttk.Button(tk_frame, text = "8 TOPKNOT", command = lambda: adder(topknot.space * 8, 0, topknot.weight * 8 + 2, 0, 0, "8 Topknot added\n", 0))
tk_8.grid(row = 2, column = 0, sticky = "EW", pady = 3)
tk_12 = ttk.Button(tk_frame, text = "12 TOPKNOT", command = lambda: adder(topknot.space * 12, 0, topknot.weight * 12 + 3, 0, 0, "12 Topknot added\n", 0))
tk_12.grid(row = 3, column = 0, sticky = "EW", pady = 3)
tk_16 = ttk.Button(tk_frame, text = "16 TOPKNOT", command = lambda: adder(topknot.space * 16, 0, topknot.weight * 16 + 4, 0, 0, "16 Topknot added\n", 0))
tk_16.grid(row = 4, column = 0, sticky = "EW", pady = 3)

#fs_frame buttons
fs_6 = ttk.Button(fs_frame, text = "6 FOURSEAM", command = lambda: adder(fourseam.space * 3, 0, fourseam.weight * 3 + 1, 0, 0, "6 Fourseam added\n", 0))
fs_6.grid(row = 1, column = 0, sticky = "EW")
fs_12 = ttk.Button(fs_frame, text = "12 FOURSEAM", command = lambda: adder(fourseam.space * 6, 0, fourseam.weight * 6 + 2, 0, 0, "12 Fourseam added\n", 0))
fs_12.grid(row = 2, column = 0, sticky = "EW")
fs_18 = ttk.Button(fs_frame, text = "18 FOURSEAM", command = lambda: adder(fourseam.space * 9, 0, fourseam.weight * 9 + 3, 0, 0, "18 Fourseam added\n", 0))
fs_18.grid(row = 3, column = 0, sticky = "EW")

#gb1_frame buttons
saucy_maui = ttk.Button(gb1_frame, text = "SAUCY (SINGLE SAUCE)", command = lambda: adder(0, 1.24, 30.50, 4.00, 0, "Saucy Box (Single Sauce) added\n", 9))
saucy_maui.grid(row = 1, column = 0, sticky = "EW")
saucy_combo = ttk.Button(gb1_frame, text = "SAUCY (COMBO PACK)", command = lambda: adder(0, 1.60, 48.50, 4.00, 0, "Saucy Box (Combo Pack) added\n", 9))
saucy_combo.grid(row = 2, column = 0, sticky = "EW")
lucky = ttk.Button(gb1_frame, text = "YOU LUCKED OUT BOX", command = lambda: adder(0, 2.12, 36.00, 4.00, 0, "You Lucked Out Box added\n", 9))
lucky.grid(row = 3, column = 0, sticky = "EW")
love_pieces = ttk.Button(gb1_frame, text = "LOVE YOU TO PIECES BOX", command = lambda: adder(0, 1.50, 39.50, 4.00, 0, "Love You to Pieces Box added\n", 9))
love_pieces.grid(row = 4, column = 0, sticky = "EW")
everyday_super = ttk.Button(gb1_frame, text = "EVERYDAY HOLIDAY SUPER", command = lambda: adder(0, 1.56, 30.50, 4.00, 0, "Everyday Holiday Super Box added\n", 9))
everyday_super.grid(row = 5, column = 0, sticky = "EW")
everyday_ultra = ttk.Button(gb1_frame, text = "EVERYDAY HOLIDAY ULTRA", command = lambda: adder(0, 2.74, 63.00, 6.00, 0, "Everyday Holiday Ultra Box added\n", 10))
everyday_ultra.grid(row = 6, column = 0, sticky = "EW")
everyday_mega = ttk.Button(gb1_frame, text = "EVERYDAY HOLIDAY MEGA", command = lambda: adder(0, 4.91, 113.50, 8.00, 0, "Everyday Holiday Mega Box added\n", 12))
everyday_mega.grid(row = 7, column = 0, sticky = "EW")


#gb2_frame buttons
'''These add to gift_box_space instead of space in the adder function so that the space can be substracted
in case of there being more than one gift box, since the gift box IF statement handles package_size
separately.  If they are in a 12x4, gift_box_code sent to adder is 1.00, if in a 12x6, it's 1.10. This
allows different package_size calculations depending on how many gift boxes of each size are in the order.'''
love = ttk.Button(gb2_frame, text = "LOVE BOX", command = lambda: adder(0, 1.40, 21.00, 4.00, 0, "Love Box added\n", 9))
love.grid(row = 1, column = 0, sticky = "EW")
truelove = ttk.Button(gb2_frame, text = "TRUE LOVE BOX", command = lambda: adder(0, 2.68, 44.00, 6.00, 0, "True Love Box added\n", 10))
truelove.grid(row = 2, column = 0, sticky = "EW")
oprah = ttk.Button(gb2_frame, text = "GOURMET PRETZEL BOX", command = lambda: adder(0, 2.06, 41.00, 4.00, 0, "Gourmet Pretzel Box added\n", 9))
oprah.grid(row = 3, column = 0, sticky = "EW")
waffle_box = ttk.Button(gb2_frame, text = "GOURMET BELGIAN WAFFLE BOX", command = lambda: adder(0, 1.43, 45.60, 4.00, 0, "Gourmet Belgian Waffle Box added\n", 9))
waffle_box.grid(row = 4, column = 0, sticky = "EW")
pretzel_waffle = ttk.Button(gb2_frame, text = "GOURMET PRETZEL & WAFFLE BOX", command = lambda: adder(0, 2.02, 49.80, 4.00, 0, "Gourmet Pretzel & Waffle Box added\n", 9))
pretzel_waffle.grid(row = 5, column = 0, sticky = "EW")
holly_jolly = ttk.Button(gb2_frame, text = "HOLLY & JOLLY", command = lambda: adder(0, 1.56, 30.50, 4.00, 0, "Holly & Jolly Box added\n", 9))
holly_jolly.grid(row = 6, column = 0, sticky = "EW")
comfort_joy = ttk.Button(gb2_frame, text = "COMFORT & JOY", command = lambda: adder(0, 2.74, 62.00, 6.00, 0, "Comfort & Joy Box added\n", 10))
comfort_joy.grid(row = 7, column = 0, sticky = "EW")
merrier = ttk.Button(gb2_frame, text = "MORE THE MERRIER", command = lambda: adder(0, 4.97, 113.50, 8.00, 0, "More the Merrier Box added\n", 12))
merrier.grid(row = 8, column = 0, sticky = "EW")

#gb3_frame buttons
'''These add to gift_box_space instead of space in the adder function so that the space can be substracted
in case of there being more than one gift box, since the gift box IF statement handles package_size
separately.  If they are in a 12x4, gift_box_code sent to adder is 1.00, if in a 12x6, it's 1.10. This
allows different package_size calculations depending on how many gift boxes of each size are in the order.'''
knead_love = ttk.Button(gb3_frame, text = "ALL YOU KNEAD IS LOVE BOX", command = lambda: adder(0, 2.62, 51.00, 6.00, 0, "All You Knead is Love Box added\n", 10))
knead_love.grid(row = 1, column = 0, sticky = "EW")
brunch = ttk.Button(gb3_frame, text = "LET'S BRUNCH BOX", command = lambda: adder(0, 1.85, 33.50, 4.00, 0, "Let's Brunch Box added\n", 9))
brunch.grid(row = 2, column = 0, sticky = "EW")
movie_night = ttk.Button(gb3_frame, text = "MOVIE NIGHT BOX", command = lambda: adder(0, 1.74, 39.50, 4.00, 0, "Movie Night Box added\n", 9))
movie_night.grid(row = 3, column = 0, sticky = "EW")
bbq_box = ttk.Button(gb3_frame, text = "BBQ BOX", command = lambda: adder(0, 2.14, 37.00, 4.00, 0, "BBQ Box added\n", 9))
bbq_box.grid(row = 4, column = 0, sticky = "EW")
jude = ttk.Button(gb3_frame, text = "ST. JUDE BOX", command = lambda: adder(0, 2.06, 40.50, 4.00, 0, "St. Jude Box added\n", 9))
jude.grid(row = 5, column = 0, sticky = "EW")
gameday = ttk.Button(gb3_frame, text = "GAME DAY BOX", command = lambda: adder(0, 1.56, 36.00, 4.00, 0, "Game Day Box added\n", 9))
gameday.grid(row = 6, column = 0, sticky = "EW")
cancer = ttk.Button(gb3_frame, text = "CANCER AWARENESS BOX", command = lambda: adder(0, 2.06, 40.50, 4.00, 0, "Cancer Awareness Box added\n", 9))
cancer.grid(row = 7, column = 0, sticky = "EW")

#salt_frame buttons
salt_sugar = ttk.Button(salt_frame, text = "SALTS / SUGARS / TOPPERS", command = lambda: adder(salt.space, 0, salt.weight, 0, 0, "Salt / Sugar / Topper added\n", 0))
salt_sugar.grid(row = 1, column = 0, sticky = "EW")
salt_combo = ttk.Button(salt_frame, text = "GOURMET SALT COMBO", command = lambda: adder(salt.space * 5, 0, salt.weight * 5, 0, 0, "Gourmet Salt Combo added\n", 0))
salt_combo.grid(row = 2, column = 0, sticky = "EW")
sugar_combo = ttk.Button(salt_frame, text = "GOURMET SUGAR COMBO", command = lambda: adder(salt.space * 3, 0, salt.weight * 3, 0, 0, "Gourmet Sugar Combo added\n", 0))
sugar_combo.grid(row = 3, column = 0, sticky = "EW")

#mustard_frame buttons
sauce = ttk.Button(mustard_frame, text = "SAUCE / MUSTARD", command = lambda: adder(mustard.space, 0, mustard.weight, 0, 0, "Sauce / Mustard added\n", 0))
sauce.grid(row = 1, column = 0, sticky = "EW", pady = 3)
sauce = ttk.Button(mustard_frame, text = "GOURMET SAUCE COMBO", command = lambda: adder(mustard.space * 3, 0, mustard.weight * 3, 0, 0, "Gourmet Sauce Combo added\n", 0))
sauce.grid(row = 2, column = 0, sticky = "EW", pady = 3)

#waffle_frame buttons
waffle_single = ttk.Button(waffle_frame, text = "1 WAFFLE", command = lambda: adder(waffle.space * 1, 0, waffle.weight * 1, 0, 0, "1 Waffle added\n", 0))
waffle_single.grid(row = 1, column = 0, sticky = "EW")
waffle_6 = ttk.Button(waffle_frame, text = "6 WAFFLES", command = lambda: adder(waffle.space * 6, 0, waffle.weight * 6, 0, 0, "6 Waffles added\n", 0))
waffle_6.grid(row = 2, column = 0, sticky = "EW")
waffle_12 = ttk.Button(waffle_frame, text = "12 WAFFLES", command = lambda: adder(waffle.space * 12, 0, waffle.weight * 12, 0, 0, "12 Waffles added\n", 0))
waffle_12.grid(row = 3, column = 0, sticky = "EW")

root.mainloop()