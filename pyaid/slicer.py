from __future__ import division

class slicer:
    def __init__(self, array_like, stride=1, width=1, eatup=True):
        self.array_like = array_like
        self.stride = stride
        self.width = width
        self.eatup = eatup

    def __iter__(self):
        return self

    def __next__(self):
        if self.eatup == True:
            if len(self.array_like) < self.width:
                raise StopIteration()
        else:
            if len(self.array_like) == 0:
                raise StopIteration()
        fragment = self.array_like[:self.width]
        self.array_like = self.array_like[self.stride:]
        return fragment

    def __len__(self):
        return 1


if __name__ == "__main__":
    a = [0,1,2,3,4,5,6,7,8,9]
    for v in slicer(a, 1,5):
        print(v)

    print(len(slicer(a, 1,4)))
    exit()
