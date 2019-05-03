from Camera import Camera
from Calibration import CalibrationGrid


class Model:

	def __init__(self):
		self.camera = Camera()
		self.grid = None
		self.row_spacing = None
		self.col_spacing = None
		self.pos_list = None
		self.pos = None

	def UpdateCalibrationSettings(self, row_spacing, col_spacing):
		self.row_spacing = row_spacing
		self.col_spacing = col_spacing
		self.grid = self.CreateCalibrationGrid()
		self.UpdatePositionList()
		self.pos = 0

	def CreateCalibrationGrid(self):
		frame = self.camera.get_frame()
		height, width = frame.shape[:2]
		return CalibrationGrid(
			row_spacing = self.row_spacing,
			col_spacing = self.col_spacing,
			height = height, 
			width = width
		)

	def CurrentPoint(self):
		if self.pos is None:
			return None
		row = self.pos_list[self.pos][0]
		col = self.pos_list[self.pos][1]
		return self.grid.Cell(row, col)

	def NextPoint(self):
		if self.pos < len(self.pos_list) - 1:
			self.pos += 1

	def PreviousPoint(self):
		if self.pos > 0:
			self.pos -= 1

	def GetGrid(self):
		return self.grid

	def GetCameraFeed(self):
		return self.camera.get_frame()

	def IsSelected(self, row, col):
		if self.pos is None:
			return False
		return self.pos_list[self.pos] == (row, col)

	def UpdatePositionList(self):
		self.pos_list = []
		for i in range(self.grid.NumRows()):
			for j in range(self.grid.NumCols()):
				self.pos_list.append((i, j))