if __name__ == "__main__":
    import pyaid
    arg = pyaid.argsort([4,5,3,2,7,1])
    print(arg)

    print(list(pyaid.Slicer(arg, 2, 3)))
    exit()
