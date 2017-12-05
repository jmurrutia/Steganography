# Steganography Decode
# Jose M. Urrutia
# 10/31/17
# CPSC 353

##########################################################################
# This program will encode text from an image and print the text
# on screen, as well as the length of the text. Steps:
# - Embed pixels from bottom right to top left
# - First 11 bytes hide text length
# - After 11 bytes, pixel bytes hide actual text
# - Data must be hidden inside the LSB of each RGB value
# - Input JPEG image, and consume it
# - Output PNG image
##########################################################################
from PIL import Image
import string

##########################################################################
# This function will return the 32 bit value that has the length of our
# text
# @param text is the text that will be embeded
# @return the list with 32 bit string
##########################################################################
def calculateTotalBits(text):

	# Calculate total number of bits to embed in image
	totalBitsToEmbed = len(text) * 8

	# Change our total bits into a binary number 8 bits long
	bitsToBinary = "{0:08b}".format(totalBitsToEmbed)

	# Now we will fill this number with zeros to make 32 bits
	totalBitsBinary = bitsToBinary.zfill(32)

	# Convert our binary string into a list
	binaryList = []
	binaryList.append(str(totalBitsBinary))

	binaryString = ''.join(binaryList)

	# Return the value
	return binaryString

##########################################################################
# This function will convert our original text into a string in binary
# values
# @param text is the original message that will be changed into binary
# characters
# @return string of binary values
##########################################################################
def convertToBinaryString(text):

	# Now we should change each character in our message into binary
	# and store it into a list
	textInBinary = []

	# We use a for loop to traverse through the message and convert
	# each one into 8 bit binary of type string
	for letter in text:
		tempDecimal = ord(letter)
		tempBinary = '{0:08b}'.format(tempDecimal)
		textInBinary.append(str(tempBinary))

	# Now we combine our list into a string
	stringTextBinary = ''.join(textInBinary)

	# Return the value
	return stringTextBinary

##########################################################################
# This function will compare our two bits and make sure we return the 
# bit that is needed
# @param newBit is the one we want to encode
# @param originalByte is the original R,G, or B pixel byte
# @return our new Byte
# ****This function borrowed from 
##########################################################################
def putNewBit(oldbyte, newbit):
   if newbit:
      return oldbyte | newbit
   else:
      return oldbyte & 0b11111110

##########################################################################
# This function will embed all information, starting with the length of
# our text in the first 11 pixels, then our message in pixels > 12
# @param text is the original message that will be changed into binary
# characters
# @return string of binary values
##########################################################################
def embedEveryting(binList, strTxtBin, w, h, image, imageCopy):

	# Variable pixelCounter to keep track of what pixel we're on
	pixelCounter = 0
	# Variable indexForTextLength will be used to keep track of what bit we're on
	# while encoding the length of the text
	indexForTextLength = 0
	# Variable indexForActualText will be used to keep track of what bit we'r on
	# while encoding the text
	indexForActualText = 0
	# Variabe messageBitLength holds the length in bits of our message
	messageBitLength = len(strTxtBin)

	# We are going to use a nested for loop to traverse 
	# through the image. The starting row will be height-1,
	# we will end at 0, and step backwards. The staring 
	# column will be width-1, end at 0, and step backwards.
	# ***range(start, stop, step)***
	for row in range(h - 1, -1, -1):

		# Then backwards from the last pixel to the first pixel
		for column in range(w - 1, -1, -1):

			# Retrieve R, G, B values from each pixel.
			# We get the column first, then row because we need
			# to extract the info backwards
			red, green, blue = image.getpixel((column, row))

			# Now we need to retrieve the least significant bit
			# from each RBG value
			lsbRed = (red & 1)
			lsbGreen = (green & 1)
			lsbBlue = (blue & 1)

			# Here we will encode the text length into pixels 0 through 9
			if pixelCounter < 10:

				lsbRed = int(binList[indexForTextLength])
				red = putNewBit(red, lsbRed)
				indexForTextLength += 1

				lsbGreen = int(binList[indexForTextLength])
				green = putNewBit(green, lsbGreen)
				indexForTextLength += 1

				lsbBlue = int(binList[indexForTextLength])
				blue = putNewBit(blue, lsbBlue)
				indexForTextLength += 1

				# Put the new RGB back into the pixel
				imageCopy[column, row] = red, green, blue

			# Here we will encode only to Red and Green for the last pixel
			# that holds information on text size
			if pixelCounter == 10:

				lsbRed = int(binList[indexForTextLength])
				red = putNewBit(red, lsbRed)
				indexForTextLength += 1

				lsbGreen = int(binList[indexForTextLength])
				green = putNewBit(green, lsbGreen)
				indexForTextLength += 1

				# Put the new RG back into the pixel
				imageCopy[column, row] = red, green, blue

			# Now that we have embeded the length of the text, we can now
			# embed the actual text
			if pixelCounter > 10:

				# If statement to only embed for the length of the actual bits
				# We need to include each RGB in its own IF statements to 
				# make sure that we do not go out of bounds
				if indexForActualText < messageBitLength:

					lsbRed = int(strTxtBin[indexForActualText])
					red = putNewBit(red, lsbRed)
					indexForActualText += 1

				if indexForActualText < messageBitLength:

					lsbGreen = int(strTxtBin[indexForActualText])
					green = putNewBit(green, lsbGreen)
					indexForActualText += 1

				if indexForActualText < messageBitLength:

					lsbBlue = int(strTxtBin[indexForActualText])
					blue = putNewBit(blue, lsbBlue)
					indexForActualText += 1

				# Put the new RG back into the pixel
				imageCopy[column, row] = red, green, blue

			# Increment our pixel counter
			pixelCounter += 1

	image.save("EncodedImage.png")

def main():
	# Open the image that will be encoded
	im = Image.open('encode.jpg')

	# We are going to create a copy of the image to save the information to
	imageCopy = im.load()

	# Get the width and the height of the image. This
	# helps us in knowning where to begin encoding the
	# text lenght and the text itself
	width, height = im.size

	# Now we need to open the file and get the text that will be encoded
	inFile = open("test.txt", 'r')
	textToEncode = inFile.read()

	# Display the length of characters that will be encoded
	print("The length of the message to be encoded is", len(textToEncode), "characters long\n")

	# I had an issue where the .jpg I was using was too small for the text
	# that was going to be encoded. So I placed an if statement to check
	# the size of the image can fit the length of text. If the text is
	# too long, exit the program
	if (width * height) < (len(textToEncode) * 8):
		print("The message that will be encoded is too long for this image...")
		print("Please use a larger image!!")
		exit()

	# Now we will call function calculateTotalBits to get our 32
	# bit string. These 32 bits hold the number that indicates
	# how long our text is and converts our binary string into a list
	binaryList = calculateTotalBits(textToEncode)
	
	# Call function convertToBinaryString. This will provide us 
	# with our original message converted to binary values of type
	# string
	stringTextInBinary = convertToBinaryString(textToEncode)

	embedEveryting(binaryList, stringTextInBinary, width, height, im, imageCopy)

	print("Message has been encoded")

if __name__ == "__main__":
	main()