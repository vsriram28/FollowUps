from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler 
from dotenv import load_dotenv
from datetime import datetime 
import re 

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
mongo_client = MongoClient("localhost",27017)
db = mongo_client["notes-db"]
current_date = datetime.today().strftime("%m/%d/%Y")
temp_date =''
pattern = r'#([A-Za-z0-9\-\_]+):'

# function to write to the table
def write_to_db_table(content, tags):
    global temp_date
    date = temp_date

    existing_doc = db['notes'].find_one({'date': date})
    if existing_doc:
        print('   -----Existing date--------   ')
        print(content, '\n', tags)
        print('   --------------------------   ')
        db['notes'].update_one(
            {'date': date},
            {'$set': {'content': content, 'tags': tags}}
        )
    else:
        print('   -----New date--------   ')
        print(content, '\n', tags)
        print('   --------------------------   ')
        db['notes'].insert_one(
            {
                'date': date,
                'content': content,
                'tags': fetch_tags
            }
        )

# take the content from the autosaved markdown file and save it in table
def write_editor_content_to_databse():
    global temp_date
    print('selected date is: ', temp_date)

    with open('autosaved_markdown.md','r') as file:
        content = file.read()
        tags = re.findall(pattern, content)
        # print (tags)
        contents = re.findall(r':(.*?)[.]', content)
        # print(contents)
        todos = []
        completed = []
        for i,j in enumerate(tags):
            if contents[i]:
                stuff = contents[i].strip()
            # else:
                # continue
                if j.casefold() == 'todo'.casefold():
                    todos.append(stuff)
                else:
                    completed.append(stuff)
        tags = {'todo': todos, 'completed': completed}
        write_to_db_table(content, tags)

# Main function to start the app
# if there is any data existing for the current date in the database
# show it. If not, insert today as a new date and present the clear editor.
@app.route('/')
def index():
    global current_date
    query_date = current_date 
    record = db['notes'].find_one({'date':query_date})
    date_content = "Type your content here..."
    if record:
        date_content = record['content']
    else:
        new_record = db['notes'].insert_one(
            {
                'date': query_date,
                'content': '',
                'tags': {
                    'todo': [],
                    'completed': []
                }
            }
        )

    return render_template('index_G.html', contetnt=date_content, date=query_date)

# save the content being typed into the editor in a local temo file
@app.route('/save', methods=['POST'])
def save():
    markdown_content=request.form['markdown_content']
    with open('autosaved_markdown.md','w') as file:
        file.write(markdown_content)
    return '',204

# get all tags and dates from the database
@app.route('/fetch_tags', methods=['POST'])
def fetch_tags():
    tag = request.json['tag']
    todos = []
    dates = []

    # get all docs from the table
    cursor = db['notes'].find({}).sort('date', -1)
    for document in cursor:
        date = document['date']
        if 'tags' in document and 'todo' in document['tags'] and document['date'] != '':
            todos.extend(document['tags']['todo'])
            dates.extend([date for i in document['tags']['todo']])
    return jsonify({'todos': todos, 'dates': dates})

@app.route('/fetch_completes', methods=['POST'])
def fetch_completes():
    tag = request.json['tag']
    todos = []
    dates = []
    # Fetch all documents from the table
    cursor = db['notes'].find({}).sort('date', -1)
    for document in cursor:
        date = document['date']
        if 'tags' in document and 'completed' in document['tags'] and document['date'] != '':
            todos.extend(document['tags']['completed'])
            dates.extend([date for i in document['tags']['completed']])
    return jsonify({'todos': todos, 'dates': dates})


# =================== Generic API calls used ==================== #
@app.route('/api/date', methods=['GET'])
def get_date():
    data = db['notes'].find({}, {'date': 1, '_id': 0}).sort('date', -1)
    date_list = [record['date'] for record in data if record['date'] != '']
    return jsonify({'dates': date_list})

@app.route('/get_date_text', methods=['POST'])
def get_date_text():
    global current_date
    global temp_date 
    data = request.json 
    current_date = data['date']
    temp_date = current_date 
    text = db['notes'].find({'date': current_date}, {'content': 1, '_id':0})
    text = [doc['content'] for doc in text]
    text = ''.join(text)
    print(f'text is: {text} for the date: {current_date}')
    with open('autosaved_markdown.md','w') as file:
        file.write(text)
    return jsonify({'text': text})

@app.route('/api/default_content', methods=['GET'])
def default_content():
    global current_date
    date = current_date
    data = db['notes'].find({'date': date}, {'content': 1, '_id': 0})
    content = 'Type your notes here ...'
    try:
        content1 = [i['content'] for i in data]
        content1 = ''.join(content1)
        if (len(content1.strip()) > 0):
            content = content1
    except:
        print('No content present')
    return jsonify({'content': content})



# =================== main =======================#
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(write_editor_content_to_databse, 'interval', minutes=1)
    scheduler.start()
    app.run(debug=True)
