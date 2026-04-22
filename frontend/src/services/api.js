const BASE_URL = 'http://localhost:5000'

export async function getAllNodes() {
    const res = await fetch(`${BASE_URL}/nodes`)
    return res.json()
}

export async function createNode(data) {
    const res = await fetch(`${BASE_URL}/nodes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    return res.json()
}

export async function createEdge(data) {
    const res = await fetch(`${BASE_URL}/edges`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    return res.json()
}

export async function getEdges(nodeId) {
    const res = await fetch(`${BASE_URL}/edges/${nodeId}`)
    return res.json()
}