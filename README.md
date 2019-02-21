# bin_packer
Bin Packer Test Harness

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
    
