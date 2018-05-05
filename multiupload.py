import os
import time
import os.path
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import ImageFilter
from PIL.ImageFilter import (UnsharpMask)
from PIL import Image, ImageFile
import facebook

start_time = time.time()
patch = "d:/Temp/facebookphoto/" #YOU FOLDER
basewidth = 3000
album_id = "ID ALBUM FACEBOOK" #https://www.facebook.com/irgitpro/media_set?set=a.>>>>>1311276982310762<<<<<.1073741856.100002854194070&type=3
token = "YOU TOKEN FACEBOOK"

class filepatch:
    """Class of receiving and checking files. We write good files in godfile.godfile
     Be careful os.remove (s) everything does not delete photos!"""
    dir = (os.listdir(path=patch))
    godfile = set()
    for file in dir:
        pic = (patch+file)
        try:
            if Image.open(pic):
                godfile.add(str(pic))
        except IOError as errorfile:
            err = (str(errorfile))
            s = err.replace("cannot identify image file ", "")
            s = s.replace("'", "")
            os.remove(s)
    print("Received %s good links" % str(len(godfile)))

class postphoto:
    if filepatch.godfile:
        print ("Starting postprocessing %s photos" % str(len(filepatch.godfile)))
        print("*" * 60)
        for image in filepatch.godfile:

            ImageFile.LOAD_TRUNCATED_IMAGES = True
            img = Image.open(image)
            wpercent = (basewidth / float( img.size[0]))
            hsize = int((float(img.size[1] ) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.BILINEAR) #ANTIALIAS LANCZOS BILINEAR  BICUBIC
            #img.show(image)

            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance( 1.1 )
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance( 1.15 )
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance( 0.8 )
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance( 1.3 )
            img = img.filter( UnsharpMask( radius=1, percent=80, threshold=3 ) )
            img.save(image)
            enhancer = ImageEnhance.Sharpness( img )
            img = enhancer.enhance( 0.2 )
            print ("Processing photo %s completed." % str(image))

            try:
                graph = facebook.GraphAPI( access_token=token )
                if graph:
                    graph.put_photo( image=open(image, 'rb' ),
                                     album_path=album_id + "/photos" )
                    print ("Photo successfully sent")
                    os.remove( image )
                    #time.sleep(1)
                else:
                    print ("Connection error")

            except OSError as errocon:
                print (errocon)
            except Exception  as errocon2:
                print (errocon2)
            del img
    else:
        print ("Folder is empty")

print ("*"*60)
print( "--- Work completed in %s seconds ---" % (time.time() - start_time) )
