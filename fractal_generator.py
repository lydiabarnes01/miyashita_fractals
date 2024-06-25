"""
Basic Fractal Generator based on the stimuli used in
Miyashita, Y. (1988). Neuronal correlate of visual associative long-term memory in the primate temporal cortex. Nature, 335(6193), 817-820.

reimplemented in python with PIL

lydia barnes, april 2024
modifying miyashita approach to produce specific classes of stimuli varying on
    1. recursive depth
    2. colour
    3. edges
miyashita randomised these to produce a varied stimulus set. we want to control
the proportions of stimuli in each class, and record the classes. we also want 
to lock stimulus size, unless we start to re-introduce superpositions.
"""


import numpy as np
import json
import math
from PIL import Image, ImageDraw
from PIL import ImagePath 
import argparse
import colorsys


# Parse Constants from the Command Line
parser = argparse.ArgumentParser(
            description='Fractal generator akin to (Miyashita, 1988)')
parser.add_argument('--imgsize', '-imgsize', type=int, nargs='?', default=1024)
parser.add_argument('--stimuli', '-stim', type=int, nargs='?', default=200)
parser.add_argument('--min_edges', '-minedg', type=int, nargs='?', default=3)
parser.add_argument('--max_edges', '-maxedg', type=int, nargs='?', default=5)
parser.add_argument('--min_recursion', '-minrec', type=int, nargs='?', default=2)
parser.add_argument('--max_recursion', '-maxrec', type=int, nargs='?', default=2)
parser.add_argument('--use_light_background', '-lightbg', type=int, nargs='?', default=1)

args = parser.parse_args()

IMG_W, IMG_H = args.imgsize, args.imgsize
N_STIMULI = args.stimuli
SUPERPOSITIONS = 3
MIN_EDGES, MAX_EDGES = args.min_edges, args.max_edges
MIN_RECURSION, MAX_RECURSION = args.min_recursion, args.max_recursion
MIN_G_FACTOR, MAX_G_FACTOR = -IMG_H//5, IMG_H//5
use_light_background = args.use_light_background

def outer_radius_from_edge(n_edges, edge_length):
    outer_radius = 0.5 * (1/math.sin(math.pi/n_edges) * float(edge_length)) # outer radius, i.e 2*90
    return outer_radius


def get_color_from_number(number, colordefinition):
    color = colordefinition[number]['hsv']
    return color

