import numpy as np
import json 
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
import matplotlib.pyplot as plt


def find_features_within_categories(flc,featureDict,categories):
    st = LancasterStemmer()
    words_f = []
    flav_wrds =  word_tokenize(flc)
    for i in flav_wrds:
        try:
            if i.lower() not in words_f:
                words_f.append(i.lower())
            if st.stem(i.lower()) not in words_f:
                    words_f.append(st.stem(i.lower()))  
        except:
            pass   
        
    features = []
    category = []
    catvector  = []
    featurevector = []
    featureslider = 0
    for i in categories:
        if len(set(words_f).intersection(featureDict[i])) !=0:
            features = features + list(set(words_f).intersection(featureDict[i]))
            category.append(i)
            catvector.append(len(set(words_f).intersection(featureDict[i])))
            featurevector = featurevector  + list(np.zeros(len(featureDict[i])))
            for notesC in featureDict[i]:
                if notesC in words_f:
                    featurevector[featureslider + featureDict[i].index(notesC)] = 1
                    for ni in range(featureslider,featureslider+len(featureDict[i])):
                        if featurevector[ni] != 1:
                            featurevector[ni] = featurevector[ni] + 1./len(featureDict[i])
                    featurevector[featureslider + featureDict[i].index(notesC)] = 1
        else:
            featurevector = featurevector  + list(np.zeros(len(featureDict[i])))
            catvector.append(0)
        featureslider = featureslider + len(featureDict[i])
    return features, category,featurevector, catvector




#####################################################################


with open('JR_scraped.json') as cig_file:
    data= json.load(cig_file)

cig_file.close()



name = []
for i in data.keys():
    name.append(i.lower())


    
fl = []    
for i in data:
    fl.append(data[i]['MainDescription'])
    fl.append(data[i]['description'])


# cigar attributes



# cigar attributes
STRNGTH = ['Mild','Mild - Medium','Medium','Medium - Full','Full']

categories_notes = {'flowers':['tulips','violets','bouquet','flowers','floral','herbaceous','herbal','hay','haylike'], 
                    'plants':['grass','grassy','moss','tea','vegetal'], 
                    'wood':['cedar','cedary','oak','smoky','wood','woody','woodsy','woodiness'],
                    'spices':['spice','spiciness','spicy','spices','anice','licorice','cardamon','nutmeg','pepper','peppery','cinnamon','clove','cloves','cumin','cayenne','chili','allspice'],
                    'earth':['barnyard','earth','earthy','earthy/peaty','earthiness'],
                    'minerals':['lead','graphite','mineral','musk','musty','salt','salty','saltiness','savory'],
                    'fruit':['Watermelon','peach','currant','fruity','fruit','mango','pineapple','apple','raisin','plum','cherry','cherries','berry','orange','zest','citrus','lemon'],
                    'nuts':['walnut','peanut','marzipan','cashew','almond','nut','nuts','nuttiness','nutty','hazelnut','praline'],
                    'feint':['leather','leathery','honey','beewax','cream','mead'],
                    'chocolate':['cocoa','chocolate','chocolately','chocolaty','cream','butter','milky','creamy','creaminess'],
                    'coffee':['espresso','coffee/mocha','coffee','mocha','roasted'],
                    'vanilla':['caramel','custard','toffee','butterscotch'],
                    'cereal':['bran','bread','oat','barley','yeasty','husky']}

MainNotes = ['flowers','plants','wood','spices','earth','minerals','fruit','nuts','feint','chocolate','coffee','vanilla','cereal']



notes_list = []
notesV_list = []
notescategory_list = []
notescategoryV_list = []
for i in fl:
    notes, notescategory,notesV,notescategoryV = find_features_within_categories(i,categories_notes,MainNotes)
    notes_list.append(notes)
    notescategory_list.append(notescategory)
    notescategoryV_list.append(notescategoryV)
    notesV_list.append(notesV)
    

dataStr = {}
k=0
for i in data:
    if len(notes_list[k]) !=0 and data[i]['Strength'] in STRNGTH:
        dataStr[i] = {}
        dataStr[i]['name'] = str(i)
        notes = ''
        for nts in notes_list[k]:
            notes = notes + nts
            if nts != notes_list[k][-1]:
                notes = notes + ', '
        dataStr[i]['notes'] = notes
        dataStr[i]['description'] = data[i]['MainDescription']
        dataStr[i]['wrapper type'] = data[i]['WrapperType']
        dataStr[i]['origin'] = data[i]['Origin']
        dataStr[i]['wrapperColor'] = data[i]['WrapperColor']
        dataStr[i]['binder'] = data[i]['Binder']
        dataStr[i]['filler'] = data[i]['Filler']
        dataStr[i]['brand'] = data[i]['brand']
        dataStr[i]['detailed descriptions'] = data[i]['description']
        dataStr[i]['link'] = str(data[i]['link']) 
        dataStr[i]['image'] = str(data[i]['image'])
        categories = ''
        for nts in notescategory_list[k]:
            categories = categories + nts 
            if nts != notescategory_list[k][-1]:
                categories = categories + ', '
        dataStr[i]['note categories'] = categories
        dataStr[i]['note vector'] = notesV_list[k]
        dataStr[i]['strength'] = data[i]['Strength']
        strengthV = np.zeros(5)
        strengthV[STRNGTH.index(data[i]['Strength'])] = 1
        dataStr[i]['strength vector'] = list(strengthV)
        
        
    k=k+1

with open('JR_CigarStructured.json', 'w') as ff:
    json.dump(dataStr, ff)
    
ff.close()


#with open('JR_CigarStructured.json', 'w') as ff:
#    json.dump(dataStr, ff)

