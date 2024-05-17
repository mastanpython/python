# import ssl
# orig_sslsocket_init = ssl.SSLSocket.__init__
# ssl.SSLSocket.__init__ = lambda *args, cert_reqs=ssl.CERT_NONE, **kwargs: orig_sslsocket_init(*args, cert_reqs=ssl.CERT_NONE, **kwargs)
from bs4 import BeautifulSoup 
import requests 
import pandas as pd
import re
url = 'https://www.skymarkinternational.com/' 
response = requests.get(url,verify=False)
soup = BeautifulSoup(response.text, 'html5lib')
headings = ['h1','h2','h3','h4'] 
paragraph = 'p'
image = 'img' 
link = 'a'
headerData = [] 
footer = {}
body = [] 
#https://www.skymarkinternational.com/product4.html#product5 
data = soup.find_all("section")
# print(data[3])
header = soup.find_all("header") 
def datawriter(data,dataType): 
    for i in data: 
        datainsert = {} 
        if i.find("h1"): 
            print(len(dataType))
            a=i.find("h1") 
            if a.find('a'):
                if len(dataType) == 0: 
                    datainsert['Content Title'] = a.find('a').text.strip() 
                    # datainsert['Anchor Name'] = a.a 
                else:
                    datainsert['Title'] = a.find('a').text.strip()
            else:
                if len(dataType) == 0: 
                    datainsert['Content Title'] = i.find("h1").text.strip()
                else:
                    datainsert['Title'] = i.find("h1").text.strip()
        if i.find("h2"): 
            a=i.find("h2")
            print(len(dataType))
            if a.find('a'):
                if len(dataType) == 0: 
                    datainsert['Content Title'] = a.find('a').text.strip() 
                    # datainsert['Anchor Name'] = a.a 
                else:
                    datainsert['Title'] = a.find('a').text.strip()
            else:
                if len(dataType) == 0:
                    print('len')
                    datainsert['Content Title'] = i.find("h2").text.strip() 
                else:
                    datainsert['Title'] = i.find("h2").text.strip()
        if i.find("h3"):
            a=i.find("h3")
            print(len(dataType))
            if a.find('a'):
                if len(dataType) == 0: 
                    datainsert['Content Title'] = a.find('a').text.strip() 
                    # datainsert['Anchor Name'] = a.a 
                else:
                    datainsert['Title'] = a.find('a').text.strip()
            else:
                if len(dataType) == 0: 
                    datainsert['Content Title'] = i.find("h3").text.strip()  
                else:
                    datainsert['Title'] = i.find("h3").text.strip()
        if i.find("p"): 
            if len(dataType) == 0:
                datainsert['Content Description'] = i.find("p").text.strip()
            else:
                datainsert['Description'] = i.find("p").text.strip()

        if i.find("img"): 
            image= i.find('img') 
            datainsert['Image'] = "https://www.skymarkinternational.com/"+image['src']
        Links = i.find_all("a")
         # print(Links)
        NumberOfLinks = 0
        LinkName = "Link" 
        for link in Links: 
            # print(link.a) 
            # print(link) 
            link_image = link.find("img") 
            if link_image == None: 
                # print("parent",link.parent)
                if link.parent.name not in ["h1","h2","h3"]: 
                    print('Text',link.text)
                    rex = re.match('[0-9A-Za-z]', link.text)
                    print(re.match('[0-9A-Za-z]', link.text)) 
                    if rex != None:
                        
                        if NumberOfLinks == 0:
                            datainsert[LinkName] = link 
                        else:
                            datainsert[LinkName + str(NumberOfLinks)] = link
                        # LinkName = LinkName + str(NumberOfLinks) 
                        NumberOfLinks = NumberOfLinks+1 
        dataType.append(datainsert) 
datawriter(data,body) 
# datawriter(header,headerData) 
# print(body) 
# print(headerData) 
DataText = open("data.txt",'w') 
for data in body: 
    for key in data: 
        DataText.write(f"{key}:{data[key]}\n")
DataText.close()


pageJsonData = {
    "Page URL": "https://www.skymarkinternational.com/",
    "Page Category" : "Home",
    "Component Name": [],
    "Field Name": [],
    "Content": []

}

component_name = []
Field_Name = []
Content = []


for i in body:
    # print(i)
    if len(component_name) == 0:
        datalen = len(i.keys())-1
        print(len(i.keys())-1)
        component_name.append("Header Medium with Description")
        for j in range(0,datalen):
            component_name.append(''*datalen)
        for k in i:
            Field_Name.append(k)
            Content.append(i[k])

        
    else:
        component_name.append("Sub Item: Page Overview Item")
        datalen = len(i.keys())-1
        for j in range(0,datalen):
            component_name.append(''*datalen)
        for k in i:
            Field_Name.append(k)
            Content.append(i[k])

# print(component_name)

pageJsonData['Component Name'] = component_name
pageJsonData['Field Name'] = Field_Name
pageJsonData['Content'] = Content


# print(pageJsonData)

myvar = pd.DataFrame(pageJsonData)
myvar.to_excel('data.xlsx', index=False)
# print(myvar)

        






