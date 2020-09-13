import os, io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
import cv2


SOURCE = '../uploads/apple.png'
#SOURCE = Path of User's uploaded image

#Google authentication client key

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
print(path)


#Create a hash set of fruits
def load_fruits():
    fruit_set = set()
    with open('Fruits.txt') as infile:
        for line in infile:
            fruit_set.add(line.rstrip('\n').lower())
    return fruit_set

def classifyFruit(image_path, fruits):
    """
    Takes image path and fruits set and classifies fruit.
    """
    image = cv2.imread(image_path)
    client = vision.ImageAnnotatorClient()
    #read image file
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    df = pd.DataFrame(columns=['description'])
    for label in labels:
        fruit_type = label.description.lower()
        if fruit_type in fruits:
            # df = df.append(
            #     dict(
            #         description=fruit_type
            #     ),
            #     ignore_index=True
            # )
            return fruit_type
    return None


#Read text from label given a URL
def readImgUrl(img_url, client):
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = img_url
    response = client.text_detection(image=image)
    text_from_image = response.text_annotations
    df = pd.DataFrame(columns=['description'])
    for text in text_from_image:
        df = df.append(
            dict(
                description=text.description
            ),
            ignore_index=True
        )
    return df

if __name__ == '__main__':
    fruits = load_fruits()
    print(fruits)
    #path TBD
    print(classifyFruit(SOURCE,fruits))