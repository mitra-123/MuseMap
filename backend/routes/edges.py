from flask import Blueprint, request, jsonify
from database.db import get_connection

edges_bp = Blueprint('edges', __name__)

@edges_bp.route('/edges', methods=['POST'])
def create_edge():
    data = request.json
    out_node = data.get('source_id')
    in_node = data.get('target_id')
    relationship = data.get('relation')

    if not out_node or not in_node or not relationship:
        return jsonify({'error': 'source_id, target_id and relation are required'}), 400

    conn = get_connection()
    cursor = conn.cursor()

    # check both nodes exist before creating edge
    cursor.execute("SELECT NodeID FROM Node WHERE NodeID = ?", (out_node,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({'error': f'Source node {out_node} not found'}), 404

    cursor.execute("SELECT NodeID FROM Node WHERE NodeID = ?", (in_node,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({'error': f'Target node {in_node} not found'}), 404

    cursor.execute(
        "INSERT INTO Edge (OutNode, InNode, Relationship) VALUES (?, ?, ?)",
        (out_node, in_node, relationship)
    )
    conn.commit()
    edge_id = cursor.lastrowid
    conn.close()

    return jsonify({'message': 'Edge created', 'id': edge_id}), 201


@edges_bp.route('/edges/<int:node_id>', methods=['GET'])
def get_edges(node_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Edge WHERE OutNode = ? OR InNode = ?",
        (node_id, node_id)
    )
    rows = cursor.fetchall()
    conn.close()

    edges = [dict(row) for row in rows]
    return jsonify(edges), 200