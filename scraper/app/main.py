import models
from fastapi import FastAPI,  Depends
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from models import  Leboncoin, Leboncoin_imgs
from sqlalchemy.orm import Session
import uvicorn
import requests
from bs4 import BeautifulSoup
from lxml import  etree
requests.packages.urllib3.disable_warnings()

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"Hello": "world"}
#app.include_router(items.router, prefix="/items")

@app.get("/annonce")
def get_imgs_from_leboncoin_annonce(leboncoinurl: str, db: Session = Depends(get_db)):
    leboncoin = Leboncoin()
    res = db.query(Leboncoin).filter(Leboncoin.url == leboncoinurl).first()
    res1 = db.query(Leboncoin_imgs).filter(Leboncoin_imgs.lbc_url == leboncoinurl).all()
    imgs =[]
    for e in res1:
        imgs.append(e.img)
    return {"price":res.price, "date":res.date, "url":res.url, "description":res.description, "imgs": imgs}


@app.get("/all")
def get_datas(db: Session = Depends(get_db)):
    leboncoin = db.query(Leboncoin)
    leboncoin_imgs = db.query(Leboncoin_imgs)
    #imgs_items = db.query(Leboncoin_imgs).join(Leboncoin, Leboncoin.url ==  Leboncoin_imgs.lbc_url, isouter=True).all()
    #return leboncoin.all(), imgs_items
    return leboncoin.all()

@app.get("/add_leboncoin_annonce")
async def create_meta_annonce(leboncoin_cookie: str, leboncoinurl: str, db: Session = Depends(get_db)):
    leboncoinurl= "https://www.leboncoin.fr/informatique/1908042491.htm"
    leboncoin_cookie = "didomi_token=eyJ1c2VyX2lkIjoiMTc2ZTgwNjAtZTM0MC02OWVjLTk3ZGYtZGZmMGU2ZTA0ZDY2IiwiY3JlYXRlZCI6IjIwMjEtMDEtMDlUMTY6NDE6NTIuMDg3WiIsInVwZGF0ZWQiOiIyMDIxLTAxLTA5VDE2OjQxOjUyLjA4N1oiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiYW1hem9uIiwic2FsZXNmb3JjZSIsImdvb2dsZSIsImM6bmV4dC1wZXJmb3JtYW5jZSIsImM6Y29sbGVjdGl2ZS1oaFNZdFJWbiIsImM6cm9ja3lvdSIsImM6cHVib2NlYW4tYjZCSk10c2UiLCJjOnJ0YXJnZXQtR2VmTVZ5aUMiLCJjOnNjaGlic3RlZC1NUVBYYXF5aCIsImM6Z3JlZW5ob3VzZS1RS2JHQmtzNCIsImM6cmVhbHplaXRnLWI2S0NreHlWIiwiYzp2aWRlby1tZWRpYS1ncm91cCIsImM6c3dpdGNoLWNvbmNlcHRzIiwiYzpsdWNpZGhvbGQteWZ0YldUZjciLCJjOmxlbW9tZWRpYS16YllocDJRYyIsImM6eW9ybWVkaWFzLXFuQldoUXlTIiwiYzpzYW5vbWEiLCJjOnJhZHZlcnRpcy1TSnBhMjVIOCIsImM6cXdlcnRpemUtemRuZ0UyaHgiLCJjOnZkb3BpYSIsImM6cmV2bGlmdGVyLWNScE1ucDV4IiwiYzpyZXNlYXJjaC1ub3ciLCJjOndoZW5ldmVybS04Vllod2IyUCIsImM6YWRtb3Rpb24iLCJjOndvb2JpIiwiYzpzaG9wc3R5bGUtZldKSzJMaVAiLCJjOnRoaXJkcHJlc2UtU3NLd21IVksiLCJjOmIyYm1lZGlhLXBRVEZneVdrIiwiYzpwdXJjaCIsImM6bGlmZXN0cmVldC1tZWRpYSIsImM6c3luYy1uNzRYUXByZyIsImM6aW50b3dvd2luLXFhenQ1dEdpIiwiYzpkaWRvbWkiLCJjOnJhZGl1bW9uZSIsImM6YWRvdG1vYiIsImM6YWItdGFzdHkiLCJjOmdyYXBlc2hvdCIsImM6YWRtb2IiLCJjOmFkYWdpbyJdfSwidmVuZG9yc19saSI6eyJlbmFibGVkIjpbImdvb2dsZSJdfSwidmVyc2lvbiI6MiwiYWMiOiJERTJBb0FFSUFmb0JoUUR4QUhtQVNTQWtzRGlBSFZnUkJnaWxCRlFDVGNFM2dKeUFXMWd1TUJnTURDSUdKb0FBLkRFMkFvQUVJQWZvQmhRRHhBSG1BU1NBa3NEaUFIVmdSQmdpbEJGUUNUY0UzZ0p5QVcxZ3VNQmdNRENJR0pvQUEifQ==; euconsent-v2=CO_wqAhO_wqAhAHABBENBHCgAP_AAH_AAAAAG7tf_X_fb2vj-_5999t0eY1f9_63v6wzjgeNs-8NyZ_X_L4Xo2M6vB36pq4KmR4Eu3LBAQdlHOHcTQmQwIkVqTPsbk2Mr7NKJ7LEilMbe2dYGH9_n8XTuZKY70_s___z_3-__v__7rbgCAAAAAAAIAgZ8ASYal8BAmJY4Ek0aVQogQhXEhUAoAKKEYWiawgJHBTsrgI_QQIAEBqAjAiBBiCjFgEAAAAASURACAHAgEQBEAgABACpAQgAIkAQWAEgYBAAKAaFgBFAEIEhBkcFRymBARItFBPIGAAQAAAA.f_gAD_gAAAAA; __Secure-Installid=58879c8d-57ca-4398-b3f8-0694ee18ff8f; uuid=ff476a38-300b-45b5-ac19-21d65156ae11; adview_clickmeter=similar_ads__adview____7cde44b3-5365-11eb-a465-6a226adcc0bf; datadome=PjmGEVt.J1ewO310yOmuNp_sBF1G9mDlkCvaod-zM8iMTHALx0v3Tohs-jURJgVx0vjkpK5pAmen2MbmFWnT-FmmYmtWkL5alExqoVOkGv"

    headers = {
        'Host': 'www.leboncoin.fr',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'If-None-Match': 'W/"1a14c-H2XwoC63JtnPC+35JTeN/Ydig20"',
        'Cache-Control': 'max-age=0'
    }
    headers.update({'Cookie': leboncoin_cookie})

    r = requests.get(leboncoinurl, verify=False, headers=headers, timeout=3)
    htmlparser = etree.HTMLParser(encoding='utf-8')
    tree = etree.HTML(r.content, parser=htmlparser)
    soup = BeautifulSoup(r.content,'html.parser')
    price = tree.xpath('//*[@id="grid"]/article/section/div[5]/div[2]/div[1]/span')[0].text
    titre = tree.xpath('//*[@id="grid"]/article/section/div[5]/div[1]/div[1]/h1')[0].text
    date = tree.xpath('//*[@id="grid"]/article/section/div[5]/div[3]/p')[0].text
    description = tree.xpath('//*[@id="grid"]/article/div[4]/div/div/div/span')[0].text.replace("\n"," ")
    imgs = []
    for img_tag in soup.find_all('img'):
        if "large" in img_tag.get('src') and img_tag.get('src') not in imgs:
            imgs.append(img_tag.get('src'))

    db = SessionLocal()
    leboncoin = Leboncoin()
    leboncoin.titre = titre
    leboncoin.price = price
    leboncoin.date = date
    leboncoin.url = leboncoinurl 
    leboncoin.description = description
    db.add(leboncoin)
    db.commit()

    for img in imgs:
        leboncoin_imgs = Leboncoin_imgs()
        leboncoin_imgs.lbc_url = leboncoinurl
        leboncoin_imgs.img = img
        db.add(leboncoin_imgs)
        db.commit()

    return titre, price, description, date, imgs

