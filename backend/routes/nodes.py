from flask import Blueprint, request, jsonify
from database.db import get_connection
from services.embedding_service import generate_embedding, embedding_to_string, string_to_embedding
from services.similarity_service import cosine_similarity

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

    # generate embedding from title + tags
    text_for_embedding = f"{title} {tags or ''}"
    embedding = generate_embedding(text_for_embedding)
    embedding_str = embedding_to_string(embedding)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Node (NodeTitle, NodeType, Tags, content, embedding) VALUES (?, ?, ?, ?, ?)",
        (title, node_type, tags, content, embedding_str)
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


@nodes_bp.route('/nodes/<int:node_id>/similar', methods=['GET'])
def get_similar_nodes(node_id):
    conn = get_connection()
    cursor = conn.cursor()

    # get the target node
    cursor.execute("SELECT * FROM Node WHERE NodeID = ?", (node_id,))
    target = cursor.fetchone()

    if target is None:
        conn.close()
        return jsonify({'error': 'Node not found'}), 404

    if not target['embedding']:
        conn.close()
        return jsonify({'error': 'Node has no embedding'}), 400

    target_embedding = string_to_embedding(target['embedding'])

    # get all other nodes
    cursor.execute("SELECT * FROM Node WHERE NodeID != ?", (node_id,))
    all_nodes = cursor.fetchall()
    conn.close()

    # calculate similarity scores
    scored = []
    for node in all_nodes:
        if node['embedding']:
            other_embedding = string_to_embedding(node['embedding'])
            score = cosine_similarity(target_embedding, other_embedding)
            scored.append({
                'NodeID': node['NodeID'],
                'NodeTitle': node['NodeTitle'],
                'Tags': node['Tags'],
                'similarity': round(score, 3)
            })

    # sort by similarity and return top 3
    scored.sort(key=lambda x: x['similarity'], reverse=True)
    return jsonify(scored[:3]), 200