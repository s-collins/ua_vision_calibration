class CalibrationPoint:

	def __init__(self, row_pixel=None, col_pixel=None):
		"""
		Default constructs a calibration point.
		"""
		self.row_pixel = row_pixel
		self.col_pixel = col_pixel
		self.x_world_coord = None
		self.y_world_coord = None

	def RowPixel(self):
		return self.row_pixel

	def ColPixel(self):
		return self.col_pixel

	def WorldXCoord(self):
		return self.x_world_coord

	def WorldYCoord(self):
		return self.y_world_coord

	def SetWorldCoordinates(self, x, y):
		self.x_world_coord = x
		self.y_world_coord = y


class CalibrationGrid:

	def __init__(self, row_spacing, col_spacing, height, width):
		"""
		Constructs a matrix of calibration points.

		Parameters:
		 - row_spacing: number of pixels between each row
		 - col_spacing: number of pixels between each column
		 - height:      image height in pixels
		 - width:       image width in pixels
		"""
		self.matrix = []
		self.height = height
		self.width = width

		row_pixel = 0
		row_flag = True
		while (row_flag):
			self.matrix.append([])
			col_pixel = 0
			col_flag = True
			while (col_flag):
				self.matrix[-1].append(CalibrationPoint(row_pixel, col_pixel))
				col_pixel, col_flag = self.__update_index(col_pixel, col_spacing, width)
			row_pixel, row_flag = self.__update_index(row_pixel, row_spacing, height)

	def Cell(self, row, col):
		return self.matrix[row][col]

	def NumRows(self):
		return len(self.matrix)

	def NumCols(self):
		return len(self.matrix[0])

	def __update_index(self, index, step, max_index):
		flag = True
		if index == max_index:
			flag = False
		else:
			index += step
			if index > max_index:
				index = max_index
		return (index, flag)
