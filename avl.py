import json
from typing import List

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key        = None,
                  value      = None,
                  leftchild  = None,
                  rightchild = None):
        self.key        = key
        self.value      = value
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "k": node.key,
            "v": node.value,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr)

#------------------------------------------------------------------------------------
# Helper functions

# A left rotation essentially makes the right subtree of the current node the root,
# and the new root's left tree will be the current node. Vice versa for right rotation.
# Assume the following for the new variables:
# tree_a: our current node
# tree_b: the right subtree
# node_x: left subtree of tree_a
# node_y: left subtree of tree_b
# node_z: right subtree of tree_b
def leftRotate(tree_a: Node):
    tree_b = tree_a.rightchild
    node_y = tree_b.leftchild

    tree_b.leftchild = tree_a
    tree_a.rightchild = node_y
    return tree_b

def rightRotate(tree_a: Node):
    tree_b = tree_a.leftchild
    node_y = tree_b.rightchild

    tree_b.rightchild = tree_a
    tree_a.leftchild = node_y
    return tree_b

def inorderTrav(root: Node) -> List:
    temp = []
    if root != None:
        temp.extend(inorderTrav(root.leftchild))
        temp.append([root.key, root.value])
        temp.extend(inorderTrav(root.rightchild))
    return temp

# Height of (sub)tree rooted at root.
def height(root: Node) -> int:
    if root == None:
        return -1
    else:
        return max(1 + height(root.leftchild), 1 + height(root.rightchild))

# Insert.
def insert(root: Node, key: int, value: str) -> Node:
    if root == None:
        root = Node(key, value, None, None)
    else:
        if key < root.key:
            root.leftchild = insert(root.leftchild, key, value)
        else:
            root.rightchild = insert(root.rightchild, key, value)
    
    balance = height(root.leftchild) - height(root.rightchild)
    if balance > 1:
        if key < root.leftchild.key:
            return rightRotate(root)
        else:
            root.leftchild = leftRotate(root.leftchild)
            return rightRotate(root)
    elif balance < -1:
        if key > root.rightchild.key:
            return leftRotate(root)
        else:
            root.rightchild = rightRotate(root.rightchild)
            return leftRotate(root)
    else:
        return root


# Bulk Delete.
def delete(root: Node, keys: List[int]) -> Node:
    newTree = None

    newNodes = inorderTrav(root)
    for item in newNodes:
        if keys.count(item[0]) == 0:
            newTree = insert(newTree, item[0], item[1])
    return newTree
    
def searchHeight(root: Node, search_key: int) -> int:
    if search_key < root.key:
        return 1 + searchHeight(root.leftchild, search_key)
    elif search_key > root.key:
        return 1 + searchHeight(root.rightchild, search_key)
    else:
        return 1

def searchValue(root: Node, search_key: int) -> str:
    if search_key < root.key:
        return searchValue(root.leftchild, search_key)
    elif search_key > root.key:
        return searchValue(root.rightchild, search_key)
    else:
        return root.value

# Search.
def search(root: Node, search_key: int) -> str:    
    return json.dumps([searchHeight(root, search_key), searchValue(root, search_key)])
#     return [searchHeight(root, search_key), ("{val}").format(val=str(searchValue(root, search_key)))]
# Range Query.
def rangequery(root: Node, x0: int, x1: int) -> List[str]:
    newlist = []

    if root != None:
        if root.key > x1:
            newlist.extend(rangequery(root.leftchild, x0, x1))
        elif root.key < x0:
            newlist.extend(rangequery(root.rightchild, x0, x1))
        else:
            newlist.append(root.value)
            newlist.extend(rangequery(root.leftchild, x0, x1))
            newlist.extend(rangequery(root.rightchild, x0, x1))
    return newlist
