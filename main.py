# by billy willy =3 - 22/03/2023
# On loading, it will go to https://nftrade.com/marketplace, and select the 1st NFT. It will load that ones page, and
# copy or save the image. This will then be shown to the user and basically presented as if it were thier own NFT
# This is also going to be your unique flappy bird lol

import re

from selenium import webdriver
from selenium.webdriver.chrome import options
from bs4 import BeautifulSoup
import urllib.request
import os

LinksKey = re.compile(r'src="\S+"') # gets the links to images in beautiful soup list
adressKey = re.compile(r'https?:\/\/.+[\.svg|\.webp|\.png|\.jpg]') # Gets individual web adresses
extentionKey = re.compile(r'\.svg|\.webp|\.png|\.jpg')  # Gets common pic file extentions

#gets all of the front page images on NFT.com link (the ones that don't require scrolling to Load)
def GetNFT(URL):
    #higestPriceurl='https://nftrade.com/marketplace?search=&sort=min_price_desc'

    print('Setting up Headless browser')
    higestPriceurl=URL
    headlessBrowserOptions = options.Options()
    headlessBrowserOptions.add_argument("--headless")
    headlessBrowser = webdriver.Chrome(options=headlessBrowserOptions)
    headlessBrowser.get(higestPriceurl)

    print('Downloading HTML data')
    pagehtml = headlessBrowser.page_source
    # Download html data with JS loaded in
    with open('html.html','w',encoding="utf-8") as pageData:
            pageData.write(pagehtml)

    clickables = None
    print('Souping')
    with open('html.html','r') as html:
        soup = BeautifulSoup(html,'lxml')
        clicklables = soup.findAll('a')

    # save all <a> links (they contain hyperlinks for each nft image)
    print('Saving all links')
    with open('Links.txt','w') as links:
        for listing in clicklables:
            print(f'Link Tag: {listing}')
            links.write(str(listing))
            links.write('\n') # needs newlines for ezier combing of data in analyze()

def analyze(saveDir):
    htmlDocText = open('Links.txt','r')
    
    # get all link tags
    linktext = []
    for line in htmlDocText:
        result = LinksKey.findall(line)
        if len(result) != 0:
            linktext.append(result[0])

    # get all links from the individual tags
    finalList = []
    for link in linktext:
        final = adressKey.findall(link)
        finalList.append(final)

    # To download these images we need an opener with certian settings
    # this will stop links from blocking python urllib, which is a known blocked bot when it requests stuff from a website

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    # download all links
    for i,image in enumerate(finalList):
        # feedback 
        print(f'/______________________________________/{i}/______________________________________/')
        if len(image) !=0:
            # get the extention. not used but if you wanted to save a gif, just throw an if statement in
            # extention = extentionKey.findall(image[0])  

            urllib.request.urlretrieve(image[0],f'{saveDir}/{i}.png')   # save image
            print(f'saved image {image}')   # feedback


if __name__ == "__main__":
    # Using this will generate a folder with frontpage NFTs from link below into a folder called "NFTs"
    # It will also generate a HTML file, so you can look at its structure yourself, and a txt file
    # with all of the image links found from the HTML document
    nftSite = 'https://nftrade.com/marketplace?search=&sort=min_price_desc'
    GetNFT(nftSite)
    if not os.path.isdir('NFTs'):
        os.mkdir('NFTs')
    analyze('NFTs')