def chooseBrickSet(choice, colsWhole, rowsWhole):
    defaultList = [(rowsWhole-5, 0), (rowsWhole-1, 2), (rowsWhole-2, 3), (rowsWhole-7, 4),
        (rowsWhole-8, 4), (rowsWhole-1, 6), (rowsWhole-2, 7), (rowsWhole-3, 8), (rowsWhole-1, 9),
        (rowsWhole-3, 9), (rowsWhole-4, 10), (rowsWhole-2, 11), (rowsWhole-2, 12),
        (rowsWhole-2, 10), (rowsWhole-7, 11), (rowsWhole-11, 11), (rowsWhole-9, 12), (rowsWhole-9, 13), (rowsWhole-8, 14),
        (rowsWhole-8, 15), (rowsWhole-10, 16), (rowsWhole-12, 17), (rowsWhole-15, 18),
        (rowsWhole-8, 19), (rowsWhole-1, 20), (rowsWhole-2, 21), (rowsWhole-3, 22), (rowsWhole-1, 23),]
    if choice == "default":
        return defaultList