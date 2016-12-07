import os
import requests
from pymongo import MongoClient
import datetime

MONGO_HOST = os.getenv('MONGO_HOST','127.0.0.1')
MONGO_PORT = os.getenv('MONGO_PORT',27017)
DB_NAME = 'paper'

client = MongoClient(MONGO_HOST, int(MONGO_PORT))
db = client[DB_NAME]

def downloadImage():
    matchings = db.yoho_valid_matchings
    for matching in matchings.find({}):
        match_id = matching['_id']
        items = db.yoho_items.find({'matching.id': match_id})
        for item in items:
            id = str(item['_id'])
            category = item['category']
            img_url = 'http:'+item['img_url']
            dst_dir = '../images/'+match_id+'/'+category
            dst_name = id+'.jpg'
            filename = dst_dir + '/' + dst_name
            if os.path.exists(filename):
                continue
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            try:
                page = requests.get(img_url)
                with open(filename, 'wb') as image:
                    image.write(page.content)
                    print 'download completed:' + id
            except:
                print '\n Error when downloading'


if __name__=="__main__":
    print "*** begin download image ***"
    downloadImage()
    print "*** end image downloading ***"
