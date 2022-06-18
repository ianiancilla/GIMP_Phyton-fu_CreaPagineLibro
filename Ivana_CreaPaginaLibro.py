#coding: UTF-8

#from pickle import TRUE
import os
from gimpfu import *

# page
PAGE_WIDTH = 823
PAGE_HEIGHT = 1024

# image
IMG_MAX_SIZE = 650
IMG_CENTRE_X = int((PAGE_WIDTH-IMG_MAX_SIZE)/2 + (IMG_MAX_SIZE/2))
IMG_CENTRE_Y = int((PAGE_WIDTH-IMG_MAX_SIZE)/2 + (IMG_MAX_SIZE/2))
IMG_LAYER_NAME ="Immagine"
SHADOW_LAYER_NAME ="Drop Shadow"


# tape
TAPE_LEFT_LAYER_NAME = "Tape_Left"
TAPE_RIGHT_LAYER_NAME = "Tape_Right"
TAPE_OVERLAP = 20

# author
AUTHOR_LAYER_NAME = "Autore"
AUTHOR_TEXT_COLOR = "#2c1513"
AUTHOR_VERTICAL_OFFSET = -50
AUTHOR_TEXT_FONT = "IM FELL English Italic"

# page
PAGE_LAYER_NAME = "Pagina"
PAGE_TEXT_COLOR = "#1e1312"
PAGE_TEXT_FONT = "Serif Bold"

def crea_pagine_da_folder(image, drawable, image_folder_path, destination_folder_path, author, starting_page):
    page_number = starting_page
    # per ogni immagine nel folder
    for filename in os.listdir(image_folder_path):
        try:
            if filename.lower().split(".")[-1] in ("png", "jpg"):
                image_path = os.path.join(image_folder_path, filename)
                # crea pagina
                crea_pagina_libro(image, drawable, image_path, destination_folder_path, author, page_number)
                # esporta come png
                png_name = str(page_number) +".png"
                destination_path = os.path.join(destination_folder_path, png_name)

                # crea nuova immagine da mergeare per esportare tutti i livelli come PNG
                new_image = pdb.gimp_image_duplicate(image)
                layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
                pdb.file_png_save_defaults(new_image, layer, destination_path, destination_path)
                pdb.gimp_image_delete(new_image)
                
                # cancella immagine
                image.remove_layer(pdb.gimp_image_get_layer_by_name(image, IMG_LAYER_NAME))
                image.remove_layer(pdb.gimp_image_get_layer_by_name(image, SHADOW_LAYER_NAME))

                #aumenta pagina
                page_number+=1
        except Exception as error:
            pdb.gimp_message(error)

    pdb.gimp_message("Operazione completata!")



def crea_pagina_libro(image, drawable, image_path, destination_folder_path, author, page_number):

    # crea, scala e posiziona immagine
    image_layer = pdb.gimp_file_load_layer(image, image_path)
    pdb.gimp_image_insert_layer(image, image_layer, None, 2)
    pdb.gimp_layer_set_name(image_layer, IMG_LAYER_NAME)
    
    ridimensiona_layer(image_layer, IMG_MAX_SIZE)
    centra_layer(image_layer)
    # drop shadow
    pdb.gimp_image_set_active_layer(image, pdb.gimp_image_get_layer_by_name(image, IMG_LAYER_NAME))
    pdb.script_fu_drop_shadow(image, pdb.gimp_image_get_layer_by_name(image, IMG_LAYER_NAME), 0, 20, 20, "#000000", 30, 0)

    # sistema lo scotch
    layer_tape_left = pdb.gimp_image_get_layer_by_name(image, TAPE_LEFT_LAYER_NAME)
    layer_tape_right = pdb.gimp_image_get_layer_by_name(image, TAPE_RIGHT_LAYER_NAME)
    left_border_x = int(float(PAGE_WIDTH/2) - float(image_layer.width /2))
    right_border_x = left_border_x + image_layer.width

    pdb.gimp_layer_set_offsets(layer_tape_left,
                               int(left_border_x - layer_tape_left.width + TAPE_OVERLAP),
                               int(IMG_CENTRE_Y - layer_tape_left.height/2))
    pdb.gimp_layer_set_offsets(layer_tape_right,
                               int(right_border_x - TAPE_OVERLAP),
                               int(IMG_CENTRE_Y - layer_tape_right.height/2))

    # sistema testo autore
    layer_author_text = pdb.gimp_image_get_layer_by_name(image, AUTHOR_LAYER_NAME)
    pdb.gimp_text_layer_set_text(layer_author_text, author)
    pdb.gimp_text_layer_set_color(layer_author_text, AUTHOR_TEXT_COLOR)
    pdb.gimp_text_layer_set_font(layer_author_text, AUTHOR_TEXT_FONT)

    img_bottom = int(IMG_CENTRE_Y + image_layer.height/2)
    pdb.gimp_layer_set_offsets(layer_author_text,
                               int(IMG_CENTRE_X - float(layer_author_text.width /2)),
                               int(img_bottom + (PAGE_HEIGHT - img_bottom + AUTHOR_VERTICAL_OFFSET)/2 - layer_author_text.height/2 ))

    # sistema numero pagina
    layer_page_text = pdb.gimp_image_get_layer_by_name(image, PAGE_LAYER_NAME)
    pdb.gimp_text_layer_set_text(layer_page_text, page_number)
    pdb.gimp_text_layer_set_color(layer_page_text, PAGE_TEXT_COLOR)
    pdb.gimp_text_layer_set_font(layer_page_text, PAGE_TEXT_FONT)


    if (page_number%2 == 0):
        pdb.gimp_text_layer_set_justification(layer_page_text, 0)   # justify left
    else:
        pdb.gimp_text_layer_set_justification(layer_page_text, 1)   # justify right


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
    pos_x = int(IMG_CENTRE_X - float(layer.width /2))
    pos_y = int(IMG_CENTRE_X - float(layer.height /2))

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
        (PF_STRING, "image_folder_path",
                    "Path del folder di origine delle immagini PNG o JPG",
                    ""),
        (PF_STRING, "destination_folder_path",
                    """
                    
Path di destinazione delle pagine del libro

****
IMPORTANTE: file gia presenti potrebbero
venire sovrascritti!!!
****
""",
                    ""),
        (PF_STRING, "author",
                    "Nome autore dipinto",
                    ""),
        (PF_INT, "starting_page",
                 "Pagina iniziale di questa serie",
                 0)
    ],  # argument
    [],  # Return value
    crea_pagine_da_folder  #Function name
)

main()