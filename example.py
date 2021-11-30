import arcade


class SampleWindow(arcade.Window):

    def __init__(self):
        super().__init__(800, 800, "Isometric Example")
        self.sample_map = arcade.TileMap("resouces/tiled_maps/sample_square.json")


def run():
    window = SampleWindow()
    window.run()
