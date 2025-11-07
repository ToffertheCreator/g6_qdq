from flask import Flask, request, render_template, session
from algorithms import deque, queue
import os

app = Flask(__name__)
app.secret_key = 'SDIYBT'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/q', methods=['GET', 'POST'])
def q():
    message = ""
    removed_message = ""

    # Initialize queue session
    if request.method == 'GET':
        session['queue_data'] = []
        session['message'] = ""
        session['removed_message'] = ""

    if 'queue_data' not in session:
        session['queue_data'] = []

    # Rebuild queue from session data
    my_queue = queue.Queue()
    for item in session['queue_data']:
        my_queue.enqueue(item)

    if request.method == 'POST':
        data = request.form.get('inputdata', '').strip()
        operation = request.form.get('operation')

        if operation == 'enqueue' and data:
            my_queue.enqueue(data)
        elif operation == 'dequeue':
            removed = my_queue.dequeue()
            removed_message = f"Dequeued: {removed}" if removed else "Queue is empty."

        # Save updated queue state
        session['queue_data'] = my_queue.display()
        session.modified = True
    else:
        message = session.get('message', '')
        removed_message = session.get('removed_message', '')

    queue_items = my_queue.display()
    return render_template('queue.html', queue_items=queue_items, message=message, removed_message=removed_message)

@app.route('/dq', methods=['GET', 'POST'])
def dq():
    message = ""
    removed_message = ""

    # Initialize deque in session
    if request.method == 'GET':
        session['deque_data'] = []
        session['message'] = ""
        session['removed_message'] = ""

    if 'deque_data' not in session:
        session['deque_data'] = []

    # Rebuild deque from session data
    my_deque = deque.Deque()
    for item in session['deque_data']:
        my_deque.add_rear(item)

    if request.method == 'POST':
        data = request.form.get('inputdata', '').strip()
        operation = request.form.get('operation')

        if operation == 'add_front' and data:
            my_deque.add_front(data)
        elif operation == 'add_rear' and data:
            my_deque.add_rear(data)
        elif operation == 'remove_front':
            removed = my_deque.remove_front()
            removed_message = f"Removed from front: {removed}" if removed else "Deque is empty."
        elif operation == 'remove_rear':
            removed = my_deque.remove_rear()
            removed_message = f"Removed from rear: {removed}" if removed else "Deque is empty."

        # Save updated deque back to session
        session['deque_data'] = my_deque.display()
        session.modified = True
    else:
        message = session.get('message', '')
        removed_message = session.get('removed_message', '')

    deque_items = my_deque.display()
    return render_template('deque.html', deque_items=deque_items, message=message, removed_message=removed_message)

@app.route('/contact')
def contact():
    return render_template('contacts.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)