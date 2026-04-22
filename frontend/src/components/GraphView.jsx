import { useEffect, useState } from 'react'
import ForceGraph2D from 'react-force-graph-2d'
import { getEdges } from '../services/api'

export default function GraphView({ nodes, refreshKey }) {
    const [graphData, setGraphData] = useState({ nodes: [], links: [] })

    useEffect(() => {
        const loadGraph = async () => {
            if (nodes.length === 0) return

            const edgePromises = nodes.map(n => getEdges(n.NodeID))
            const edgeArrays = await Promise.all(edgePromises)
            const allEdges = edgeArrays.flat()

            const uniqueEdges = allEdges.filter(
                (edge, index, self) =>
                    index === self.findIndex(e => e.EdgeID === edge.EdgeID)
            )

            setGraphData({
                nodes: nodes.map(n => ({ id: n.NodeID, label: n.NodeTitle })),
                links: uniqueEdges.map(e => ({ source: e.OutNode, target: e.InNode }))
            })
        }

        loadGraph()
    }, [nodes, refreshKey])

    return (
        <ForceGraph2D
            graphData={graphData}
            nodeLabel="label"
            nodeAutoColorBy="label"
            width={800}
            height={500}
        />
    )
}