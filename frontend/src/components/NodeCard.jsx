export default function NodeCard({ node }) {
    return (
        <div style={{ border: '1px solid #ccc', padding: '1rem', borderRadius: '8px' }}>
            <h3>{node.NodeTitle}</h3>
            <p>Type: {node.NodeType}</p>
            <p>Tags: {node.Tags}</p>
        </div>
    )
}