#coding: UTF-8

#from pickle import TRUE
from gimpfu import *

PAGE_WIDTH = 823
PAGE_HEIGHT = 1024

IMG_LAYER_NAME = "Immagine"
IMG_MAX_SIZE = 650
IMG_CENTRE_X = int((PAGE_WIDTH-IMG_MAX_SIZE)/2 + (IMG_MAX_SIZE/2))
IMG_CENTRE_Y = int((PAGE_WIDTH-IMG_MAX_SIZE)/2 + (IMG_MAX_SIZE/2))

def crea_pagina_libro(image, drawable, image_path, author):

    # crea, scala e posiziona immagine
    image_layer = pdb.gimp_file_load_layer(image, image_path)
    pdb.gimp_image_insert_layer(image, image_layer, None, 2)
    
    ridimensiona_layer(image_layer, IMG_MAX_SIZE)
    centra_layer(image_layer)



def ridimensiona_layer(layer, max_size):
    scalar = 1.0
    if layer.width > layer.height:
        scalar = float(max_size) / float(layer.width)
    else:
        scalar = float(max_size) / float(layer.height)

    pdb.gimp_layer_scale(layer,
                         int(layer.width * scalar),
                         int(layer.height * scalar),
                         FALSE)

def centra_layer(layer):
    pos_x = int(float(PAGE_WIDTH/2) - float(layer.width /2))
    pos_y = int(float(PAGE_WIDTH/2) - float(layer.height /2))

    pdb.gimp_layer_set_offsets(layer,
                               pos_x,
                               pos_y)

register(
    "CreaPaginaLibro",  # The name of the command when called from the command line or script
    "Da usare sul file PaginaLibro.xcf, carica tutte le immagini specificate e crea pagine del libro da usare in Unity, come PNG.",  # Information about plugins displayed in the procedure browser
    "CreaPaginaLibro2",  # Information about plugins displayed in the procedure browser
    "Marzia",  # Author's name
    "Marzia",  # Copyright holder's name
    "2022",  # Year of copyright
    "<Image>/ScriptPerIvana/CreaPaginaLibro",  # Labels used for plugins in menus
    "RGB*, GRAY*",  # The type of image to be processed by the plugin
    [
        # (PF_STRING, "image_folder_path",
        #             "Path del folder di origine delle immagini PNG",
        #              ""),
        (PF_STRING, "image_path",
                    "Path immagine dipinto",
                     ""),

        (PF_STRING, "author",
                    "Nome autore dipinto",
                     "")
    ],  # argument
    [],  # Return value
    crea_pagina_libro  #Function name
)

main()