import numpy as np
import unittest

class TextComparison:
	
	def __init__(self, s1, s2):
		self.s1 = s1
		self.s2 = s2
		self.dist_arr = None

	def dist(self):

		self.dist_arr = np.zeros((len(self.s1) + 1, len(self.s2) + 1,))
		self.r1 = self.s1[::-1]
		self.r2 = self.s2[::-1]
				
		for count1 in range(len(self.r1) + 1):
			self.dist_arr[count1, 0] = count1

		for count2 in range(len(self.r2) + 1):
			self.dist_arr[0, count2] = count2

		for count1 in range(len(self.r1)):
			for count2 in range(len(self.r2)):
				if self.r1[count1] == self.r2[count2]:
					self.dist_arr[count1 + 1, count2 + 1] = self.dist_arr[count1, count2]
				else:
					min1 = self.dist_arr[count1][count2 + 1] + 1
					min2 = self.dist_arr[count1 + 1][count2] + 1
					min3 = self.dist_arr[count1][count2] + 1
					mini = min(min1, min2, min3)
					self.dist_arr[count1 +1][count2 + 1] = mini

		return self.dist_arr[len(self.r1), len(self.r2)]

	def change(self):

		if self.dist_arr is None:
			self.dist()

		count1 = len(self.r1)
		count2 = len(self.r2)
		cur_val = self.dist_arr[count1, count2]
		stop_count = 0
		change_str = ''

		while (count1 + count2 > 0) & (stop_count < 10000):

			if count1 > 0:
				move_up = self.dist_arr[count1 - 1, count2]
			else:
				move_up = 999
			
			if count2 > 0:
				move_left = self.dist_arr[count1, count2 - 1]
			else:
				move_left = 999

			if (count1 > 0) & (count2 > 0):
				move_diag = self.dist_arr[count1 -1, count2 - 1]
			else:
				move_diag = 999

			min_change = min(move_up, move_left, move_diag) - cur_val	

			if min_change == -1:
				if ((move_left - cur_val) == -1) & (count2 > 0): # moving left
					cur_change_letter = '[' + self.r2[count2 -1] + ']'
					cur_val = move_left
					count2 = count2 - 1
				elif ((move_up - cur_val) == -1) & (count1 > 0): # moving up
					cur_change_letter = '{' + self.r1[count1 - 1] + '}'
					cur_val = move_up
					count1 = count1 - 1
				elif (move_diag - cur_val == -1): # moving diag
					cur_change_letter = '[' + self.r1[count1 - 1] + '-' + self.r2[count2 - 1] + ']'
					cur_val = move_diag
					count1 = count1 - 1
					count2 = count2 - 1
			else: # moving diag - no change
				cur_change_letter = self.r1[count1 - 1]
				cur_val = move_diag
				count1 = count1 - 1
				count2 = count2 - 1

			change_str = change_str + cur_change_letter
			stop_count = stop_count + 1

		return change_str


class TestTextComparison(unittest.TestCase):

	cases = [
		('hello', 'hola', 3.0, 'h{e}[l-o]l[o-a]')
	]

	def test_dist(self):	
		for tc in self.cases:
			text_comp = TextComparison(tc[0], tc[1])
			self.assertEqual(text_comp.dist(), tc[2])

	def test_change(self):	
		for tc in self.cases:
			text_comp = TextComparison(tc[0], tc[1])
			self.assertEqual(text_comp.change(), tc[3])

if __name__ == '__main__':
    unittest.main()
