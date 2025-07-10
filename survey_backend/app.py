from flask import Flask, request, render_template_string, redirect
import csv
import os

app = Flask(__name__)

SURVEY_FILE = 'survey_results.csv'

@app.route('/', methods=['GET'])
def form():
    # Serve the survey form HTML (update the path if needed)
    with open('../digital trust mark/dtm_survey_form.html', encoding='utf-8') as f:
        return f.read()

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    file_exists = os.path.isfile(SURVEY_FILE)
    with open(SURVEY_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
    return render_template_string('<h2>Thank you! Your response has been recorded.</h2><a href="/">Submit another</a> | <a href="/results">View all results</a>')

@app.route('/results', methods=['GET'])
def results():
    if not os.path.isfile(SURVEY_FILE):
        return '<h2>No results yet.</h2>'
    with open(SURVEY_FILE, encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    html = '<h2>Survey Results</h2><table border="1">'
    for i, row in enumerate(rows):
        html += '<tr>' + ''.join(f'<th>{cell}</th>' if i == 0 else f'<td>{cell}</td>' for cell in row) + '</tr>'
    html += '</table><br><a href="/">Back to form</a>'
    return html

if __name__ == '__main__':
    app.run(debug=True) 
