from PIL import Image

#This module can classfiy the image by Average Hash Method with spilt the image to 16 pieces.
#Then calculate every piece ,consider all data and return the result
#
#author MashiMaroLjc
#version 2016-2-17

def calculate(image1,image2):
	g = image1.histogram()
	s = image2.histogram()
	assert len(g) == len(s),"error"

	data = []

	for index in range(0,len(g)):
		if g[index] != s[index]:
			data.append(1 - abs(g[index] - s[index])/max(g[index],s[index]) )
		else:
			data.append(1)
	
	return sum(data)/len(g)



def split_imgae(image,part_size):
	pw,ph = part_size
	w,h = image.size

	sub_image_list = []

	assert w % pw == h % ph == 0,"error"

	for i in range(0,w,pw):
		for j in range(0,h,ph):
			sub_image = image.crop((i,j,i+pw,j+ph)).copy()
			sub_image_list.append(sub_image)

	return sub_image_list

def classfiy_histogram_with_split(image1,image2,size = (256,256),part_size=(64,64)):
	''' 'image1' and 'image2' is a Image Object.
	You can build it by 'Image.open(path)'.
	'Size' is parameter what the image will resize to it.It's 256 * 256 when it default.  
	'part_size' is size of piece what the image will be divided.It's 64*64 when it default.
	This function return the similarity rate betweene 'image1' and 'image2'
	'''
	try:
	    image1 = image1.resize(size).convert("RGB")
	    sub_image1 = split_imgae(image1,part_size)

	    image2 = image2.resize(size).convert("RGB")
	    sub_image2 = split_imgae(image2,part_size)

	    sub_data = 0;
	    for im1,im2 in zip(sub_image1,sub_image2):
		    sub_data += calculate(im1, im2)

	    x = size[0]/part_size[0]
	    y = size[1]/part_size[1]

	    pre = round((sub_data/(x*y) ),3)
	    #print(pre * 100)
	    return  pre
	except:
		return  0


__all__ = [classfiy_histogram_with_split]


def histogramImage(filepath1,filepath2):
	try:
	    image1 = Image.open(filepath1)
	    image2 = Image.open(filepath2)
	    result=classfiy_histogram_with_split(image1, image2)
	    return result
	except:
		return 0


if __name__ == '__main__':
	res=histogramImage("./image_src/unknown_132.png","./image_src/132_2.png")
	print("acc:",res)
