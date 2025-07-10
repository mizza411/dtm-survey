from flask import Flask, request, render_template_string, redirect
import csv
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SURVEY_FILE = 'survey_results.csv'

@app.route('/', methods=['GET'])
def form():
    # Serve the survey form HTML from the local directory
    with open('dtm_survey_form.html', encoding='utf-8') as f:
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
        reader = csv.DictReader(f)
        responses = list(reader)
    if not responses:
        return '<h2>No results yet.</h2>'
    html = '<h2>Survey Results</h2>'
    for i, row in enumerate(responses):
        html += '<div style="border:1px solid #aaa; border-radius:8px; margin:20px 0; padding:16px; background:#fafbfc; max-width:700px;">'
        html += f'<h3>Response {i+1}</h3>'
        for key, value in row.items():
            if value.strip():
                html += f'<div style="margin-bottom:8px;"><b>{key}:</b> {value}</div>'
        html += '</div>'
    html += '<br><a href="/">Back to form</a>'
    return html

if __name__ == '__main__':
    app.run(debug=True) 
