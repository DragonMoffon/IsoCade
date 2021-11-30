import math
from typing import TYPE_CHECKING

import arcade
if TYPE_CHECKING:
    from arcade import Texture, TextureAtlas


def to_isometric_square(tile_x: int, tile_y: int, map_size: tuple[int, int], tile_size: tuple[int, int]):
    """
    Helper function which takes a x and y tile co-ordinate, like that you would get from Tiled, and converts it to a
    screen space x and y co-ordinate.
    :param tile_x: the tile x coord
    :param tile_y: the tile y coord
    :param map_size: The map size in tile count.
    :param tile_size: The scaled size of the tiles.
    :return: center_x and center_y position.
    """

    # Optional Step, makes the center of the map lie at 0, 0. If not used all of the center_y's will be negative.
    t_x = tile_x - map_size[0]/2
    t_y = tile_y - map_size[1]/2

    # because the sprites are already cast to the ~30 degrees for the isometric the only needed rotations is the
    # 45 degrees. However since cos and sin 45 are both 0.707 they are removed from the system as it simply makes
    # the final center offset smaller.
    iso_x = (t_x - t_y) * (tile_size[0]/2)
    iso_y = -(t_x + t_y) * (tile_size[1]/2)

    # The iso_y is negative, because it means that the lower values start at the top rather than the bottom.
    # this fixes an issue that tiled causes as the top most tile having the value (0, 0) which would make the whole map
    # upside down.

    # Note: This algorithm also only works assuming the tiles are in "Square" isometric mode not "offset".

    return iso_x, iso_y


def from_isometric_square(center_x: int, center_y: int, map_size: tuple[int, int], tile_size: tuple[int, int]):
    """
    Helper function which takes a screen space center x and center y tile co-ordinates and converts them to tile space.
    :param center_x: The world space x coord.
    :param center_y: The world space y coord.
    :param map_size: The map size in tile count.
    :param tile_size: The scaled size of the tiles.
    :return: tile_x and tile_y position.
    """

    # It took a lot of bad algebra to get here, and to be honest I don't know why this works. Just trust me it works.
    # I could maybe find the maths somewhere in my notes. The easier way to have calculated it would have been to find
    # the inverse matrix, which is essentially what I found in the end. I instead (not knowing matrix mathematics) did
    # the simultaneous equation to find it.
    tiled_x = center_x/tile_size[0] - center_y/tile_size[1] + 1
    tiled_y = -center_x/tile_size[0] - center_y/tile_size[1] + 1

    # If you did the original shifting, remove it.
    tiled_x += map_size[0]/2
    tiled_y += map_size[1]/2

    return math.floor(tiled_x), math.floor(tiled_y)


class IsoList(arcade.SpriteList):

    def clear(self):
        raise NotImplementedError()

    def __init__(self,
                 use_spatial_hash=None,
                 spatial_hash_cell_size=128,
                 is_static=False,
                 atlas: "TextureAtlas" = None,
                 capacity: int = 100,
                 lazy: bool = False,
                 visible: bool = True,):
        super().__init__(use_spatial_hash, spatial_hash_cell_size, is_static, atlas, capacity, lazy, visible)

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        if self._sprite_pos_changed:
            self.sort(key=lambda sprite: sprite.x + sprite.y, reverse=True)
        super().draw(filter=filter, pixelated=pixelated, blend_function=blend_function)
