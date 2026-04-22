from flask import Blueprint, request, jsonify
from database.db import get_connection

nodes_bp = Blueprint('nodes', __name__)

@nodes_bp.route('/nodes', methods=['POST'])
def create_node():
    data = request.json
    title = data.get('title')
    node_type = data.get('type')
    tags = data.get('tags')
    content = data.get('content')

    if not title or not node_type:
        return jsonify({'error': 'title and type are required'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Node (NodeTitle, NodeType, Tags, content) VALUES (?, ?, ?, ?)",
        (title, node_type, tags, content)
    )
    conn.commit()
    node_id = cursor.lastrowid
    conn.close()

    return jsonify({'message': 'Node created', 'id': node_id}), 201


@nodes_bp.route('/nodes', methods=['GET'])
def get_all_nodes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Node")
    rows = cursor.fetchall()
    conn.close()

    nodes = [dict(row) for row in rows]
    return jsonify(nodes), 200


@nodes_bp.route('/nodes/<int:node_id>', methods=['GET'])
def get_node(node_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Node WHERE NodeID = ?", (node_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({'error': 'Node not found'}), 404

    return jsonify(dict(row)), 200


@nodes_bp.route('/nodes/<int:node_id>', methods=['DELETE'])
def delete_node(node_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Node WHERE NodeID = ?", (node_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Node deleted'}), 200