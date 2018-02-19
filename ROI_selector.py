import argparse
import cv2 # Image manipulation
import numpy as np # Efficient storing of ROI
import pickle # Serializing numpy objects for future use
from datetime import datetime

tmpPt = [] # current ROI
refPts = [] # list of all ROI

in_selection = False 

def ROI_select(event, x, y, flags, param):

	global refPts, in_selection, tmpPt

	# clicking left mouse button --> selection started and first point recorded
	if event == cv2.EVENT_LBUTTONDOWN:
		tmpPt = [(x, y)]
		in_selection = True

	# releasing left mouse button --> selection ends and second point recorded
	elif event == cv2.EVENT_LBUTTONUP:
		tmpPt.append((x, y))
		in_selection = False

		# drawing a rectangle to show the user how the selection went
		cv2.rectangle(image, tmpPt[0], tmpPt[1], (0, 255, 0), 2)
		cv2.imshow("image", image)
		refPts.append(tmpPt) #adding the ROI to the list

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-r", "--roi", default="ROI_"+datetime.now().strftime("%Y%m%d-%H%M%S")+".p", help="Path to save ROI")
args = vars(ap.parse_args())



image = cv2.imread(args["image"])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", ROI_select)

# loop until (d) done or (r) reset
while True:
	# image displayed and waiting for keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF

	# r pressed --> reset selection
	if key == ord("r"):
		image = clone.copy()
		refPts = []

	# d pressed --> done
	elif key == ord("d"):
		break

array = []
for i, pt in enumerate(refPts):
	print(pt)
	array.append([pt[0][0], pt[0][1], pt[1][0], pt[1][1]])

array = np.array(array)

savein = args["roi"]
pickle.dump( array, open( savein, "wb" ) )

print("Saved Regions of Interest as Pickle file in: " + savein)

cv2.destroyAllWindows()