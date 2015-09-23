from bs4 import BeautifulSoup
import urllib2
import json

################
rooturl = "http://www.jrcigars.com"
url = rooturl + "/handmade-cigars"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
list = soup.find("div",{"class":"brand-list-content"})

htmlDic = []
data = {}
number = 0
nameList = []
LinkList = []
for link in list.findAll("p"):
    res = link.find("a").get('href')
    name = link.find("a").get('name')
    if len(res.split('/')) >3:
        LinkList.append(rooturl+res)
        nameList.append(name)
dltd = 0        
num=0
for cigLink in LinkList: #back to 2
    cigName = nameList[LinkList.index(cigLink)]
    cPage = urllib2.urlopen(cigLink)
    cSoup = BeautifulSoup(cPage.read())
    
    data[cigName]={}
    data[cigName]['link'] = cigLink
    data[cigName]['brand'] = cigLink.split('/')[-2].replace('-',' ')

    if data[cigName]['brand'] == 'www.jrcigars.com':
        data[cigName]['brand'] = 'N/A'
            
    try:
        cContent = cSoup.find("div", {"id":"category-desc"}).get_text()
        data[cigName]['MainDescription'] = cContent
    except:
        data[cigName]['MainDescription'] = 'N/A'
    description = ''
    image = []
    Ring = []
    Shape = []
    WrapperType  = []
    WrapperColor  = []
    Binder = []
    Filler = []
    Origin = []
    Strength = []
    WrapperColor = []
    flag = 0
    ####### Lists for image and all features.
    ex = cSoup.findAll("div", {"class":"col-sm-3 col-xs-6"})
    for item in ex:
        try:
            exLink =rooturl+item.find("a").get('href')+'#read-more'
            exPage = urllib2.urlopen(exLink)
            exSoup = BeautifulSoup(exPage.read())       
            description = description + (exSoup.find("div",{"itemprop":"description"}).get_text())
            image.append(rooturl+exSoup.find("meta",{"itemprop":"image"}).get('content'))
            details = exSoup.find("div",{"class":"cigar-details"})
            Ring.append(details.findAll("p")[0].get_text())
            WrapperType.append(details.findAll("p")[-6].get_text())
            if details.findAll("p")[-6].get_text() != WrapperType[0]:
                flag = 1
            Binder.append(details.findAll("p")[-5].get_text())
            if details.findAll("p")[-5].get_text() != Binder[0]:
                flag = 1
            Filler.append(details.findAll("p")[-4].get_text())
            if details.findAll("p")[-4].get_text() != Filler[0]:
                flag = 1
            Origin.append(details.findAll("p")[-3].get_text())
            if details.findAll("p")[-3].get_text() != Origin[0]:
                flag = 1
            Strength.append(details.findAll("p")[-2].get_text())
            if details.findAll("p")[-2].get_text() != Strength[0]:
                flag = 1
            WrapperColor.append(details.findAll("p")[-1].get_text())
            if details.findAll("p")[-1].get_text() != WrapperColor[0]:
                flag = 1
            if details.findAll("p")[-7].get_text() != details.findAll("p")[0].get_text():
                Shape.append(details.findAll("p")[-7].get_text())
            else:
                Shape.append('N/A')
        except:
            flag = 1
            
    if flag == 0:
        data[cigName]['description'] = description
        data[cigName]['image'] = image[Ring.index(max(Ring))]
        data[cigName]['Ring'] = Ring[Ring.index(max(Ring))]
        data[cigName]['Shape'] = Shape[Ring.index(max(Ring))]
        data[cigName]['WrapperType'] = WrapperType[0]
        data[cigName]['WrapperColor'] = WrapperColor[0]
        data[cigName]['Binder'] = Binder[0]
        data[cigName]['Filler'] = Filler[0]
        data[cigName]['Origin'] =Origin[0]
        data[cigName]['Strength'] =Strength[0]
        data[cigName]['WrapperColor'] =WrapperColor[0]
    else:
        del data[cigName]
        dltd = dltd+1
        print 'the following is deleted %s'%(dltd)
            
    num=num+1
    print num

