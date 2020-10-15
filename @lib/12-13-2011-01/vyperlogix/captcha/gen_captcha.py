import random
import Image
import ImageFont
import ImageDraw
import ImageFilter

def gen_captcha(text, fnt, fnt_sz, file_name, fmt='JPEG'):
    """Generate a captcha image"""
    # randomly select the foreground color
    fgcolor = random.randint(0,0xffff00)
    # make the background color the opposite of fgcolor
    bgcolor = fgcolor ^ 0xffffff
    # create a font object 
    font = ImageFont.truetype(fnt,fnt_sz)
    # determine dimensions of the text
    dim = font.getsize(text)
    # create a new image slightly larger that the text
    im = Image.new('RGB', (dim[0]+5,dim[1]+5), bgcolor)
    d = ImageDraw.Draw(im)
    x, y = im.size
    r = random.randint
    # draw 100 random colored boxes on the background
    for num in range(100):
        d.rectangle((r(0,x),r(0,y),r(0,x),r(0,y)),fill=r(0,0xffffff))
    # add the text to the image
    d.text((3,3), text, font=font, fill=fgcolor)
    im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
    # save the image to a file
    im.save(file_name, format=fmt)

def gen_random_word(wordLen=6):
        allowedChars = "abcdefghijklmnopqrstuvwzyzABCDEFGHIJKLMNOPQRSTUVWZYZ0123456789"
        word = ""
        for i in range(0, wordLen):
            word = word + allowedChars[random.randint(0,0xffffff) % len(allowedChars)]
        return word
    
if __name__ == '__main__':
    """Example: This grabs a random word from the dictionary 'words' (one
	word per line) and generates a jpeg image named 'test.jpg' using
	the truetype font 'porkys.ttf' with a font size of 25.
	"""
    word = gen_random_word()
    gen_captcha(word.strip(), 'arial.ttf', 25, "test.jpg")
        