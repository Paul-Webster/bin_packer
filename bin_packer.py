'''
bin_packer.py
Python 2.7/Eclipse Neon 2.2

Algorithm Overview:
    Partition a list of bin items into a sublist of bins whose unit height sums
    don't exceed a maximum value of bin_size (number of containable elements).
    Allow for bin containers of various sizes and the sorting of bin container
    items.

Algorithm Semantics:
    # Specify the list of bin containers sizes.
    bin_sizes = [ 29, 30, 30, 30, 30 ]
    # Determine the number of required bin containers.
    bin_count = BinManager.compute_bin_count(values, bin_sizes)
    # Allocate the bin containers.
    bin_list = [ BinContainer(i, bin_sizes[i]) for i in range(bin_count) ]
    # Split the input list by size.
    value_sets = BinManager.split_values_by_size(values, large_items_at_top)
    # Add items to bin containers;
        # Option 1 - First Fit sequential order.
        # Option 2 - Distribute items evenly amongst bin containers.

Inputs:
    bin_sizes - List of bin container sizes.
    large_items_at_top - Place larger bin items to the top of each bin container (True/False)
    bin_items = List of bin items which may vary in size (1U/2U, etc ...).

Examples:
    Bins = BinManager.order_sequentially(bin_items, bin_sizes)
    BinManager.show("Bin contents", Bins)

    Bins = BinManager.evenly_distribute(bin_items, bin_sizes)
    BinManager.show("Bin contents", Bins)
'''


################################################################################
# BinItem - Bin item abstraction class.
###############################################################################
class BinItem(int):

    ############################################################################
    # Create a bin element with the specified unit height.
    ############################################################################
    def __init__(self, unit_height=1):
        self.unit_height = unit_height

    ############################################################################
    # str() - Printable representation.
    ############################################################################
    def __str__(self):
        return 'BinItem(unit_height=%d)' % self.unit_height


################################################################################
# Bin - Class which holds bin items.
###############################################################################
class BinContainer(object):

    ############################################################################
    # Container for bin items that holds a running sum.
    ############################################################################
    def __init__(self, index, size):
        self.index = index
        self.size = size
        self.count = 0
        self.items = []

    ############################################################################
    # append() - Add an element to this container.
    ############################################################################
    def append(self, item):
        self.items.append(item)
        self.count += item

    ############################################################################
    # str() - Printable representation.
    ############################################################################
    def __str__(self):
        return 'Bin(index=%s size=%s, count=%d, unused=%d, items=%s)' % \
            (self.index, self.size, self.count, self.size - self.count, str(self.items))


