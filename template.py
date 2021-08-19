from PIL import Image, ImageDraw, ImageFont
import itertools


def create_tile(w, h, color, index_number):
    # Handles generating a single tile

    font_size = 30
    font = ImageFont.truetype("arial.ttf", size=font_size)
    
    tile_size = [(0,0), (w - 1, h - 1)]

    tile_object = Image.new("RGB", (w, h))

    tile = ImageDraw.Draw(tile_object)
    tile.rectangle(tile_size, fill = color, outline="#dddddd", width=1)
    
    text_w, text_h = font.getsize(index_number) # gets size of text object for calculating alighnment
    text_pos = ((w - text_w)/2, (h - text_h)/2) # Centering text in the tile

    tile.text(text_pos, index_number, align="center", font=font) # Placing text over the tile
    
    return tile_object


def generate_tiles(tile_w, tile_h, h_tiles, v_tiles): 
    # Generating the number of image tiles - Return a list of tiles
    
    num_tiles = h_tiles * v_tiles

    tiles = [] # A list to hold all the generated tiles.

    cycled_colors = itertools.cycle(colors)

    h_tile_counter = 0 # To keep count of horizontal tiles

    for i in range(num_tiles):
        tile = f"tile_{i}"
        tile = create_tile(tile_w, tile_h, next(cycled_colors), str(f"{i+1:03d}"))
        h_tile_counter += 1

        if h_tile_counter == h_tiles:
            next(cycled_colors)
            h_tile_counter = 0
            
        tiles.append(tile)

    return tiles
            

def concat_tiles(tiles, h_number, v_number):
    # Create the grid template using list of tiles and number of verticle and horizontal tiles.
    
    resolution = (tiles[0].width * h_number, tiles[0].height * v_number)
    print(f"H: {resolution[0]}, V: {resolution[1]}")

    grid = Image.new('RGB', resolution)

    tile_count = 0
    for tv in range(v_number):

        for th in range(h_number):
            grid.paste(tiles[th + tile_count], (tiles[0].width * th, tiles[0].height * tv))

        tile_count = tile_count + h_number

    return grid


# SETTING OF PARAMETERS FOR TEMPLATE

# colors = ["Red", "Yellow", "Green", "Blue", "Magenta", "Orange"] # Define the color paller to be used
# colors = ["#fe5000", "#55215b", "#153c77", "#f8063b", "#62ac05"] # Define the color paller to be used
colors = ["#60acbd", "#de8789", "#f37544", "#ee5259", "#7cc953"] # Define the color paller to be used

tile_width = 128 # With in pixels
tile_height = 128  # Height in pixels 
v_tiles = 12 # Number of verticle tiles 
h_tiles = 4 # Number of horizontal tiles


# FUNCTION CALLS

tiles = generate_tiles(tile_width, tile_height, v_tiles, h_tiles) # Generating a list of tiles
grid = concat_tiles(tiles, v_tiles, h_tiles) # Concatenating generated tiles from list
grid.show()