@app.get("/add_leboncoin_annonce2")
async def create_meta_annonce2(leboncoin_cookie: str, leboncoinurl: str, db: Session = Depends(get_db)):
    leboncoinurl= "https://www.leboncoin.fr/informatique/1800141207.htm"
    leboncoin_cookie = "didomi_token=eyJ1c2VyX2lkIjoiMTc2ZTgwNjAtZTM0MC02OWVjLTk3ZGYtZGZmMGU2ZTA0ZDY2IiwiY3JlYXRlZCI6IjIwMjEtMDEtMDlUMTY6NDE6NTIuMDg3WiIsInVwZGF0ZWQiOiIyMDIxLTAxLTA5VDE2OjQxOjUyLjA4N1oiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiYW1hem9uIiwic2FsZXNmb3JjZSIsImdvb2dsZSIsImM6bmV4dC1wZXJmb3JtYW5jZSIsImM6Y29sbGVjdGl2ZS1oaFNZdFJWbiIsImM6cm9ja3lvdSIsImM6cHVib2NlYW4tYjZCSk10c2UiLCJjOnJ0YXJnZXQtR2VmTVZ5aUMiLCJjOnNjaGlic3RlZC1NUVBYYXF5aCIsImM6Z3JlZW5ob3VzZS1RS2JHQmtzNCIsImM6cmVhbHplaXRnLWI2S0NreHlWIiwiYzp2aWRlby1tZWRpYS1ncm91cCIsImM6c3dpdGNoLWNvbmNlcHRzIiwiYzpsdWNpZGhvbGQteWZ0YldUZjciLCJjOmxlbW9tZWRpYS16YllocDJRYyIsImM6eW9ybWVkaWFzLXFuQldoUXlTIiwiYzpzYW5vbWEiLCJjOnJhZHZlcnRpcy1TSnBhMjVIOCIsImM6cXdlcnRpemUtemRuZ0UyaHgiLCJjOnZkb3BpYSIsImM6cmV2bGlmdGVyLWNScE1ucDV4IiwiYzpyZXNlYXJjaC1ub3ciLCJjOndoZW5ldmVybS04Vllod2IyUCIsImM6YWRtb3Rpb24iLCJjOndvb2JpIiwiYzpzaG9wc3R5bGUtZldKSzJMaVAiLCJjOnRoaXJkcHJlc2UtU3NLd21IVksiLCJjOmIyYm1lZGlhLXBRVEZneVdrIiwiYzpwdXJjaCIsImM6bGlmZXN0cmVldC1tZWRpYSIsImM6c3luYy1uNzRYUXByZyIsImM6aW50b3dvd2luLXFhenQ1dEdpIiwiYzpkaWRvbWkiLCJjOnJhZGl1bW9uZSIsImM6YWRvdG1vYiIsImM6YWItdGFzdHkiLCJjOmdyYXBlc2hvdCIsImM6YWRtb2IiLCJjOmFkYWdpbyJdfSwidmVuZG9yc19saSI6eyJlbmFibGVkIjpbImdvb2dsZSJdfSwidmVyc2lvbiI6MiwiYWMiOiJERTJBb0FFSUFmb0JoUUR4QUhtQVNTQWtzRGlBSFZnUkJnaWxCRlFDVGNFM2dKeUFXMWd1TUJnTURDSUdKb0FBLkRFMkFvQUVJQWZvQmhRRHhBSG1BU1NBa3NEaUFIVmdSQmdpbEJGUUNUY0UzZ0p5QVcxZ3VNQmdNRENJR0pvQUEifQ==; euconsent-v2=CO_wqAhO_wqAhAHABBENBHCgAP_AAH_AAAAAG7tf_X_fb2vj-_5999t0eY1f9_63v6wzjgeNs-8NyZ_X_L4Xo2M6vB36pq4KmR4Eu3LBAQdlHOHcTQmQwIkVqTPsbk2Mr7NKJ7LEilMbe2dYGH9_n8XTuZKY70_s___z_3-__v__7rbgCAAAAAAAIAgZ8ASYal8BAmJY4Ek0aVQogQhXEhUAoAKKEYWiawgJHBTsrgI_QQIAEBqAjAiBBiCjFgEAAAAASURACAHAgEQBEAgABACpAQgAIkAQWAEgYBAAKAaFgBFAEIEhBkcFRymBARItFBPIGAAQAAAA.f_gAD_gAAAAA; __Secure-Installid=58879c8d-57ca-4398-b3f8-0694ee18ff8f; uuid=ff476a38-300b-45b5-ac19-21d65156ae11; adview_clickmeter=similar_ads__adview____7cde44b3-5365-11eb-a465-6a226adcc0bf; datadome=PjmGEVt.J1ewO310yOmuNp_sBF1G9mDlkCvaod-zM8iMTHALx0v3Tohs-jURJgVx0vjkpK5pAmen2MbmFWnT-FmmYmtWkL5alExqoVOkGv"

    headers = {
        'Host': 'www.leboncoin.fr',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'If-None-Match': 'W/"1a14c-H2XwoC63JtnPC+35JTeN/Ydig20"',
        'Cache-Control': 'max-age=0'
    }
    headers.update({'Cookie': leboncoin_cookie})

    r = requests.get(leboncoinurl, verify=False, headers=headers, timeout=3)
    htmlparser = etree.HTMLParser(encoding='utf-8')
    tree = etree.HTML(r.content, parser=htmlparser)
    soup = BeautifulSoup(r.content,'html.parser')
    price = tree.xpath('//*[@id="grid"]/article/section/div[5]/div[2]/div[1]/span')[0].text
    titre = tree.xpath('//*[@id="grid"]/article/section/div[5]/div[1]/div[1]/h1')[0].text
    date = tree.xpath('//*[@id="grid"]/article/section/div[5]/div[3]/p')[0].text
    description = tree.xpath('//*[@id="grid"]/article/div[4]/div/div/div/span')[0].text.replace("\n"," ")
    imgs = []
    for img_tag in soup.find_all('img'):
        if "large" in img_tag.get('src') and img_tag.get('src') not in imgs:
            imgs.append(img_tag.get('src'))

    db = SessionLocal()
    leboncoin = Leboncoin()
    leboncoin.titre = titre
    leboncoin.price = price
    leboncoin.date = date
    leboncoin.url = leboncoinurl 
    leboncoin.description = description
    db.add(leboncoin)
    db.commit()

    db = SessionLocal()
    for img in imgs:
        leboncoin_imgs = Leboncoin_imgs()
        leboncoin_imgs.lbc_url = leboncoinurl
        leboncoin_imgs.img = img
        db.add(leboncoin_imgs)
        db.commit()
    return titre, price, description, date, imgs

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)