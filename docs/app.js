import { createElement } from 'react'
import { createRoot } from 'react-dom/client'
import { WordAligner } from './word-aligner.js'

const root = createRoot(document.getElementById('root'))
root.render(createElement(WordAligner))
