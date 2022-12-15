import unittest


def partition(array, low, high):
    pivot = high
    left = low
    right = pivot - 1

    while left <= right:
        if array[left] > array[pivot]:
            while array[right] > array[pivot] and left <= right:
                right -= 1

            if right < left:
                break

            array[left], array[right] = array[right], array[left]

        left += 1

    array[left], array[pivot] = array[pivot], array[left]
    return left


def quicksort(array, low=None, high=None):
    low = 0 if low is None else low
    high = len(array) - 1 if high is None else high

    if low < high:
        pivot = partition(array, low, high)
        quicksort(array, low, pivot - 1)
        quicksort(array, pivot + 1, high)


class Test(unittest.TestCase):

    def test_interviewcake(self):
        array = [0, 8, 1, 2, 7, 9, 3, 4]
        quicksort(array)
        self.assertEqual([0, 1, 2, 3, 4, 7, 8, 9], array)
