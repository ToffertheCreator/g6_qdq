from flask import Flask, request, render_template, session, jsonify
from algorithms import deque, queue, binarytree, bst, graph_bfs, sorting
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

@app.route('/binary_tree', methods=['GET', 'POST'])
def binary_tree():
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

@app.route('/bst', methods=['GET', 'POST'])
def bst_route():
    message = ""
    traversal_result = ""
    search_result = ""
    tree_data = None

    if request.method == 'GET':
        session['bst'] = None
        session['bst_type'] = None

    if 'bst' not in session:
        session['bst'] = None
    if 'bst_type' not in session:
        session['bst_type'] = None

    if request.method == 'POST':
        action = request.form.get('action')
        
        # Handle clear action
        if action == 'clear':
            session['bst'] = None
            session['bst_type'] = None
            session.modified = True
            message = "BST cleared successfully"
            return render_template('bst.html', tree=None, message=message)
        
        operation = request.form.get('operation')
        value = request.form.get('value', '').strip()

        # Handle insertions
        if operation == 'insert' and value:
            # Try to determine the type
            try:
                # Try int first
                if '.' not in value:
                    converted_value = int(value)
                    value_type = 'int'
                else:
                    converted_value = float(value)
                    value_type = 'float'
            except ValueError:
                # It's a string/letter
                converted_value = value
                value_type = 'str'
            
            # Check type consistency
            if session['bst_type'] is None:
                # First node, set the type
                session['bst_type'] = value_type
            elif session['bst_type'] != value_type:
                message = f"✗ Type mismatch: BST contains {session['bst_type']}s, but you entered a {value_type}"
                tree_data = session['bst']
                return render_template('bst.html', tree=tree_data, message=message)
            
            # If tree is empty, create root
            if session['bst'] is None:
                bt = bst.BST(converted_value)
                session['bst'] = node_to_dict(bt.root)
                session.modified = True
                message = f"Inserted {converted_value}"
            else:
                bt = bst.BST()
                bt.root = node_from_dict(session['bst'])
                bt.insert(converted_value)
                session['bst'] = node_to_dict(bt.root)
                session.modified = True
                message = f"Inserted {converted_value}"
        
        # Handle search
        elif operation == 'search' and value:
            try:
                if '.' not in value:
                    converted_value = int(value)
                    value_type = 'int'
                else:
                    converted_value = float(value)
                    value_type = 'float'
            except ValueError:
                converted_value = value
                value_type = 'str'
            
            if session['bst']:
                bt = bst.BST()
                bt.root = node_from_dict(session['bst'])
                
                if bt.search(converted_value):
                    search_result = f"✓ Found: {converted_value} exists in the BST"
                else:
                    search_result = f"✗ Not Found: {converted_value} does not exist in the BST"
            else:
                message = "BST is empty"
        
        # Handle delete
        elif operation == 'delete' and value:
            try:
                if '.' not in value:
                    converted_value = int(value)
                    value_type = 'int'
                else:
                    converted_value = float(value)
                    value_type = 'float'
            except ValueError:
                converted_value = value
                value_type = 'str'
            
            if session['bst']:
                bt = bst.BST()
                bt.root = node_from_dict(session['bst'])
                
                if bt.search(converted_value):
                    bt.delete(converted_value)
                    message = f"Deleted {converted_value} from BST"
                    session['bst'] = node_to_dict(bt.root)
                    session.modified = True
                else:
                    message = f"Could not delete {converted_value} - not found in BST"
            else:
                message = "BST is empty"
        
        # Handle traversals
        elif operation in ['preorder_traversal', 'inorder_traversal', 'postorder_traversal']:
            if session['bst']:
                bt = bst.BST()
                bt.root = node_from_dict(session['bst'])
                
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
                message = "BST is empty"
        
        # Handle get min
        elif operation == 'get_min':
            if session['bst']:
                bt = bst.BST()
                bt.root = node_from_dict(session['bst'])
                min_value = bt.get_min()
                message = f"Minimum value: {min_value}"
            else:
                message = "BST is empty"
        
        # Handle get max
        elif operation == 'get_max':
            if session['bst']:
                bt = bst.BST()
                bt.root = node_from_dict(session['bst'])
                max_value = bt.get_max()
                message = f"Maximum value: {max_value}"
            else:
                message = "BST is empty"
        
        # Handle get height
        elif operation == 'find_height':
            if session['bst']:
                bt = bst.BST()
                bt.root = node_from_dict(session['bst'])
                height = bt.find_height()
                message = f"Height of BST: {height}"
            else:
                message = "BST is empty"

    tree_data = session['bst']
    return render_template('bst.html', tree=tree_data, message=message, traversal_result=traversal_result, search_result=search_result)

@app.route('/graph', methods=['GET', 'POST'])
def graph_route():
    return render_template('graph.html')

@app.route('/api/find-path', methods=['POST'])
def api_find_path():
    """API endpoint to find shortest path using BFS"""
    try:
        data = request.get_json()
        start = data.get('start')
        goal = data.get('goal')
        
        if not start or not goal:
            return jsonify({'error': 'Start and goal are required'}), 400
        
        path = graph_bfs.bfs_shortest_path(start, goal)
        
        if path:
            return jsonify({'path': path})
        else:
            return jsonify({'path': []})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sort', methods=['GET', 'POST'])
def sort_route():
    return render_template('sorting.html')

@app.route('/api/sort', methods=['POST'])
def api_sort():
    """API endpoint to perform sorting and return steps"""
    try:
        data = request.get_json()
        arr = data.get('arr', [])
        algorithm = data.get('algorithm', 'bubble')
        
        if not arr:
            return jsonify({'error': 'Array is required'}), 400
        
        # Call the appropriate sorting function
        if algorithm == 'bubble':
            steps = sorting.bubble_sort(arr)
        elif algorithm == 'selection':
            steps = sorting.selection_sort(arr)
        elif algorithm == 'insertion':
            steps = sorting.insertion_sort(arr)
        elif algorithm == 'merge':
            steps = sorting.merge_sort(arr)
        elif algorithm == 'quick':
            steps = sorting.quick_sort(arr)
        else:
            return jsonify({'error': 'Invalid algorithm'}), 400
        
        return jsonify({'steps': steps})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/contact')
def contact():
    return render_template('contacts.html')

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
