from flask import Flask, escape, request, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/ping')
def ping():
    return render_template('ping.html')
@app.route('/pong',methods=['GET','POST'])
def pong():
    #request.args => get방식으로 데이터가 들어올 때.
    #request.form => post방식으로 데이터가 들어올 때.
    #print(request.form.get('keyword'))
    #keyword=request.args.get('keyword')
    keyword=request.form.get('keyword')
    return render_template('pong.html',keyword=keyword)

@app.route('/naver')
def naver():
    return render_template('naver.html')

@app.route('/google')
def google():
    return render_template('google.html')


@app.route('/summoner')
def summoner():
    return render_template('summoner.html')

@app.route('/opgg')
def opgg():
    username=request.args.get('username')
    opgg_url=f"https://www.op.gg/summoner/userName={username}"
    res=requests.get(opgg_url).text
    soup=BeautifulSoup(res,'html.parser')
    tierrank=soup.find('div',{'class':'TierRank'}).text
    winlose=soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.sub-tier > div > div.sub-tier__league-point > span').text
    WL=winlose.replace('/','').replace('패','').strip().split('승')

    return render_template('opgg.html',username=username,tierrank=tierrank)


@app.route('/zara1')
def zara1():
    return render_template('zara1.html')

import re

@app.route('/zara2')
def zara2():
    product_name=request.args.get('product')
    url='https://www.zara.com/kr/ko/man-special-prices-l806.html?v1=1282748'
    source=BeautifulSoup(requests.get(url,'utf-8').text,'html.parser')
    product_list=source.select('ul.product-list>li')
    isproduct=re.compile(product_name)
    total_list=[]
    price_list=[]
    for product in product_list:
        if isproduct.search(product.text):
            total_list.append(product.text)
            #price_list.append(product.select_one('div.product-info>div.product-info-item-price>div._product-price>span.sale').text)
        else:
            print('얜 아니야')
    return render_template('zara2.html',product_name=product_name,contents=total_list)


if __name__ == '__main__':
    app.run(debug=True)