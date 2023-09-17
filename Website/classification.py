import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import logging
logging.getLogger('tensorflow').setLevel(logging.FATAL)
import cv2 as cv
from cvzone.ClassificationModule import Classifier
import time

class classification:

    def __init__(self, model_path, labels_path):
        self.model_path = model_path
        self.labels_path = labels_path
        self.mydata = Classifier(self.model_path, self.labels_path)

    def classify_image(self, img_data):

        if img_data is None:
            return("Error: Unable to read the image.")


        predict, index = self.mydata.getPrediction(img_data, color=(0, 0, 255))

        if index == 0:
            return("Name: Tulsi-leaf$ Species: Ocimum tenuiflorum$ Description: Tulsi is an aromatic shrub in the basil family that is thought to have originated in north central India and now grows native throughout the eastern world tropics. It is an erect, much branched sub-shrib 30-60cm tall, with simple opposite green or purple leaves. Within Ayurveda, tulsi is known as \"Mother Medicine of Nature\" and \"The Queen of Herbs\".$ Habitat: tropical, sub-tropical regions ")
        elif index == 1:
            return("Name: Aloevera-leaf$ Species: Aloe barbadensis miller$ Description: Aloevera is a herb with succulent leaves that are arranged in a rosette.The leaves are grey to green and sometimes have white spots on their surfaces.They have sharp, pinkish spines along their edges and are the source of the colourless get found in many commercial and medicinal products.$ Habitat: arid areas")
        elif index == 2:
            return("Name: Doddpathre-leaf$ Species: Coleus amboinicus$ Description: Doddapatre is a member of the mint family Lamiaceae and grows up to 1m tall.The stem is fleshy,either with long rigid hairs or densely covered with soft,short, and erect hairs. Leaves are fleshy,simple,broad and oval-shaped with a tapering tip. The margins are coarse and slightly serrated.$ Habitat: roadsides, stony dry wastelands")
        elif index == 3:
            return("Name: Neem-leaf$ Species: Azadirachta indica$ Description: Neem trees are attractive broad-leaved evrgreens that can grow up to 30m tall and 2.5m in girth.Their spreading branches form rounded crowns as much as 20m across.Neem leaves are medium to large in size and elongated to oblong in shape, averaging 20-40cm in length.The vibrant green leaves are smooth and glossy with sharp,serrated edges.$ Habitat: grasslands, shrublands, woodlands,floodplains")
        elif index == 4:
            return("Name: Curry-leaf$ Species: Murraya koenigii$ Description: Curry leaf is a small, tropical to sub-tropical tree or shrub that itypically grows to 6-15' tall and is noted for its pungent, aromatic, curry leaves which are an important flavoring used in Indian/Asian cuisine.This tree is native to moist forests in India and Sri Lanka.$ Habitat: tropical, sub-tropical regions")
        elif index == 5:
            return("Name: Henna-leaf$ Species: Lawsonia inermis$ Description: The leaves are the source of of a reddish-brown dye,Known as henna, which is commonly used for temporary body art anf to dye fabrics. The plant bears small opposite leaves and small, fragrant, white to red flowers.$ Habitat: tropical, sub-tropical regions")
        elif index == 6:
            return("Name: Hibiscus-leaf$ Species: Hibicus rosa-sinensis$ Description: Hibiscus leaves are ovate, simple and 8 to 10.5 cm long. Its green and glossy leaves are alternatively organized and several cultivars show toothed margins.$ Habitat: wetlands, savannah, woodlands")
        else:
            return None
        