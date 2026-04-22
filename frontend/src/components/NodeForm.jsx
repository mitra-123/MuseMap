import { useState } from 'react'

export default function NodeForm({ onSubmit }) {
    const [title, setTitle] = useState('')
    const [type, setType] = useState('text')
    const [tags, setTags] = useState('')
    const [content, setContent] = useState('')

    const handleSubmit = () => {
        if (!title) return
        onSubmit({ title, type, tags, content })
        setTitle('')
        setTags('')
        setContent('')
    }

    return (
        <div>
            <input
                placeholder="Title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
            />
            <select value={type} onChange={(e) => setType(e.target.value)}>
                <option value="text">Text</option>
                <option value="image">Image</option>
                <option value="link">Link</option>
            </select>
            <input
                placeholder="Tags (comma separated)"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
            />
            <input
                placeholder="Content or URL"
                value={content}
                onChange={(e) => setContent(e.target.value)}
            />
            <button onClick={handleSubmit}>Add Node</button>
        </div>
    )
}