import { useEffect, useState } from 'react'
import NodeCard from '../components/NodeCard'
import NodeForm from '../components/NodeForm'
import GraphView from '../components/GraphView'
import { getAllNodes, createNode, createEdge } from '../services/api'

export default function Home() {
    const [nodes, setNodes] = useState([])
    const [sourceId, setSourceId] = useState('')
    const [targetId, setTargetId] = useState('')
    const [relation, setRelation] = useState('')
    const [edgeMessage, setEdgeMessage] = useState('')
    const [refreshKey, setRefreshKey] = useState(0)

    useEffect(() => {
        getAllNodes().then(data => setNodes(data))
    }, [])

    const handleAddNode = async (nodeData) => {
        await createNode(nodeData)
        const updated = await getAllNodes()
        setNodes(updated)
    }

    const handleAddEdge = async () => {
        if (!sourceId || !targetId || !relation) {
            setEdgeMessage('Please fill in all fields')
            return
        }
        const result = await createEdge({
            source_id: parseInt(sourceId),
            target_id: parseInt(targetId),
            relation
        })
        if (result.error) {
            setEdgeMessage(result.error)
        } else {
            setEdgeMessage('Connection created!')
            setSourceId('')
            setTargetId('')
            setRelation('')
            setRefreshKey(prev => prev + 1) // 👈 forces graph to reload
        }
    }
    return (
        <div>
            <h1>MuseMap</h1>

            {/* Add Node Form */}
            <NodeForm onSubmit={handleAddNode} />

            {/* Node Cards */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', marginTop: '1rem' }}>
                {nodes.map(node => (
                    <NodeCard key={node.NodeID} node={node} />
                ))}
            </div>

            {/* Connect Nodes Form */}
            <div style={{ marginTop: '2rem' }}>
                <h2>Connect Nodes</h2>
                <p style={{ color: '#888', fontSize: '0.9rem' }}>
                    Node IDs: {nodes.map(n => `${n.NodeID} (${n.NodeTitle})`).join(', ')}
                </p>
                <input
                    placeholder="Source Node ID"
                    value={sourceId}
                    onChange={(e) => setSourceId(e.target.value)}
                />
                <input
                    placeholder="Target Node ID"
                    value={targetId}
                    onChange={(e) => setTargetId(e.target.value)}
                    style={{ marginLeft: '0.5rem' }}
                />
                <input
                    placeholder="Relationship (e.g. inspired by)"
                    value={relation}
                    onChange={(e) => setRelation(e.target.value)}
                    style={{ marginLeft: '0.5rem' }}
                />
                <button onClick={handleAddEdge} style={{ marginLeft: '0.5rem' }}>
                    Connect
                </button>
                {edgeMessage && <p style={{ color: 'green' }}>{edgeMessage}</p>}
            </div>

            {/* Graph Visualization */}
            <div style={{ marginTop: '2rem' }}>
                <h2>Graph View</h2>
                <GraphView nodes={nodes} refreshKey={refreshKey} />
            </div>
        </div>
    )
}