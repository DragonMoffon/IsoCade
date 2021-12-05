from typing import Any, Dict, Optional

import pytiled_parser.tiled_object
from arcade import (
    SpriteList,
    TileMap
)

from isometric import isolist


class IsoTileMap(TileMap):

    def _calculate_sprite_position(self, sprite, column, row, scaling):
        if self.tiled_map.orientation == "isometric":
            sprite.center_x, sprite.center_y = isolist.to_isometric_square(column, row, scaling,
                                                                           self.tiled_map.map_size,
                                                                           self.tiled_map.tile_size)
        else:
            sprite.center_x = (
                    column * (self.tiled_map.tile_size[0] * scaling)
                    + sprite.width / 2
            )
            sprite.center_y = (
                     self.tiled_map.map_size.height - row - 1
                     ) * (self.tiled_map.tile_size[1] * scaling) + sprite.height / 2

    def _process_tile_layer(
        self,
        layer: pytiled_parser.TileLayer,
        scaling: float = 1.0,
        use_spatial_hash: Optional[bool] = None,
        hit_box_algorithm: str = "Simple",
        hit_box_detail: float = 4.5,
        custom_class: Optional[type] = None,
        custom_class_args: Dict[str, Any] = {},
    ) -> isolist.IsoList:

        sprite_list: isolist.IsoList = isolist.IsoList(use_spatial_hash=use_spatial_hash)
        map_array = layer.data

        # Loop through the layer and add in the list
        for row_index, row in enumerate(map_array):
            for column_index, item in enumerate(row):
                # Check for an empty tile
                if item == 0:
                    continue

                tile = self._get_tile_by_gid(item)
                if tile is None:
                    raise ValueError(
                        (
                            f"Couldn't find tile for item {item} in layer "
                            f"'{layer.name}' in file '{self.tiled_map.map_file}'"
                            f"at ({column_index}, {row_index})."
                        )
                    )

                my_sprite = self._create_sprite_from_tile(
                    tile,
                    scaling=scaling,
                    hit_box_algorithm=hit_box_algorithm,
                    hit_box_detail=hit_box_detail,
                    custom_class=custom_class,
                    custom_class_args=custom_class_args,
                )

                if my_sprite is None:
                    print(
                        f"Warning: Could not create sprite number {item} in layer '{layer.name}' {tile.image}"
                    )
                else:
                    self._calculate_sprite_position(my_sprite, column_index, row_index, scaling)

                    # Tint
                    if layer.tint_color:
                        my_sprite.color = layer.tint_color

                    # Opacity
                    opacity = layer.opacity
                    if opacity:
                        my_sprite.alpha = int(opacity * 255)

                    sprite_list.visible = layer.visible
                    sprite_list.append(my_sprite)

        return sprite_list
