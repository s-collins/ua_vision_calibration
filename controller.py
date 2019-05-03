import cv2
import yaml

class Controller:

	def __init__(self):
		self.model = None
		self.view = None

	def SetModel(self, model):
		self.model = model

	def SetView(self, view):
		self.view = view

	def RefreshCalibrationSettings(self):
		row_spacing = self.view.GetRowSpacingEntry()
		col_spacing = self.view.GetColSpacingEntry()
		if row_spacing.isdigit() and col_spacing.isdigit():
			row_spacing = int(row_spacing)
			col_spacing = int(col_spacing)
			self.model.UpdateCalibrationSettings(row_spacing, col_spacing)
		self.RefreshPointInformation()

	def Refresh(self):
		self.RefreshImage()
		self.RefreshPointInformation()

	def RefreshImage(self):
		image = self.model.GetCameraFeed()
		self.DrawGrid(image)
		self.view.SetImage(image)
		self.view.frame.after(self.view.REFRESH_RATE, self.Refresh)

	def RefreshPointInformation(self):
		point = self.model.CurrentPoint()
		if point is not None:
			self.view.SetPointValues(
				row_pixel = point.RowPixel(),
				col_pixel = point.ColPixel(),
				world_x = point.WorldXCoord(),
				world_y = point.WorldYCoord()
			)

	def DrawGrid(self, image):
		selected_color = (255, 0, 0)
		default_color = (0, 0, 255)

		grid = self.model.GetGrid()
		if grid is None:
			return

		for i in range(grid.NumRows()):
			for j in range(grid.NumCols()):
				cell = grid.Cell(i, j)
				center = (cell.ColPixel(), cell.RowPixel())
				color = default_color
				if self.model.IsSelected(i, j):
					color = selected_color
				cv2.circle(image, center, 5, color, 2)

	def PreviousPoint(self):
		self.model.PreviousPoint()

	def NextPoint(self):
		self.model.NextPoint()

	def SavePoint(self):
		point = self.model.CurrentPoint()
		x = self.view.GetWorldXEntry()
		y = self.view.GetWorldYEntry()
		if len(x) > 0 and len(y) > 0:
			point.SetWorldCoordinates(int(x), int(y))

	def SaveGrid(self):
		grid = self.model.GetGrid()
		output_dict = {
			'num_rows': grid.NumRows(),
			'num_cols': grid.NumCols(),
			'points': []
		}
		for i in range(grid.NumRows()):
			for j in range(grid.NumCols()):
				point = grid.Cell(i, j)
				point_dict = {
					'row_pixel': point.RowPixel(),
					'col_pixel': point.ColPixel(),
					'x_cm': point.WorldXCoord(),
					'y_cm': point.WorldYCoord()
				}
				output_dict['points'].append(point_dict)
		with open('calibration_grid.yaml', 'w') as f:
			yaml.dump(output_dict, f)
