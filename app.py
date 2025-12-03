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

def node_to_dict(node):
    """Convert Node object to dictionary for JSON/session storage"""
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

@app.route('/tree', methods=['GET', 'POST'])
def tree():
    message = ""
    traversal_result = ""
    search_result = ""
    max_result = ""
    height_result = ""

    # Initialize session store for tree on GET
    if request.method == 'GET' and 'tree' not in session:
        session['tree'] = None

    # Helper to restore BinaryTree object from session
    def restore_binarytree_from_session():
        root_dict = session.get('tree')
        if not root_dict:
            return None
        root_node = node_from_dict(root_dict)
        bt = binarytree.BinaryTree()  # Create empty tree
        bt.root = root_node  # Directly assign the root node
        return bt

    # Helper to save BinaryTree root to session
    def save_binarytree_to_session(bt):
        if bt is None or bt.root is None:
            session['tree'] = None
        else:
            session['tree'] = node_to_dict(bt.root)
        session.modified = True

    if request.method == 'POST':
        action = request.form.get('action', None)
        operation = request.form.get('operation', '').strip()
        value_raw = request.form.get('value', '').strip()

        # CLEAR action (top-priority)
        if action == 'clear':
            session['tree'] = None
            session.modified = True
            message = "Tree cleared successfully"
            return render_template('binarytree.html', tree=None, message=message)

        # Accept any data type (string, number, etc.) for general binary tree
        value = value_raw if value_raw != '' else None

        # Restore current tree from session
        bt = restore_binarytree_from_session()

        # If inserting into an empty tree, create new BinaryTree with root
        if operation == 'insert_left':
            if value is None:
                message = "No value provided for insert."
            else:
                if bt is None:
                    # create new tree with root value
                    bt = binarytree.BinaryTree(value)
                    message = f"Inserted root {value}"
                else:
                    bt.insert_left(value)
                    message = f"Inserted {value} (left)"
                save_binarytree_to_session(bt)
        
        elif operation == 'insert_right':
            if value is None:
                message = "No value provided for insert."
            else:
                if bt is None:
                    # create new tree with root value
                    bt = binarytree.BinaryTree(value)
                    message = f"Inserted root {value}"
                else:
                    bt.insert_right(value)
                    message = f"Inserted {value} (right)"
                save_binarytree_to_session(bt)

        elif operation == 'search':
            if bt is None:
                message = "Tree is empty"
            else:
                # Use find_node_by_value which does BFS search
                found = bt.find_node_by_value(value) is not None
                search_result = f"✓ Found: {value} exists in the tree" if found else f"✗ Not Found: {value} does not exist in the tree"

        elif operation == 'delete':
            message = "Delete operation not available for general binary trees. Use BST instead."

        elif operation == 'get_max':
            if bt is None:
                message = "Tree is empty"
            else:
                max_val = bt.get_max_value(bt.root)
                max_result = max_val if max_val is not None else "Tree is empty"

        elif operation == 'height':
            if bt is None:
                message = "Tree is empty"
            else:
                # find height of root
                height_result = bt.find_height(bt.root)

        # Traversals
        elif operation in ['inorder_traversal', 'preorder_traversal', 'postorder_traversal']:
            if bt is None:
                message = "Tree is empty"
            else:
                if operation == 'inorder_traversal':
                    traversal_result = "Inorder: " + bt.inorder_traversal(bt.root).strip()
                elif operation == 'preorder_traversal':
                    traversal_result = "Preorder: " + bt.preorder_traversal(bt.root).strip()
                elif operation == 'postorder_traversal':
                    traversal_result = "Postorder: " + bt.postorder_traversal(bt.root).strip()

    # finally render with session tree
    tree_data = session.get('tree')
    return render_template(
        'binarytree.html',
        tree=tree_data,
        message=message,
        traversal_result=traversal_result,
        search_result=search_result,
        max_result=max_result,
        height_result=height_result
    )

@app.route('/bst', methods=['GET', 'POST'])
def bst():
    message = ""
    traversal_result = ""
    search_result = ""
    max_result = ""
    min_result = ""
    height_result = ""

    # Initialize session tree
    if request.method == "GET" and "bst_tree" not in session:
        session["bst_tree"] = None

    # Restore BST object
    def restore():
        data = session.get("bst_tree")
        if data is None:
            return None
        root = node_from_dict(data)
        bt = bst.BST()  # Create empty tree from BST module
        bt.root = root  # Directly assign the root node
        return bt

    # Save back to session
    def save(bt):
        session["bst_tree"] = node_to_dict(bt.root) if bt and bt.root else None
        session.modified = True

    if request.method == "POST":
        action = request.form.get("action")
        op = request.form.get("operation")
        raw = request.form.get("value", "").strip()

        # Clear
        if action == "clear":
            session["bst_tree"] = None
            return render_template("bst.html", tree=None, message="Tree cleared.")

        # Parse input value
        value = None
        if raw != "":
            try:
                value = int(raw)
            except:
                return render_template("bst.html", tree=session.get("bst_tree"), message="Value must be a number.")

        bt = restore()

        # Insert
        if op == "insert":
            if bt is None:
                bt = bst.BST(value)
            else:
                bt.insert(value)
            save(bt)
            message = f"Inserted {value}"

        # Search
        elif op == "search":
            if bt:
                found = bt.search(bt.root, value)
                search_result = f"✓ {value} found" if found else f"✗ {value} not found"
            else:
                message = "Tree is empty"

        # Delete
        elif op == "delete":
            if bt:
                bt.root = bt.delete(bt.root, value)
                save(bt)
                message = f"Deleted {value}"
            else:
                message = "Tree is empty"

        # Max value
        elif op == "get_max":
            if bt:
                max_result = bt.get_max(bt.root)
            else:
                message = "Tree is empty"

        # Min value
        elif op == "get_min":
            if bt:
                min_result = bt.get_min(bt.root)
            else:
                message = "Tree is empty"

        # Height
        elif op == "height":
            if bt:
                height_result = bt.find_height(bt.root)
            else:
                message = "Tree is empty"

        # Traversals
        elif op in ["preorder_traversal", "inorder_traversal", "postorder_traversal"]:
            if not bt:
                message = "Tree is empty"
            else:
                if op == "preorder_traversal":
                    traversal_result = "Preorder: " + bt.preorder_traversal(bt.root)
                elif op == "inorder_traversal":
                    traversal_result = "Inorder: " + bt.inorder_traversal(bt.root)
                elif op == "postorder_traversal":
                    traversal_result = "Postorder: " + bt.postorder_traversal(bt.root)

    return render_template(
        "bst.html",
        tree=session.get("bst_tree"),
        message=message,
        search_result=search_result,
        traversal_result=traversal_result,
        max_result=max_result,
        min_result=min_result,
        height_result=height_result
    )

@app.route('/contact')
def contact():
    return render_template('contacts.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
