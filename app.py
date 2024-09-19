from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask_cors import CORS
app = Flask(__name__, static_url_path='/static')
CORS(app)

# MongoDB 설정
try:
    client = MongoClient("mongodb://1111:1111@localhost:27017/"
    , connectTimeoutMS=60000,  # 60초로 연결 타임아웃 설정
    socketTimeoutMS=60000)    # 60초로 소켓 타임아웃 설정

    db = client.articles
    print("MongoDB 연결 성공")
except Exception as e:
    print(f"MongoDB 연결 실패: {e}")

@app.route('/')
def home():
    return render_template('index.html')

# 메모 데이터 추가
@app.route('/', methods=['POST'])
def postArticle():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    print(f"Received URL: {url_receive}, Received Comment: {comment_receive}")  # Flask 콘솔에 출력

    # meta 태그 스크래핑
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')

    url_image = og_image['content'] if og_image else 'https://via.placeholder.com/150'
    url_title = og_title['content'] if og_title else 'No Title'

    article = {
        'url': url_receive,
        'title': url_title,
        'image': url_image,
        'comment': comment_receive
    }

    # MongoDB에 데이터 삽입
    db.articles.insert_one(article)

    # 삽입 확인 (방금 삽입한 데이터 조회)
    inserted_article = db.articles.find_one({'url': url_receive, 'comment': comment_receive})

    if inserted_article:
        return jsonify({'result': 'success', 'message': 'Article added and confirmed in the database', 'article': inserted_article})
    else:
        return jsonify({'result': 'fail', 'message': 'Failed to add article'})

# 저장된 메모 데이터 가져오기
@app.route('/', methods=['GET'])
def readArticles():
    articles = list(db.articles.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'articles': articles})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
    

    
