import { useState } from 'react'
import { getSimilarNodes } from '../services/api'

export default function NodeCard({ node }) {
    const [similar, setSimilar] = useState([])
    const [showSimilar, setShowSimilar] = useState(false)

    const handleFindSimilar = async () => {
        const results = await getSimilarNodes(node.NodeID)
        setSimilar(results)
        setShowSimilar(true)
    }

    return (
        <div style={{ border: '1px solid #ccc', padding: '1rem', borderRadius: '8px', minWidth: '200px' }}>
            <h3>{node.NodeTitle}</h3>
            <p>Type: {node.NodeType}</p>
            <p>Tags: {node.Tags}</p>
            <button onClick={handleFindSimilar} style={{ marginTop: '0.5rem' }}>
                Find Similar
            </button>
            {showSimilar && similar.length > 0 && (
                <div style={{ marginTop: '0.5rem' }}>
                    <strong>Similar nodes:</strong>
                    {similar.map(s => (
                        <p key={s.NodeID} style={{ fontSize: '0.85rem', color: '#555' }}>
                            {s.NodeTitle} — {(s.similarity * 100).toFixed(0)}% match
                        </p>
                    ))}
                </div>
            )}
        </div>
    )
}