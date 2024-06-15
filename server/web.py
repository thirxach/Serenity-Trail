from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

# Initialize the Flask app
app = Flask(__name__)
# Configure the database - SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Create a model for the database
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    message = db.Column(db.String(200))

    def __repr__(self):
        return f'<Message {self.name}>'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/trail')
def trail():
    return render_template('Trail.html')


@app.route('/about')
def about():
    return render_template('About.html')


@app.route('/contact')
def contact():
    return render_template('Contact.html')

# Create a POST endpoint to store the feedback
@app.route('/feedback', methods=['POST'])
def post_message():
    data = request.get_json()
    new_message = Message(name=data['name'], email=data['email'], phone=data['phone'], message=data['message'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message stored'}), 201

# Create a GET endpoint to retrieve the feedback
@app.route('/feedback', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    output = []
    for message in messages:
        message_data = {'name': message.name, 'email': message.email, 'phone': message.phone,
                        'message': message.message}
        output.append(message_data)
    return jsonify(output)

# admin routes need to be protected
# In ths case, we will use nginx to protect the admin routes
@app.route('/admin/view_feedback')
def view_messages():
    messages = Message.query.all()
    return render_template('feedback_dashboard.html', messages=messages)

# Delete a feedback message by id
@app.route('/admin/delete_feedback', methods=['POST'])
def delete_messages():
    data = request.get_json()
    message = Message.query.filter_by(id=data['id']).first()
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted'})

# start the server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5555)
