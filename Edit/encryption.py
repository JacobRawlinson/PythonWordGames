def decrypt(filename):
    file = open(filename + ".txt", "r")

    text = file.read()
    file.close()

    firstHalf = len(text)//2 #gets the length of the first half of the text

    lastHalf = text[firstHalf:len(text):1] #saves the last half of the text in a variable
    lastHalf = lastHalf[::-1] #inverts the last half (turning it back to normal)

    firstHalf = text[0:firstHalf+1] #saves the first half of the text in a variable

    fullText = []
    n=0
    counter = 0
    while n < len(text):
        if n%2 == 0:
            fullText.extend(firstHalf[counter]) #even numbered indexed characters are brought from the first half of the text
        else:
            fullText.extend(lastHalf[counter]) #odd numbered indexed characters are brought from the last half of the text
            counter+=1
        n += 1

    fullText =  ''.join(fullText) #joins the list "fullText" to create a string
    return fullText

def encrypt(text, filename):
    firstHalf = text[0::2] #retrieves all even numbered indexed characters
    secondHalf = text[1::2] #retrieves all odd numbered indexed characters

    secondHalf = secondHalf[::-1] #inverts the second half of the encrypted text
    fullText = firstHalf + secondHalf

    file = open(filename + ".txt", "w")
    file.write(fullText) #writes the encrypted text to the file
    file.close()