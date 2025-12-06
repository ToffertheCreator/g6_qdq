from flask import Flask, request, render_template, session
from algorithms import deque, queue, binarytree, bst
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

    if request.method == 'GET':
        session['deque_data'] = []
        session['message'] = ""
        session['removed_message'] = ""

    if 'deque_data' not in session:
        session['deque_data'] = []

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

        session['deque_data'] = my_deque.display()
        session.modified = True
    else:
        message = session.get('message', '')
        removed_message = session.get('removed_message', '')

    deque_items = my_deque.display()
    return render_template('deque.html', deque_items=deque_items, message=message, removed_message=removed_message)

def node_to_dict(node):
    if node is None:
        return None
    return {
        'value': node.value,
        'left': node_to_dict(node.left),
        'right': node_to_dict(node.right)
    }

def node_from_dict(data):
    if data is None:
        return None
    return binarytree.Node(
        data['value'],
        node_from_dict(data['left']),
        node_from_dict(data['right'])
    )

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

        if action == 'clear':
            session['tree'] = None
            session.modified = True
            message = "Tree cleared successfully"
            return render_template('binarytree.html', tree=None, message=message)
        
        if (operation == 'insert_left' or operation == 'insert_right') and value:
            bt = binarytree.BinaryTree()
            
            if session['tree'] is None:
                bt.root = binarytree.Node(value)
                session['tree'] = node_to_dict(bt.root)
                session.modified = True
                message = f"Inserted {value}"
            else:
                bt.root = node_from_dict(session['tree'])
                
                start_node = bt.root
                if starting_node_value:
                    start_node = bt.find_node_by_value(starting_node_value)
                    if not start_node:
                        message = f"Starting node {starting_node_value} not found"
                        tree_data = session['tree']
                        return render_template('binarytree.html', tree=tree_data, message=message)
                
                if operation == 'insert_left':
                    bt.insert_left(value, start_node)
                    message = f"Inserted {value}"
                else:
                    bt.insert_right(value, start_node)
                    message = f"Inserted {value}"
                
                session['tree'] = node_to_dict(bt.root)
                session.modified = True
        
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

@app.route('/bst', methods=['GET', 'POST'])
def bst():
    message = ""
    traversal_result = ""
    search_result = ""
    tree_data = None

    if request.method == 'GET':
        session['bst'] = None

    if 'bst' not in session:
        session['bst'] = None

    if request.method == 'POST':
        operation = request.form.get('operation')
        value = request.form.get('value', '').strip()
        action = request.form.get('action')

        # SINGLE DIGIT VALIDATION
        if value and not (value.isdigit() and len(value) == 1):
            message = "Error: Only single-digit integers (0-9) are allowed."
            tree_data = session['bst']
            return render_template('binarysearchtree.html', tree=tree_data, message=message)

        if action == 'clear':
            session['bst'] = None
            session.modified = True
            message = "Tree cleared successfully"
            return render_template('binarysearchtree.html', tree=None, message=message)

        # Insert
        if operation == 'insert' and value:
            numeric_value = int(value)

            if session['bst'] is None:
                bst_tree = bst.BST(numeric_value)
                session['bst'] = node_to_dict(bst_tree.root)
                session.modified = True
                message = f"Inserted {numeric_value}"
            else:
                bst_tree = bst.BST()
                bst_tree.root = node_from_dict(session['bst'])
                bst_tree.insert(numeric_value)
                session['bst'] = node_to_dict(bst_tree.root)
                session.modified = True
                message = f"Inserted {numeric_value}"

        # Search
        elif operation == 'search' and value:
            numeric_value = int(value)

            if session['bst']:
                bst_tree = bst.BST()
                bst_tree.root = node_from_dict(session['bst'])

                if bst_tree.search(numeric_value):
                    search_result = f"✓ Found: {numeric_value} exists in the tree"
                else:
                    search_result = f"✗ Not Found: {numeric_value} does not exist in the tree"
            else:
                message = "Tree is empty"

        # Delete
        elif operation == 'delete' and value:
            numeric_value = int(value)

            if session['bst']:
                bst_tree = bst.BST()
                bst_tree.root = node_from_dict(session['bst'])

                bst_tree.root = bst_tree.delete(numeric_value, bst_tree.root)
                session['bst'] = node_to_dict(bst_tree.root) if bst_tree.root else None
                session.modified = True
                message = f"Deleted {numeric_value}"
            else:
                message = "Tree is empty"

        # Traversals
        elif operation in ['preorder_traversal', 'inorder_traversal', 'postorder_traversal']:
            if session['bst']:
                bst_tree = bst.BST()
                bst_tree.root = node_from_dict(session['bst'])

                if operation == 'preorder_traversal':
                    result = bst_tree.preorder_traversal(bst_tree.root).strip()
                    traversal_result = f"Preorder: {result}"
                elif operation == 'inorder_traversal':
                    result = bst_tree.inorder_traversal(bst_tree.root).strip()
                    traversal_result = f"Inorder: {result}"
                elif operation == 'postorder_traversal':
                    result = bst_tree.postorder_traversal(bst_tree.root).strip()
                    traversal_result = f"Postorder: {result}"
            else:
                message = "Tree is empty"

    tree_data = session['bst']
    return render_template('binarysearchtree.html', tree=tree_data, message=message, traversal_result=traversal_result, search_result=search_result)

@app.route('/contact')
def contact():
    return render_template('contacts.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