################################################################################
# BinManager - Static bin packer helper class
################################################################################
class BinManager():            
    
    debug = False
    ########################################################################
    # compute_bin_count() - Compute the number of required bin containers.
    ########################################################################        
    
    @staticmethod
    def compute_bin_count(bin_items, bin_sizes):
        print ('========================[ packing bins ]========================')
        unit_height_sum = sum(bin_items)
        bin_count = 0
        container_sum = 0
        while (container_sum < unit_height_sum):
            container_sum += bin_sizes[bin_count]
            bin_count += 1
        print ('A total of', unit_height_sum, 'unit height sizes requires at least', bin_count, 'bin containers.')
        return bin_count 
    
    ############################################################################
    # split_values_by_size() - Split the input list by sizing values.
    ############################################################################
    
    @staticmethod
    def split_values_by_size(values, large_values_first):
        sets = []
        if len(values) < 1:
            return sets
        ary = []
        sets.append(ary)
        sorted_list = sorted(values, reverse=large_values_first)
        val = sorted_list[0]    
        for item in sorted_list:
            if val == item:
                ary.append(item)
            else:
                ary = []
                ary.append(item)
                sets.append(ary)
                val = item
                
        return sets
    
    ############################################################################
    # can_add_to_bin() - Determine if an item can be added to a bin container.
    ############################################################################
    
    @staticmethod
    def can_add_to_bin(bin_container, item):
        bin_size = bin_container.size
        if bin_container.count + item <= bin_size:
            return True
        return False
    
    ############################################################################
    # order_sequentially() - Pack bin items into a Bin (order sequentially).
    ############################################################################
    
    @staticmethod
    def order_sequentially(values, bin_sizes, large_items_at_top=False):
        # Determine the number of required bin containers.
        bin_count = BinManager.compute_bin_count(values, bin_sizes)
        # Allocate the bin containers.
        bin_list = [ BinContainer(i, bin_sizes[i]) for i in range(bin_count) ]
        # Split the input list by size values.
        value_sets = BinManager.split_values_by_size(values, large_items_at_top)
        # Add items to containers.
        cidx = 0
        for value_set in value_sets:
            for item in value_set:
                if BinManager.can_add_to_bin(bin_list[cidx], item):
                    bin_list[cidx].append(item)
                    if BinManager.debug:
                        print ('Adding', item, 'to', bin_list[cidx])
                else:
                    cidx += 1
                    bin_list[cidx].append(item)
                    if BinManager.debug:
                        print ('Adding', item, 'to', bin_list[cidx])
        
        return bin_list
    
    ############################################################################
    # evenly_distribute() - Pack bin items into a Bin (evenly distribute).
    ############################################################################
    
    @staticmethod
    def evenly_distribute(values, bin_sizes, large_items_at_top=False):
        # Determine the number of required bin containers.
        bin_count = BinManager.compute_bin_count(values, bin_sizes)
        # Allocate the bin containers.
        bin_list = [ BinContainer(i, bin_sizes[i]) for i in range(bin_count) ]
        # Split the input list by size values.
        value_sets = BinManager.split_values_by_size(values, large_items_at_top)
        # EVenly distribute items across containers.
        cidx = 0
        nidx = 0
        for value_set in value_sets:
            for item in value_set:
                cidx = nidx % bin_count
                if BinManager.can_add_to_bin(bin_list[cidx], item):
                    bin_list[cidx].append(item)
                    if BinManager.debug:
                        print ('Adding', item, 'to', bin_list[cidx])
                else:
                    print ('ERROR : Container overflow -', \
                        'Item does not fit specified container constraints', \
                        ': Item skipped !!!', item, 'on', bin_list[cidx])
                nidx += 1
        
        return bin_list
    
    ############################################################################
    # show() - Show the contents of all bins.
    ############################################################################
    
    @staticmethod
    def show(msg, bins):
        print ('==========================[ results ]===========================')
        print (msg)
        print ('Packing solution requires %d bin containers' % len(Bins))
        print ("++++[ container results ]++++")
        for bin_container in bins:
            print (bin_container)
        print ('===============================================================\n')    


