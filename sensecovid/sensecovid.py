from Credibility import Credibility_Analysis
from flask import Flask, jsonify, request, render_template
from datetime import timezone, timedelta, datetime
import json
import os

app = Flask(__name__,
            static_folder='../',  # Open resource access for this path
            static_url_path='')

content_words = ''
content_url = ''
result = ''
score = ''
fake = ''
now = ''
once_before = ''

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/test')
def ie():
    return render_template('component-notifications.html')

@app.route('/sentiment')
def sentiment_page():
    filePath = '../backend/result/daily_senti_results'
    folders = os.listdir(filePath)
    folders.sort()
    for folder in folders:
        ff = str(filePath+'/'+folder)
        files = os.listdir(ff)
        if len(files) == 0:
            empty_folder = folder
    folders.remove(empty_folder)

    return render_template('sentiment.html',day_ids=folders,day_active=folders[0])

@app.route('/sentiment', methods=['POST'])
def sentiment_request():
    filePath = '../backend/result/daily_senti_results'
    folders = os.listdir(filePath)
    folders.sort()
    for folder in folders:
        ff = str(filePath+'/'+folder)
        files = os.listdir(ff)
        if len(files) == 0:
            empty_folder = folder
    folders.remove(empty_folder)
    
    if request.method == 'POST':
        # print(request.form)
        tab = request.form["tab_number"]        # day_id : '2020-12-23'

    return render_template('sentiment.html',day_ids=folders,day_active=tab)

@app.route('/story')
def story_page():
    s = open('../backend/result/sum_updates/latest_sum.json','r')
    s_read = s.read()
    text_sum = json.loads(s_read)
    s.close()

    utc = timezone.utc                                  # Get UTC Time Zone Object
    utc_time = datetime.utcnow().replace(tzinfo=utc)
    America = timezone(timedelta(hours=-4))
    print(America)
    time_usa = utc_time.astimezone(America)
    time_str = datetime.strftime(time_usa,'%Y-%m-%d %H:%M:%S')
    # curr_time = datetime.now()
    # now = curr_time.strftime("%Y-%m-%d %H:%M:%S")
    news = text_sum["News"]
    opinion = text_sum["Opinions"]
    tweets = text_sum["Tweets"]
    return render_template('story.html', news_story = news, opinion_story = opinion, tweets_content = list(tweets), last_update_time = time_str)


@app.route('/user_tagged_history')
def tagged_record():
    f = open('./static/data/user_tagged.json','r')
    f_his = f.read()
    tagdata = json.loads(f_his)
    f.close()
    return render_template('user_tagged_history.html', user_tags = tagdata)

@app.route('/credibility_history')
def history_record():
    f = open('./static/data/cre_his.json','r')
    f_his = f.read()
    hisdata = json.loads(f_his)
    f.close()
    return render_template('credibility_history.html', history_credibility = hisdata)

@app.route('/credibility')
def redirect_credibility():
    return render_template('credibility.html')
    

@app.route('/credibility', methods=['POST'])
def testpost():
    # POST request
    if request.method == 'POST' and request.form["query"] == "key1":
        content = request.form["tweet_content"]        # tweet content
        
        # format the content
        url_posi = content.find('http')
        if url_posi != -1:
            content_words = content[ : url_posi]
            content_url = content[url_posi : ]
        else:
            content_words = content
            content_url = ''

        # tell if the content is analyzed before
        f = open('./static/data/cre_his.json','r')
        f_read = f.read()
        his = json.loads(f_read)
        f.close()
        for k, v in his.items():
            if content_words in v["content"]:
                # Get the history result
                once_before = "This tweet is analyzed before, the sequence number is: " + k
                result = v["result"]
                score = v["score"] 
                fake = v["fake"]
                real = v["real"]
                now = v["time"]
                flag = 0
            else:
                flag = 1

        if flag==1:
            # Get the analyze result
            once_before = ""
            Cred_Model = Credibility_Analysis('./Credibility/Cred_Eval_model.pkl')
            result, score, (fake, real) = Cred_Model.Evaluate(text = str(content), only_score = False)
            score = round(score,2) * 100
            fake = round(fake, 2)
            real = round(real, 2)

            # update local history file
            curr_time = datetime.now()
            now = curr_time.strftime("%Y-%m-%d %H:%M:%S")  # analyze time
            l = len(his)
            his[str(l+1)] = {"content":str(content), "score":score , "time":now, "fake":fake, "real":real, "result":result}
            f1 = open('./static/data/cre_his.json','w')
            json.dump(his, f1)
            f1.close() 
        return render_template('credibility.html', tweet_content=content_words, tweet_url = content_url,
                        str_result = "This tweet is highly likely to be " + result, credi_score=score, 
                        fake_num = "Fake confidence: " + str(fake), real_num = "Real confidence: " + str(real), 
                        ana_time = "Analyzed at " + str(now), if_analyzed_before = once_before)

    # # user submit tweet url and tag                    
    if request.method == 'POST' and request.form["query"] == "key2":
        url = request.form["url"]        # tweet url
        tag = request.form["tag"]        # user's tag     
        
        h = open('./static/data/user_tagged.json','r')
        user_his = json.loads(h.read())
        h.close()
        
        for k, v in user_his.items():
            if url == v["url"]:
                return render_template('credibility.html', submitted_flag = 'false')
            if url == '':
                return render_template('credibility.html', submitted_flag = 'false2')
        le = len(user_his)
        user_his[str(le+1)] = {"url": url, "tag": tag}
        h = open('./static/data/user_tagged.json','w')
        json.dump(user_his, h)
        h.close()

        return render_template('credibility.html', submitted_flag = 'true')


if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=80) # Broadcasting Through port 80
    # , host='0.0.0.0', port=80)