def create_shape_from_edges(n_edges=3, edge_length=500, rotate=0):
    pass

    xy = [
        ((math.cos(th) + 1) * outer_radius_from_edge(n_edges, edge_length),
         (math.sin(th) + 1) * outer_radius_from_edge(n_edges, edge_length))
        for th in [(i * (2 * math.pi) / n_edges)+rotate for i in range(n_edges)]
        ]  
  
    # center shape
    sum_x, sum_y = 0, 0
    for x, y in xy:
        sum_x += x
        sum_y += y
    
    xy = [
        (x + IMG_W//2 - sum_y/n_edges,
         y + IMG_H//2 - sum_y/n_edges) for x,y in xy
        ]
    
    return xy


def draw_shape_from_xy(xy, canvas, color="#eeeeff"):    
    img1 = ImageDraw.Draw(canvas)
    img1.polygon(xy, fill=color, outline=color) 
    pass

def deflect_the_midpoint_of_each_edge(xy):
    
    GA = np.random.randint(-MAX_G_FACTOR, MAX_G_FACTOR) #amplitude defined by random number generator
    
    xs = []
    ys = []
    
    for x, y in xy:
        xs.append(x)
        ys.append(y)
    
    xs.append(xy[0][0])
    ys.append(xy[0][1])
        
    xs = np.ravel(np.column_stack((np.array(xs),np.zeros(len(xs)))))
    ys = np.ravel(np.column_stack((np.array(ys),np.zeros(len(ys)))))
    for i in range(0, 2*len(xy), 2):
        mx = (xs[i] + xs[i+2])/2 
        my = (ys[i] + ys[i+2])/2 
        dx = xs[i+2] - xs[i]
        dy = ys[i+2] - ys[i]
        
        theta = np.arctan(dy/dx)
        if (dx > 0 and dy < 0):
            xs[i+1] = mx - GA * math.sin(theta)
            ys[i+1] = my + GA * math.cos(theta)
        elif (dx > 0 and dy > 0):
            xs[i+1] = mx - GA * math.sin(theta)
            ys[i+1] = my + GA * math.cos(theta)
        elif (dx < 0 and dy > 0):
            xs[i+1] = mx + GA * math.sin(theta)
            ys[i+1] = my - GA * math.cos(theta)
        elif (dx == 0 and dy > 0):
            xs[i+1] = mx + GA * math.sin(theta)
            ys[i+1] = my - GA * math.cos(theta)
        elif (dx == 0 and dy < 0):
            xs[i+1] = mx - GA * math.sin(theta)
            ys[i+1] = my + GA * math.cos(theta)    
        elif (dy == 0 and dx > 0):
            xs[i+1] = mx - GA * math.sin(theta)
            ys[i+1] = my + GA * math.cos(theta)
        elif (dy == 0 and dx < 0):
            xs[i+1] = mx + GA * math.sin(theta)
            ys[i+1] = my - GA * math.cos(theta)
        else: #(dx < 0 and dy < 0)
            xs[i+1] = mx + GA * math.sin(theta)
            ys[i+1] = my - GA * math.cos(theta)
    
    new_xy = [
        (x,y) for x,y in zip(xs,ys)
        ]
    
    new_xy.pop(-1)
    new_xy.pop(-1)
    
    return new_xy


if __name__ == "__main__":
    # load colours
    if use_light_background == 1: #light background, dark foreground colours
        canvas_colour = (255,255,255,0)
        f = open('./colours/dark-colours.json')
    else:
        canvas_colour = (0,0,0,0)
        f = open('./colours/light-colours.json')
    colordefinition = json.load(f)

    # seed the random number generator
    np.random.seed(12345)

    for colour in range(len(colordefinition)):
        for edge in range(MIN_EDGES,MAX_EDGES+1):
            for recursion in range(MIN_RECURSION,MAX_RECURSION+1):
                for stimulus in range(N_STIMULI):
                
                    # make canvas
                    canvas = Image.new("RGBA", (IMG_H,IMG_W), canvas_colour) 

                    # rotate triangles and polygons so that they sit flat against the base of the canvas
                    if edge == 4:
                        rotate = math.pi*.75
                    else:
                        rotate = math.pi/2

                    # make image    
                    xy_polygon = create_shape_from_edges(edge, IMG_W//4, rotate=rotate)
                    for rec in range(recursion):
                        xy_polygon = deflect_the_midpoint_of_each_edge(xy_polygon)
                    
                    #   get color
                    color = get_color_from_number(colour, colordefinition)
                    hsv = np.asarray((color['h'],color['s'],color['v']))

                    #   shift hue up or down 
                    hsv[0] = (hsv[0] + np.random.normal(0,5)) % 360

                    #   rescale to 0,1
                    hsv = np.asarray(( np.interp(hsv[0], (0, 360), (0, 1)), np.interp(hsv[1], (0, 100), (0, 1)), np.interp(hsv[2], (0, 100), (0, 1)) ))

                    #   get rgb
                    rgb = colorsys.hsv_to_rgb(hsv[0],hsv[1],hsv[2])
                    rgb = np.interp(rgb,(0,1),(0,255))
                    rgb = rgb.astype(int)
                    rgb = (rgb[0],rgb[1],rgb[2])

                    draw_shape_from_xy(xy_polygon, canvas, rgb)    
        
                    # auto-crop
                    imageBox = canvas.getbbox()
                    canvas = canvas.crop(imageBox)

                    # resize
                    (w,h) = canvas.size
                    width = np.max([w,h]); height = width
                    xbuffer = int(np.round((width-w)/2)); ybuffer = int(np.round((height-h)/2))

                    resized = Image.new("RGBA", (width, height), canvas_colour)
                    resized.paste(canvas,(xbuffer,ybuffer))
                    resized = resized.resize((IMG_H//2,IMG_W//2))

                    #   save image
                    resized.save('./img/{}-{}-{}edges-{}recursions.png'.format(stimulus,colordefinition[colour]['name'],edge,recursion))


'''
if __name__ == "__main__":
    # RGB colors
    f = open('256rgb.json')
    colordefinition = json.load(f)
    np.random.seed(12345)

    for stim in range(N_STIMULI):
        canvas = Image.new("RGB", (IMG_H,IMG_W), "#000000") 
        # Get a seed for the random number generator

        # Get the Number of Superposition
        n_superpositions = np.random.randint(0,4)
        n_superpositions = SUPERPOSITIONS

        # FOR LOOP
        for sup in range(n_superpositions):
            # Get the number of Edges
            n_edges = np.random.randint(MIN_EDGES, MAX_EDGES+1)
            # Get the size of Edges
            edge_size = np.random.randint(IMG_W//16, IMG_W//2)

            # Get the Polygon
            xy_polygon = create_shape_from_edges(n_edges, edge_size)
            # Get the depth of recursion
            n_recursions = np.random.randint(MIN_RECURSION, MAX_RECURSION+1)
            # FOR LOOP
            for rec in range(n_recursions):
                xy_polygon = deflect_the_midpoint_of_each_edge(xy_polygon)

            # Get the color
            color = get_color_from_number(np.random.randint(0,256), colordefinition)
            # Draw on canvas
            draw_shape_from_xy(xy_polygon, canvas, color)    
    
        canvas.save('./imgs/{}.png'.format(stim))
'''