from flask import Flask, request, render_template, session
from algorithms import deque, queue, binarytree
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

    if request.method == 'GET':
        session['queue_data'] = []
        session['message'] = ""
        session['removed_message'] = ""

    # Rebuild queue from session data
    my_queue = queue.Queue()
    for item in session['queue_data']:
        my_queue.enqueue(item)

    if request.method == 'POST':
        operation = request.form.get('operation')
        data = request.form.get('inputdata')

        if operation == 'enqueue' and data:
            my_queue.enqueue(data)
            message = f"Added {data} to queue"
            session['queue_data'] = my_queue.display()
        elif operation == 'dequeue':
            if my_queue.display():
                removed_item = my_queue.dequeue()
                removed_message = f"Removed {removed_item} from queue"
                session['queue_data'] = my_queue.display()
            else:
                message = "Queue is empty"

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

@app.route('/tree', methods=['GET', 'POST'])
def tree():
    message = ""
    traversal_result = ""
    search_result = ""
    tree_data = None

    if request.method == 'GET':
        session['tree'] = None

    if 'tree' not in session:
        session['tree'] = None

    if request.method == 'POST':
        operation = request.form.get('operation')
        value = request.form.get('value', '').strip()
        starting_node_value = request.form.get('starting_node', '').strip()
        action = request.form.get('action')

        # Handle clear action
        if action == 'clear':
            session['tree'] = None
            session.modified = True
            message = "Tree cleared successfully"
            return render_template('binarytree.html', tree=None, message=message)
        
        operation = request.form.get('operation')
        value = request.form.get('value', '').strip()
        starting_node_value = request.form.get('starting_node', '').strip()

        # Handle insertions
        if (operation == 'insert_left' or operation == 'insert_right') and value:
            bt = binarytree.BinaryTree()
            
            # If tree is empty, create root
            if session['tree'] is None:
                bt.root = binarytree.Node(value)
                session['tree'] = node_to_dict(bt.root)
                session.modified = True
                message = f"Inserted {value}"
            else:
                # Tree already exists, insert into it
                bt.root = node_from_dict(session['tree'])
                
                # Find starting node
                start_node = bt.root
                if starting_node_value:
                    start_node = bt.find_node_by_value(starting_node_value)
                    if not start_node:
                        message = f"Starting node {starting_node_value} not found"
                        tree_data = session['tree']
                        return render_template('binarytree.html', tree=tree_data, message=message)
                
                # Insert based on operation
                if operation == 'insert_left':
                    bt.insert_left(value, start_node)
                    if starting_node_value:
                        message = f"Inserted {value} to the left of {start_node.value}"
                    else:
                        message = f"Inserted {value}"
                else:  # insert_right
                    bt.insert_right(value, start_node)
                    if starting_node_value:
                        message = f"Inserted {value} to the right of {start_node.value}"
                    else:
                        message = f"Inserted {value}"
                
                session['tree'] = node_to_dict(bt.root)
                session.modified = True
        
        # Handle search
        elif operation == 'search' and value:
            if session['tree']:
                bt = binarytree.BinaryTree()
                bt.root = node_from_dict(session['tree'])
                
                if bt.search(value):
                    search_result = f"✓ Found: {value} exists in the tree"
                else:
                    search_result = f"✗ Not Found: {value} does not exist in the tree"
            else:
                message = "Tree is empty"
        
        # Handle delete
        elif operation == 'delete' and value:
            if session['tree']:
                bt = binarytree.BinaryTree()
                bt.root = node_from_dict(session['tree'])
                
                if bt.delete(value):
                    message = f"Deleted {value} from tree"
                    session['tree'] = node_to_dict(bt.root)
                    session.modified = True
                else:
                    message = f"Could not delete {value} - not found in tree"
            else:
                message = "Tree is empty"
        
        # Handle traversals
        elif operation in ['preorder_traversal', 'inorder_traversal', 'postorder_traversal']:
            if session['tree']:
                bt = binarytree.BinaryTree()
                bt.root = node_from_dict(session['tree'])
                
                if operation == 'preorder_traversal':
                    result = bt.preorder_traversal(bt.root).strip()
                    traversal_result = f"Preorder: {result}"
                elif operation == 'inorder_traversal':
                    result = bt.inorder_traversal(bt.root).strip()
                    traversal_result = f"Inorder: {result}"
                elif operation == 'postorder_traversal':
                    result = bt.postorder_traversal(bt.root).strip()
                    traversal_result = f"Postorder: {result}"
            else:
                message = "Tree is empty"

    tree_data = session['tree']
    return render_template('binarytree.html', tree=tree_data, message=message, traversal_result=traversal_result, search_result=search_result)

def node_to_dict(node):
    """Convert Node object to dictionary for JSON serialization"""
    if node is None:
        return None
    return {
        'value': node.value,
        'left': node_to_dict(node.left),
        'right': node_to_dict(node.right)
    }

def node_from_dict(data):
    """Convert dictionary back to Node object"""
    if data is None:
        return None
    return binarytree.Node(
        data['value'],
        node_from_dict(data['left']),
        node_from_dict(data['right'])
    )

@app.route('/contact')
def contact():
    return render_template('contacts.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)