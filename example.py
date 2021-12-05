import arcade

from isometric import isomap


class SampleWindow(arcade.Window):

    def __init__(self):
        super().__init__(900, 900, "Isometric Example")
        self.sample_map = isomap.IsoTileMap("resouces/tiled_maps/sample_square.json", scaling=0.2)

        arcade.set_viewport(-450, 450, -450, 450)

    def on_draw(self):
        for layer in self.sample_map.sprite_lists.values():
            layer.draw()


def run():
    window = SampleWindow()
    window.run()
