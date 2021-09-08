from PIL import Image, ImageDraw, ImageFont
import itertools

class LedTemp():

    def __init__(self, tile_width, tile_height, h_tiles, v_tiles, colors):
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.h_tiles = h_tiles
        self.v_tiles = v_tiles
        self.colors = colors

    def create_tile(self, color, index_number):
        # Handles generating a single tile

        font_size = 30
        font = ImageFont.truetype("arial.ttf", size=font_size)
        
        tile_size = [(0,0), (self.tile_width - 1, self.tile_height - 1)]

        tile_object = Image.new("RGB", (self.tile_width, self.tile_height))

        tile = ImageDraw.Draw(tile_object)
        tile.rectangle(tile_size, fill = color, outline="#dddddd", width=1)
        
        text_w, text_h = font.getsize(index_number) # gets size of text object for calculating alighnment
        text_pos = ((self.tile_width - text_w)/2, (self.tile_height - text_h)/2) # Centering text in the tile

        tile.text(text_pos, index_number, align="center", font=font) # Placing text over the tile
        
        return tile_object


    def generate_tiles(self): 
        # Generating the number of image tiles - Return a list of tiles
        
        num_tiles = self.h_tiles * self.v_tiles

        tiles = [] # A list to hold all the generated tiles.

        cycled_colors = itertools.cycle(self.colors)

        h_tile_counter = 0 # To keep count of horizontal tiles

        for i in range(num_tiles):
            tile = f"tile_{i}"
            tile = self.create_tile(next(cycled_colors), str(f"{i+1:03d}"))
            h_tile_counter += 1

            if h_tile_counter == self.h_tiles:
                next(cycled_colors)
                h_tile_counter = 0
                
            tiles.append(tile)

        return tiles #Returns a list of tiles
                

    def concat_tiles(self, tiles):
        # Create the grid template using list of tiles and number of verticle and horizontal tiles.
        
        resolution = (tiles[0].width * self.h_tiles, tiles[0].height * self.v_tiles)
        print(f"H: {resolution[0]}, V: {resolution[1]}")

        grid = Image.new('RGB', resolution)

        tile_count = 0
        for tv in range(self.v_tiles):

            for th in range(self.h_tiles):
                grid.paste(tiles[th + tile_count], (tiles[0].width * th, tiles[0].height * tv))

            tile_count = tile_count + self.h_tiles

        return grid


    def save_grid(self, grid_name):
        grid_name.save(f"template_{self.tile_width*h_tiles}x{self.tile_height*v_tiles}.png", "PNG")
                

# SETTING OF PARAMETERS FOR TEMPLATE

# colors = ["Red", "Yellow", "Green", "Blue", "Magenta", "Orange"] # Define the color paller to be used
# colors = ["#fe5000", "#55215b", "#153c77", "#f8063b", "#62ac05"] # Define the color paller to be used
colors = ["#60acbd", "#de8789", "#f37544", "#ee5259", "#7cc953"] # Define the color paller to be used

tile_width = 128 # With in pixels
tile_height = 128  # Height in pixels 
h_tiles = 12 # Number of verticle tiles 
v_tiles = 4 # Number of horizontal tiles

# FUNCTION CALLS
LedTemp_1 = LedTemp(tile_width, tile_height, h_tiles, v_tiles, colors) 
tiles = LedTemp_1.generate_tiles()
grid = LedTemp_1.concat_tiles(tiles)

grid.show()
LedTemp_1.save_grid(grid)
