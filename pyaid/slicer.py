from __future__ import division

class slicer:
    def __init__(self, array_like, stride=1, width=1, eatup=True):
        self.array_like = array_like
        self.stride = stride
        self.width = width
        self.index = 0
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
        if key_type is int:
            if key < 0 or self.length <= key:
                raise IndexError
            head_index = self.stride * key
            tail_index = head_index + self.width
            fragment = self.array_like[head_index:tail_index]
            return fragment
        if key_type is slice:
            head = 0 if key.start is None else key.start
            tail = self.length if key.stop is None else key.stop
            step = 1 if key.step is None else key.step
            if step == 0:
                raise ValueError("slice step cannot be zero")
            if step < 0:
                head, tail = tail-1, head-1
            return [
                self.array_like[self.stride * i:self.stride * i + self.width]
                for i in range(head, tail, step)
            ]

if __name__ == "__main__":
    import unittest
    class TestSlicer(unittest.TestCase):
        def test_length(self):
            self.assertEqual(len(slicer([0,1,2,3,4], 2, 3)), 3)
            self.assertEqual(len(slicer([0,1,2,3,4], 2, 3, False)), 2)
        def test_indexing(self):
            instance = slicer([0,1,2,3,4], 2, 3)
            self.assertEqual(instance[0], [0,1,2])
            self.assertEqual(instance[1], [2,3,4])
            self.assertEqual(instance[2], [4])
            with self.assertRaises(IndexError):
                instance[-1]
            with self.assertRaises(IndexError):
                instance[-1]
            with self.assertRaises(IndexError):
                instance[len(instance) + 1]
        def test_slice_indexing(self):
            instance = slicer([0,1,2,3,4], 2, 3)
            self.assertEqual(instance[0:1], [[0,1,2]])
            self.assertEqual(instance[:1], [[0,1,2]])
            self.assertEqual(instance[2:3], [[4]])
            self.assertEqual(instance[2:], [[4]])
            self.assertEqual(instance[0::2], [[0,1,2],[4]])
            self.assertEqual(instance[0:1:-1], [[0,1,2]])
            self.assertEqual(instance[2:3:-1], [[4]])
            with self.assertRaises(ValueError):
                instance[0:1:0]
        def test_iteration(self):
            instance = slicer([0,1,2,3,4], 2, 3)
            self.assertEqual(len(instance), 3)
            self.assertEqual(instance.__next__(), [0,1,2])
            self.assertEqual(len(instance), 2)
            self.assertEqual(instance.__next__(), [2,3,4])
            self.assertEqual(len(instance), 1)
            self.assertEqual(instance.__next__(), [4])
            self.assertEqual(len(instance), 0)
            with self.assertRaises(StopIteration):
                self.assertEqual(instance.__next__(), [])
    unittest.main()
    exit()
