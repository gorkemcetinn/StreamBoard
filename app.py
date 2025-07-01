from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import csv
import io
from flask import make_response


app = Flask(__name__)
CORS(app)

# Bellekteki kullanıcılar: her biri dict
users = []

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json() or {}
    # Beklediğimiz tüm alanlar:
    expected = ('first_name','last_name','fullname','email','gender','country','age')
    if not all(k in data for k in expected):
        return jsonify({'message': 'Eksik alan'}), 400

    users.append({
        'first_name': data['first_name'],
        'last_name':  data['last_name'],
        'fullname':   data['fullname'],
        'email':      data['email'],
        'gender':     data['gender'],
        'country':    data['country'],
        'age':        data['age']
    })
    return jsonify({'message':'Eklendi'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    # Artık tam nesne listesi dönsün
    return jsonify(users)

@app.route('/last_user', methods=['GET'])
def last_user():
    if not users:
        return jsonify({}), 204
    return jsonify(users[-1])

@app.route('/stats', methods=['GET'])
def stats():
    male = sum(1 for u in users if u['gender'] == 'male')
    female = sum(1 for u in users if u['gender'] == 'female')
    return jsonify({'male': male, 'female': female})

@app.route('/export/csv', methods=['GET'])
def export_csv():
    # Başlık satırı + user objelerinden sıra ile veri
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Full Name', 'Email', 'Gender', 'Country', 'Age'])
    for u in users:
        writer.writerow([u['fullname'], u['email'], u['gender'], u['country'], u['age']])
    
    resp = make_response(output.getvalue())
    resp.headers['Content-Disposition'] = 'attachment; filename=users.csv'
    resp.headers['Content-Type'] = 'text/csv'
    return resp

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
