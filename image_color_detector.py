import cv2
import pandas as pd
import numpy as np

# Load image
img = cv2.imread("Data/image.jpg")  # Make sure the path and file exist
imgWidth = img.shape[1] - 40

# Load color dataset
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv("Data/colors.csv", header=None, names=index)

# Initialize variables
r = g = b = xpos = ypos = 0
clicked = False

# Mouse callback function
def getRGBvalue(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# Function to get closest color name
def colorname(B, G, R):
    minimum = float('inf')
    cname = ""
    for i in range(len(df)):
        d = abs(B - int(df.loc[i, "B"])) + abs(G - int(df.loc[i, "G"])) + abs(R - int(df.loc[i, "R"]))
        if d < minimum:
            minimum = d
            cname = df.loc[i, "color_name"] + " Hex: " + df.loc[i, "hex"]
    return cname

# Set up window and mouse callback
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", getRGBvalue)

# Display loop
while True:
    cv2.imshow("Image", img)

    if clicked:
        # Draw a rectangle to show the color
        cv2.rectangle(img, (20, 20), (imgWidth, 60), (b, g, r), -1)
        text = colorname(b, g, r) + f'   R={r} G={g} B={b}'

        # Put text on top of the rectangle
        color = (0, 0, 0) if r + g + b >= 600 else (255, 255, 255)
        cv2.putText(img, text, (50, 50), 2, 0.8, color, 2, cv2.LINE_AA)

    # Exit on ESC key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
