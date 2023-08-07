# the main purpose of this project is to create a code encoder and decoder , that generate an image from code , and vis versa

#todo :
    # read code source content from file
    # tokenize it in the smallest size possible , possibly characters
    # read tokens 4 by 4 or 3 by 3 depending on the library used if it allows alpha channels
    # the characters are ascii , range from alphanumerique to symbols , soo we got to make them go up to 255
    # push them to the image processor to write each pixel into the image
    
from PIL import Image  

a_r = (3,2)
    
def read_arr_from_file(filename):
    with open(filename) as f:
        lines = f.readlines()
    return lines
    
def flatten_arr_to_str(lines):
    code = ""
    for i in lines:
        code += i
    return code 

def calculate_width_height(area):
    aspect_ratio = a_r
    # Calculate the scaling factor 'x' from the area and aspect ratio
    x = (area / (aspect_ratio[1] * aspect_ratio[0])) ** 0.5

    # Calculate the width and height
    width = round(x * aspect_ratio[0])
    height = round(x * aspect_ratio[1])

    return width, height


def encode_code(filename):
    lines = read_arr_from_file(filename)
    code = flatten_arr_to_str(lines)

    intokens = []

    for v in [*code]:
        intokens.append(ord(v))
        
    # print(intokens)


    pixels = []
            
    for i in range(0, len(intokens), 4):
        token1 = intokens[i] if i < len(intokens) else 255
        token2 = intokens[i + 1] if i + 1 < len(intokens) else 255
        token3 = intokens[i + 2] if i + 2 < len(intokens) else 255
        token4 = intokens[i + 3] if i + 3 < len(intokens) else 255
        pixels.append((token1, token2, token3, token4))


    width , height = calculate_width_height(len(pixels))
    img  = Image.new( mode = "RGBA", size = (width, height), color = (255, 255, 255, 255) )

    x = 0
    for i in range(width):
        for j in range(height):
            if(x>=len(pixels)):
                break
            img.putpixel((i,j) , pixels[x])
            x+=1
        
    return img

def decode_code(imagefile):
    pixels = []
    img = Image.open(imagefile)
    width, height = img.size

    itokens = []
    for x in range(width):
        for y in range(height):
            pixels.append(img.getpixel((x,y)))
            
    itokens = list(sum(pixels,()))
    tokens = []
    for i in itokens:
        if(i==255):
            continue
        tokens.append(chr(i))
        
    print("".join(tokens))

    

img = encode_code('tailwind.html')

img.save("code.png")

img = decode_code("code.png")