################################################################################
# main - Program main line
################################################################################
if __name__ == '__main__':
    import random
    
    ############################################################################
    # Case #1:
    ############################################################################
    bin_sizes = [ 30 ]
    msg = 'Simple Case: 3 bin items - 2/1U in height, 1/2U in height.\n' + \
            'bin sizes: ' + str(bin_sizes) + '\n' + \
            'Larger items placed at the top of each bin.\n' + \
            'Bins will be filled in sequential order.'
    large_items_at_top = True
    bin_items = [ BinItem(1), BinItem(2), BinItem(1) ]
    Bins = BinManager.order_sequentially(bin_items, bin_sizes, large_items_at_top)
    BinManager.show(msg, Bins)
    
    ############################################################################
    # Case #2:
    ############################################################################
    bin_sizes = [ 34, 34, 34 ]
    msg = 'Random Case: 45 bin items - random(1, 2) in height.\n' + \
            'bin sizes: ' + str(bin_sizes) + '\n' + \
            'Larger items placed at the bottom of each bin.\n' + \
            'Bin items evenly distributed amongst bin containers.'
    large_items_at_top = False
    bin_items = [ BinItem(random.randint(1, 2)) for i in range(45) ]
    Bins = BinManager.evenly_distribute(bin_items, bin_sizes, large_items_at_top)
    BinManager.show(msg, Bins)    
    
    """
    You have 45 items that are 1 unit high, 36 items that are 2 units high.
    Please provide an algorithm that will in both cases distribute the items
    evenly across bins that can hold no more than 30 units of height.
    """
    ###########################################################################
    # Case #3:
    ############################################################################
    bin_sizes = [ 30, 30, 30, 30 ]
    msg = 'Implementation Requirement #1:\n' + \
            '45/1U bin items, 36/2U bin items.\n' + \
            'bin sizes: ' + str(bin_sizes) + '\n' + \
            'Larger units placed at the bottom of each bin.\n' + \
            'Bin items evenly distributed amongst bin containers.'
    large_items_at_top = False
    bin_items = [ BinItem(1) for i in range(45) ]
    for i in range(36):
        bin_items.append(BinItem(2))
    Bins = BinManager.evenly_distribute(bin_items, bin_sizes, large_items_at_top)
    BinManager.show(msg, Bins)
    """
    In another case, you have 57 items that are 1 unit high and 38 units that
    are each 2 units high.
    Please provide an algorithm that will in both cases distribute the items
    evenly across bins that can hold no more than 30 units of height.
    """    
    ###########################################################################
    # Case #4:
    ############################################################################
    bin_sizes = [ 30, 30, 30, 30, 30 ]
    msg = 'Implementation Requirement #2:\n' + \
            '57/1U bin items, 38/2U bin items.\n' + \
            'bin sizes: ' + str(bin_sizes) + '\n' + \
            'Larger units placed at the bottom of each bin.\n' + \
            'Bin items evenly distributed amongst bin containers.'
    large_items_at_top = False
    bin_items = [ BinItem(1) for i in range(57) ]
    for i in range(38):
        bin_items.append(BinItem(2))
    Bins = BinManager.evenly_distribute(bin_items, bin_sizes, large_items_at_top)
    BinManager.show(msg, Bins)
    """
    Explain how you will handle the odd item.
    How does your algorithm change if the first bin can take only 29 units of
    height, and all subsequent bins have a capacity of 30 units.
        Please refer to the provided Bin container printouts.
    """
    ###########################################################################
    # Case #4:
    ############################################################################
    bin_sizes = [ 29, 30, 30, 30, 30 ]
    msg = 'Implementation Requirement #3:\n' + \
            '57/1U bin items, 38/2U bin items.\n' + \
            'bin sizes: ' + str(bin_sizes) + '\n' + \
            'Larger units placed at the bottom of each bin.\n' + \
            'Bin items evenly distributed amongst bin containers.'
    large_items_at_top = False
    bin_items = [ BinItem(1) for i in range(57) ]
    for i in range(38):
        bin_items.append(BinItem(2))
    Bins = BinManager.evenly_distribute(bin_items, bin_sizes, large_items_at_top)
    BinManager.show(msg, Bins)
    ###########################################################################
    # Case #5:
    ############################################################################
    print ("INTENTIONAL TEST of container overflow situations")
    bin_sizes = [ 2, 40, 40, 40, 40 ]
    msg = 'INTENTIONAL TEST of container overflow situations:\n' + \
            '57/1U bin items, 38/2U bin items.\n' + \
            'bin sizes: ' + str(bin_sizes) + '\n' + \
            'Larger units placed at the bottom of each bin.\n' + \
            'Bin items evenly distributed amongst bin containers.'
    large_items_at_top = False
    bin_items = [ BinItem(1) for i in range(57) ]
    for i in range(38):
        bin_items.append(BinItem(2))
    Bins = BinManager.evenly_distribute(bin_items, bin_sizes, large_items_at_top)
    BinManager.show(msg, Bins)
    print ("NOTE : This solution could dynamically adapt for the above overflow conditions")
    print ("       Errors are shown for purposes of demonstration.")
