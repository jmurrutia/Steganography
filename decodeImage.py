# Steganography Decode
# Jose M. Urrutia
# 10/31/17
# CPSC 353

##########################################################################
# This program will decode text from an image and print the text
# on screen, as well as the length of the text. Steps:
# - Read pixels from bottom right to top left
# - First 11 bytes hold text length
# - After 11 bytes, pixel bytes hold actual text
# - Print the length of the text on screen
# - Print the embeded text on screen
##########################################################################
from PIL import Image

##########################################################################
# This function will return the value for length of the embedded text
# @param w is the width of the original image
# @param h is the height of the original 
# @param image is the image object
# @return the integer value of our embeded text
##########################################################################
def getTextLength(w, h, image):

	# This list will hold the binary values that are
	# extracted in the first 11 bytes. Once converted
	# to ASCII, we can get the length of the text
	textLength = []

	# textLengthCount will help us in counting the first 
	# 11 bytes that hold the text length
	textLengthCount = 0

	# textLengthString will hold our text length binary
	# value in a string
	textLengthString = ''

	# We are going to use a nested for loop to traverse 
	# through the image. The starting row will be height-1,
	# we will end at 0, and step backwards. The staring 
	# column will be width-1, end at 0, and step backwards.
	# ***range(start, stop, step)***

	# We only need to go through 1 row. So we start at the last row
	# and end and the row above that
	for row in range(h - 1, h - 2, -1):

		# Then backwards from last pixel to 11th to last pixel
		for column in range(w - 1, w - 12, -1):

			# Retrieve R, G, B values from each pixel.
			# We get the column first, then row because we need
			# to extract the info backwards
			red, green, blue = image.getpixel((column, row))

			# Now we need to retrieve the least significant bit
			# from each RBG value
			lsbRed = (red & 1)
			lsbGreen = (green & 1)
			lsbBlue = (blue & 1)

			# If statement to traverse through first 10 pixels
			if textLengthCount < 10:

				# Append the lsb value to our textLength list.
				# Convert to string to later convert to integer value
				textLength.append(str(lsbRed))
				textLength.append(str(lsbGreen))
				textLength.append(str(lsbBlue))

			# If statment for pixel 11. Here, we only care about
			# our R and G values. B is ignored.
			if textLengthCount == 10:
				textLength.append(str(lsbRed))
				textLength.append(str(lsbGreen))

			# Increase our counter
			textLengthCount += 1

			# Join our list of string binary values into one variable
			textLengthString = ''.join(textLength)

	# Convert the binary value to an integer
	lengthOfText = int(textLengthString, 2)

	# Return the value
	return lengthOfText

##########################################################################
# This function will return the secret embedded text
# @param w is the width of the original image
# @param h is the height of the original 
# @param image is the image object
# @param textLength is the length of our text
# @return the embeded text
##########################################################################
def pullText(w, h, image, totalAsciiBits):

	# Keep track of pixel count
	pixelCount = 0

	# List variable to hold 
	textInBinary = []

	# Traverse through image 
	# Move backwards through rows
	for row in range(h - 1, -1, -1):

		# Move backwards through columns
		for column in range(w - 12, -1, -1):

			# Retrieve RGB values from each pixel
			red, green, blue = image.getpixel((column, row))

			# Now we need to retrieve the least significant bit
			# from each RBG value
			lsbRed = (red & 1)
			lsbGreen = (green & 1)
			lsbBlue = (blue & 1)

			# Append the lsb value to our list and decrement 
			# the number of bits
			if pixelCount < totalAsciiBits:
				textInBinary.append(str(lsbRed))
				pixelCount += 1
				# print(pixelCount)
				textInBinary.append(str(lsbGreen))
				pixelCount += 1
				# print(pixelCount)
				textInBinary.append(str(lsbBlue))
				pixelCount += 1
				# print(pixelCount)

	# Join our list of string binary values into one variable
	binaryTextToString = ''.join(textInBinary)

	# Return our string of binary values
	return binaryTextToString

def main():
	# Open the image that will be decoded
	im = Image.open('EncodedImage.png')

	# Get the width and the height of the image. This
	# helps us in knowing where to begin collecting 
	# the text length
	width, height = im.size

	# Get the length of the embedded text
	embedLength = getTextLength(width, height, im)

	# Display the value of our text
	print('The length of our hidden text is', str(int(embedLength / 8)), 'characters\n')

	# Get the binary string of our text
	message = pullText(width, height, im, embedLength)

	# Split our binary string into 8 bits for each character
	message = " ".join(message[i:i+8] for i in range(0, len(message), 8))

	# Loop to convert each byte into a character
	plaintext = ""
	for byte in message.split():

		plaintext += chr(int(byte, 2))

	# Display our secret message on screen
	print('Our secret message is...\n', plaintext)

if __name__ == "__main__":
	main()