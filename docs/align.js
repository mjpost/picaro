function processAlignment(text) {
    try {
        // Check for tab first, otherwise use |||
        const parts = text.includes('\t') ? text.split('\t') : text.split('|||');
        if (parts.length !== 3) {
            throw new Error('Invalid input format');
        }
        
        const [source, target, alignment] = parts.map(p => p.trim());
        const sourceWords = source.split(' ');
        const targetWords = target.split(' ');
        const alignments = new Set(
            alignment.split(' ').map(a => a.trim()).filter(a => a)
        );
        
        let table = '<table>';
        
        // Header row with target words
        table += '<tr><td class="cell"></td>';
        for (let targetWord of targetWords) {
            table += `<td class="cell">${targetWord}</td>`;
        }
        table += '</tr>';
        
        // Create alignment grid
        for (let i = 0; i < sourceWords.length; i++) {
            table += `<tr><td class="cell">${sourceWords[i]}</td>`;
            for (let j = 0; j < targetWords.length; j++) {
                const isAligned = alignments.has(`${i}-${j}`);
                table += `<td class="cell ${isAligned ? 'aligned' : ''}">${isAligned ? 'X' : ''}</td>`;
            }
            table += '</tr>';
        }
        
        table += '</table>';
        return table;
    } catch (error) {
        return '<p>Invalid input format</p>';
    }
}

document.getElementById('input').addEventListener('input', function(e) {
    const text = e.target.value;
    if (text) {
        document.getElementById('output').innerHTML = processAlignment(text);
    } else {
        document.getElementById('output').innerHTML = '';
    }
});
