import json
from pprint import pprint
import re

class Product:
    def __init__(self,
                 asin,
                 helpful,
                 overall,
                 reviewText,
                 reviewTime,
                 reviewerID,
                 reviewerName,
                 summary,
                 unixReviewTime):
        self.asin = asin
        self.helpful = helpful
        self.overall = overall
        self.reviewText = reviewText
        self.reviewTime = reviewTime
        self.reviewerID = reviewerID
        self.reviewerName = reviewerName
        self.summary = summary
        self.unixReviewTime = unixReviewTime

    def returnDict(self):
        return {"asin": self.asin,
                "helpful": self.helpful,
                "overall": self.overall,
                "reviewText": self.reviewText,
                "reviewTime": self.reviewTime,
                "reviewerID": self.reviewerID,
                "reviewerName": self.reviewerName,
                "summary": self.summary,
                "unixReviewTime": self.unixReviewTime}


class Facets:
    def __init__(self,
                 prodType,
                 customerRating,
                 material):
        self.prodType = prodType
        self.customerRating = customerRating
        self.material = material
                 
    def returnDict(self):
        return {"prodType": self.prodType,
                "customerRating": self.customerRating,
                "material": self.material}

def jsonToObj(line):
    j = json.loads(line)
    reviewerName = -1
    asin = j['asin']
    helpful = j['helpful']
    overall = j['overall']
    reviewText = j['reviewText']
    reviewTime = j['reviewTime']
    reviewerID = j['reviewerID']
    if 'reviewerName' in j:
        reviewerName = j['reviewerName']
    summary = j['summary']
    unixReviewTime = ['unixReviewTime']

    return Product(asin,
                   helpful,
                   overall,
                   reviewText,
                   reviewTime,
                   reviewerID,
                   reviewerName,
                   summary,
                   unixReviewTime)


def parseProducts(productsPath):
    products = []
    productsFile = open(productsPath, "r")
    for line in productsFile:
        newProduct = jsonToObj(line)
        products.append(newProduct)

    productsFile.close()
    return products


def parseWords(path):
    words = set()
    f = open(path, "r")
    for word in f:
        words.add(word.strip())

    f.close()
    return words

def parseProductType(path):
    words = {}
    f = open(path, "r")
    for line in f:
        similarTypes = line.strip().split(',')
        words[similarTypes[0]] = set(similarTypes[0])
        for i in range(1, len(similarTypes)):
            words[similarTypes[0]].add(similarTypes[i])

    f.close()
    return words                      
        

def addToDict(key, aDict):
    if key in aDict:
        aDict[key] += 1
    else:
        aDict[key] = 1

def extractFacets(reviewText,
                  posWords,
                  negWords,
                  materials,
                  prodTypes):
    reviewText = reviewText.lower()
    regex = re.compile('[^a-zA-Z]')
    reviewText = regex.sub(' ', reviewText)
    wordList = reviewText.split()

    nounDict = {}
    verbDict = {}
    adjectDict = {}
    adverbDict = {}
    posCount = 0
    negCount = 0
    materialType = set()
    prodType = {}
    
    for word in wordList:
        if word in posWords:
            posCount += 1
        elif word in negWords:
            negCount += 1

        if word in materials:
            materialType.add(word)

        for key in prodTypes:
            if word in prodTypes[key]:
                addToDict(key, prodType)        

    sentimentDiff = 0
    if len(wordList) > 0:    
        sentimentDiff = float(posCount-negCount)/len(wordList)
    print sentimentDiff
    sentimentSnippet = ''
    
    if sentimentDiff > 0.2:
        sentimentSnippet = 'Stellar review, product is highly recommended'
    elif sentimentDiff > 0.1:
        sentimentSnippet = 'Good review, would recommend buying'
    elif sentimentDiff > 0:
        sentimentSnippet = 'Neutral review, not much to say'
    else:
        sentimentSnippet = 'Negative review, avoid buying'

    topProdTypes = sorted(prodType.items(),
                          key=lambda x: x[1],
                          reverse=True)[0:3]

    prodTypesSnippet = 'This item is falls in the categories: '
    for types in topProdTypes:
        prodTypesSnippet += types[0] + ', '
    prodTypesSnippet = prodTypesSnippet[:-2]
        

    materialSnippet = ''
    if len(materialType) > 0:
        materialSnippet = 'I think this item is made of ' + list(materialType)[0] 
    else:
        materialSnippet = 'No mention of the material'

    productFacets = Facets(prodTypesSnippet, sentimentSnippet, materialSnippet)
    return productFacets


def main():
    products = parseProducts('Musical_Instruments_5.json')
    posWords = parseWords('positive.txt')
    negWords = parseWords('negative.txt')
    materials = parseWords('materials.txt')
    productType = parseProductType('productType.txt')
    asinDict = {}

    for product in products:
        if product.asin in asinDict:
            asinDict[product.asin].append(product)
        else:
            asinDict[product.asin] = [product]

    numProds = len(asinDict)

    for key in asinDict:
        for product in asinDict[key]:
            pprint(extractFacets(product.reviewText,
                                posWords,
                                negWords,
                                materials,
                                productType).returnDict())

if __name__ == "__main__":
    main()
