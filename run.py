import view
import controller
import model

if __name__ == '__main__':
	model = model.Model()
	controller = controller.Controller()
	view = view.View()

	controller.SetModel(model)
	controller.SetView(view)

	view.SetController(controller)

	view.Show()
