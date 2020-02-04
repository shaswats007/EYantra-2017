import csv

## Dictionaries for storing information about Overlay

RED_MARKERS = {}
GREEN_MARKERS = {}
BLUE_MARKERS = {}

## Initialise Marker Information Dictionaries

with open('ip.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in reader:
		l = row[0].split(",")
		if(l[0] == 'Red'):
			RED_MARKERS[l[1]] = l[2]
		if(l[0] == 'Green'):
			GREEN_MARKERS[l[1]] = l[2]
		if(l[0] == 'Blue'):
			BLUE_MARKERS[l[1]] = l[2]		


'''
*Function Name: stitch
*Input: ip_image, count
*Output: A overlay image that consists of the ip_image stiched to count times.
*Logic: Concatenate the ip_image count times for overlaying it on the background.
'''


def stitch(ip_image,count):
	overlay = ip_image.copy()
	for i in range(count):
		overlay = np.concatenate((overlay, ip_image), axis = 1)
	return overlay


'''
*Function Name: blend_transparent
*Input: face_img, overlay_t_img
*Output: Numpy matrix consisting of overlay_t_img overlayed on the face_img
*Logic:
*Note: This is the same function that was provided in Eyantra Task 1B
'''

def blend_transparent(face_img, overlay_t_img):
	# Split out the transparency mask from the color info
	overlay_img = overlay_t_img[:,:,3]	# Grab the BRG planes
	overlay_mask = overlay_t_img[:,:,3]     # And the alpha plane

	# Again calculate the inverse mask
	background_mask = 255 - overlay_mask
	
	# Turn the masks in three chanel, so we can use them as weights
	overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_BGR2GRAY)
	background_mask = cv2.cvtColor(background_mask, cv2.COLOR_BGR2GRAY)
	
	# Create a masked out face image, and masked out overlay
	# We convert the images to floating point in range 0.0 to 10.0
	face_part = (face_img * (1/255.0)) * (background_mask * (1/255.0))
	overlay_part = (overlay_img * (1/255.0)) * ((overlay_mask * (1/255.0))

	# And finally just add them together, and rescale it back to a 8bit integer image
	return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

