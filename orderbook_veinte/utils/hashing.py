def generatehash(items:list):
    items = [str(i) for i in items]
    hash = ''
    for i in range(len(items)):
        hash += items[i]
    hash.replace('.' , '')
    return hash