from pyglet import window
import moderngl

class Application(window.Window):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.context = moderngl.create_context()
		print(self.context)