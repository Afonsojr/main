# coding: utf-8

import requests
from bs4 import BeautifulSoup
from pydal import DAL, Field


db = DAL('sqlite://storage.db')

Dicio = db.define_table('dicio',
                Field('palavra', type='string'),
                Field('significado', type='text'),
                Field('sinonimo', type='string'),
                Field('antonimo', type='string'),
                Field('classe_gramatical', type='string'),
                Field('separacao_silabica', type='string'),
                #Field('', type='string'),
                Field('plural', type='string'),
                Field('frase', type='text'),
                Field('anagrama', type='string'),
                
               )


def crawler(link):
    url = 'https://www.dicio.com.br%s' % link
    
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html5lib')
    
    content = soup.find('div', {'id':'content'})
    #print len(content)
    #print content.prettify()
    #Palavra
    palavra = content.find('h1', {'itemprop':'name'}).text 

    try:
        #Significado
        significado = ''
        for i in range(len(content.find('p',{'class':'significado textonovo'}).find_all('span'))):
            significado += content.find('p',{'class':'significado textonovo'}).find_all('span')[i].text
            significado += '\n'
    except:
        significado = "Nao informado"

    try:
        #Sinonimos esta retornando uma lista
        sinonimo = ''
        for i in range(len(content.find_all('p',  {'class':"adicional sinonimos"})[0].text.split(':')[1].split(','))):
            sinonimo += content.find_all('p',  {'class':"adicional sinonimos"})[0].text.split(':')[1].split(',')[i]
    except:
        sinonimo = 'Nao informado'


    try:
        #antonimos esta retornando uma lista
        antonimo = ''
        for i in range(len(content.find_all('p',  {'class':"adicional sinonimos"})[1].text.split(':')[1].split(','))):
            antonimo += content.find_all('p',  {'class':"adicional sinonimos"})[1].text.split(':')[1].split(',')[i]
    except:
        antonimo = 'Nao informado'

    try:
        #Classe gramatical
        classe_gramatical = content.find_all('p',  {'class':"adicional"})[2].find_all('b')[0].text
    except:
        classe_gramatical = 'Nao informado'

    try:
        #Separacao silabica
        separacao = content.find_all('p',  {'class':"adicional"})[2].find_all('b')[1].text
    except:
        separacao = 'Nao informado'

    try:
        #plural
        plural = content.find_all('p',  {'class':"adicional"})[2].find_all('b')[2].text.replace(' ', '')
    except:
        plural = 'Nao informado'

    try:
        #Frase
        frase = ''
        for fra in range(len(content.find_all('div',  {'class':"frases"})[0].find_all('div'))):
            frase += content.find_all('div',  {'class':"frases"})[0].find_all('div')[fra].text
            frase += '\n\n' 
    except:
        frase = 'Nao informado'

    try:
        anagrama = ''
        for ana in range(len(content.find_all('ul',  {'class':"list col-4 small"})[1].find_all('li'))):
            anagrama +=content.find_all('ul',  {'class':"list col-4 small"})[1].find_all('li')[ana].text
            anagrama += ' '
    except:
        anagrama = "Nao Informado."
    
    link = soup.find('div', {'id':'word-nav'}).find_all('a')[2].get('href')
    with open('log.log', 'w') as fil:
        fil.write(link)
    
    Dicio.insert(palavra = palavra,
                 significado = significado,
                 sinonimo = sinonimo,
                 antonimo = antonimo,
                 classe_gramatical = classe_gramatical,
                 separacao_silabica = separacao,
                 plural = plural,
                 frase = frase, 
                 anagrama = anagrama)
    
    #Commit
    db.commit()
    print link
    #crawler(link)

if __name__ == '__main__':
    while True:
        with open('log.log', 'r') as fil:
            file = fil.read()

        crawler(file)


