from __future__ import division

class Slicer:
    def __init__(self, array_like, stride=1, width=1, eatup=True):
        self.array_like = array_like
        self.stride = stride
        self.width = width
        self.index = 0
        self.sliced = None
        if eatup:
            self.length = ((len(array_like) + stride - 1) // stride)
        else:
            self.length = (len(array_like) - width) // stride + 1
        return None

    def __iter__(self):
        return self

    def __next__(self):
        if self.length == self.index:
            raise StopIteration()
        if self.sliced is not None:
            fragment = self.sliced[self.index]
        else:
            head_index = self.stride * self.index
            tail_index = head_index + self.width
            fragment = self.array_like[head_index:tail_index]
        self.index += 1
        return fragment

    def __len__(self):
        return self.length - self.index

    def __bool__(self):
        return True

    def __getitem__(self, key):
        key_type = type(key)
        if key_type in [int, slice]:
            if self.sliced is None:
                index = self.index
                self.sliced = list(self)
                self.index = index
            return self.sliced[key]
        raise KeyError

    def rewind(self):
        self.index = 0
        return None

if __name__ == "__main__":
    import unittest
    class TestSlicer(unittest.TestCase):
        def test_length(self):
            self.assertEqual(len(Slicer([0,1,2,3,4], 2, 3)), 3)
            self.assertEqual(len(Slicer([0,1,2,3,4], 2, 3, False)), 2)
        def test_indexing(self):
            instance = Slicer([0,1,2,3,4], 2, 3)
            self.assertEqual(instance[0], [0,1,2])
            self.assertEqual(instance[1], [2,3,4])
            self.assertEqual(instance[2], [4])
            self.assertEqual(instance[-1], [4])
            self.assertEqual(instance[-2], [2,3,4])
            with self.assertRaises(IndexError):
                print(len(instance))
                instance[len(instance) + 1]
            with self.assertRaises(KeyError):
                instance["a"]
        def test_slice_indexing(self):
            instance = Slicer([0,1,2,3,4], 2, 3)
            self.assertEqual(instance[0:1], [[0,1,2]])
            self.assertEqual(instance[:1], [[0,1,2]])
            self.assertEqual(instance[2:3], [[4]])
            self.assertEqual(instance[2:], [[4]])
            self.assertEqual(instance[0::2], [[0,1,2],[4]])
            with self.assertRaises(ValueError):
                instance[0:1:0]
        def test_iteration(self):
            instance = Slicer([0,1,2,3,4], 2, 3)
            self.assertEqual(len(instance), 3)
            self.assertEqual(instance.__next__(), [0,1,2])
            self.assertEqual(len(instance), 2)
            self.assertEqual(instance.__next__(), [2,3,4])
            self.assertEqual(len(instance), 1)
            self.assertEqual(instance.__next__(), [4])
            self.assertEqual(len(instance), 0)
            with self.assertRaises(StopIteration):
                instance.__next__()
            instance.rewind()
            self.assertEqual(len(instance), 3)
            self.assertEqual(instance.__next__(), [0,1,2])

    unittest.main()
    exit()
