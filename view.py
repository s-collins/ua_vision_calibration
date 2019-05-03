import cv2
import tkinter as tk
from PIL import Image, ImageTk


class View():

	REFRESH_RATE = 50

	def __init__(self):
		self.frame = tk.Tk()
		self.frame.title('Calibration Grid Maker')
		self.controller = None

		# variables
		self.var_rowPixelValue = tk.StringVar()
		self.var_colPixelValue = tk.StringVar()
		self.var_worldXCoordinateValue = tk.StringVar()
		self.var_worldYCoordinateValue = tk.StringVar()

		# create widgets
		self.lbl_RowSpacing = tk.Label(self.frame, text='Row Spacing (pixels):')
		self.lbl_ColSpacing = tk.Label(self.frame, text='Column Spacing (pixels):')
		self.entry_RowSpacing = tk.Entry(self.frame)
		self.entry_ColSpacing = tk.Entry(self.frame)
		self.btn_Refresh = tk.Button(self.frame, text='Refresh Settings')

		self.feed = tk.Label(self.frame)

		self.lbl_rowPixel = tk.Label(self.frame, text='Row Pixel')
		self.lbl_colPixel = tk.Label(self.frame, text='Col Pixel')
		self.lbl_worldXCoordinate = tk.Label(self.frame, text='World X Coordinate (cm):')
		self.lbl_worldYCoordinate = tk.Label(self.frame, text='World Y Coordinate (cm):')

		self.lbl_rowPixelValue = tk.Label(self.frame, textvariable=self.var_rowPixelValue)
		self.lbl_colPixelValue = tk.Label(self.frame, textvariable=self.var_colPixelValue)
		self.lbl_worldXCoordinateValue = tk.Label(self.frame, textvariable=self.var_worldXCoordinateValue)
		self.lbl_worldYCoordinateValue = tk.Label(self.frame, textvariable=self.var_worldYCoordinateValue)

		self.lbl_newXCoordinate = tk.Label(self.frame, text='New X Coordinate (cm):')
		self.lbl_newYCoordinate = tk.Label(self.frame, text='New Y Coordinate (cm):')
		self.entry_newXCoordinate = tk.Entry(self.frame)
		self.entry_newYCoordinate = tk.Entry(self.frame)
		self.btn_Save = tk.Button(self.frame, text='Save Point')
		self.btn_Previous = tk.Button(self.frame, text='Previous Point')
		self.btn_Next = tk.Button(self.frame, text='Next Point')

		# layout widgets
		self.lbl_RowSpacing.grid(row=0, column=0, sticky='e')
		self.lbl_ColSpacing.grid(row=1, column=0, sticky='e')
		self.entry_RowSpacing.grid(row=0, column=1, sticky='we')
		self.entry_ColSpacing.grid(row=1, column=1, sticky='we')
		self.btn_Refresh.grid(row=2, column=0, columnspan=2, sticky='we')

		self.feed.grid(row=3, column=0, columnspan=2)

		self.lbl_rowPixel.grid(row=4, column=0, sticky='e')
		self.lbl_colPixel.grid(row=5, column=0, sticky='e')
		self.lbl_worldXCoordinate.grid(row=6, column=0, sticky='e')
		self.lbl_worldYCoordinate.grid(row=7, column=0, sticky='e')

		self.lbl_rowPixelValue.grid(row=4, column=1)
		self.lbl_colPixelValue.grid(row=5, column=1)
		self.lbl_worldXCoordinateValue.grid(row=6, column=1)
		self.lbl_worldYCoordinateValue.grid(row=7, column=1)

		self.lbl_newXCoordinate.grid(row=8, column=0, sticky='e')
		self.lbl_newYCoordinate.grid(row=9, column=0, sticky='e')
		self.entry_newXCoordinate.grid(row=8, column=1, sticky='we')
		self.entry_newYCoordinate.grid(row=9, column=1, sticky='we')
		self.btn_Save.grid(row=10, column=0, columnspan=2, sticky='we')
		self.btn_Previous.grid(row=11, column=0, sticky='we')
		self.btn_Next.grid(row=11, column=1, sticky='we')

		# menu
		self.menu = tk.Menu(self.frame)
		self.file_menu = tk.Menu(self.menu)
		self.menu.add_cascade(label='file', menu=self.file_menu)
		self.frame.config(menu=self.menu)

	def SetController(self, controller):
		self.controller = controller

		# wire the callbacks
		self.btn_Refresh.config(command=self.controller.RefreshCalibrationSettings)
		self.btn_Previous.config(command=self.controller.PreviousPoint)
		self.btn_Next.config(command=self.controller.NextPoint)
		self.btn_Save.config(command=self.controller.SavePoint)
		self.file_menu.add_command(label='Save Calibration Grid', command=self.controller.SaveGrid)

	def GetRowSpacingEntry(self):
		return self.entry_RowSpacing.get()

	def GetColSpacingEntry(self):
		return self.entry_ColSpacing.get()

	def GetWorldXEntry(self):
		return self.entry_newXCoordinate.get()

	def GetWorldYEntry(self):
		return self.entry_newYCoordinate.get()

	def SetImage(self, image):
		im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		im = Image.fromarray(im)
		im = ImageTk.PhotoImage(im)
		self.feed.configure(image=im)
		self.feed.image = im

	def SetPointValues(self, row_pixel, col_pixel, world_x, world_y):
		self.var_rowPixelValue.set(str(row_pixel))
		self.var_colPixelValue.set(str(col_pixel))
		self.var_worldXCoordinateValue.set(str(world_x))
		self.var_worldYCoordinateValue.set(str(world_y))

	def Show(self):
		self.frame.after(self.REFRESH_RATE, self.controller.Refresh)
		self.frame.mainloop()


