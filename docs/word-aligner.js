import React, { useState } from 'react';

const WordAligner = () => {
  const [input, setInput] = useState('');
  const [alignmentGrid, setAlignmentGrid] = useState(null);
  
  const processAlignment = (text) => {
    try {
      const [source, target, alignment] = text.includes('|||') ? 
        text.split(" ||| ") : 
        text.split("\t");
      const sourceWords = source.split(" ");
      const targetWords = target.split(" ");
      const alignmentPoints = alignment.split(" ").map(point => {
        const [x, y] = point.split("-").map(Number);
        return [x, y];
      });
      
      const grid = sourceWords.map((_, i) => 
        targetWords.map((_, j) => 
          alignmentPoints.some(([x, y]) => x === i && y === j) ? "X" : ""
        )
      );
      
      return { sourceWords, targetWords, grid };
    } catch (e) {
      return null;
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setAlignmentGrid(processAlignment(input));
  };

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="mb-6">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="w-full p-2 border rounded mb-2"
          placeholder="Enter source ||| target ||| alignments"
          rows={3}
        />
        <button 
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Visualize Alignment
        </button>
      </form>

      {alignmentGrid && (
        <div className="overflow-x-auto">
          <table className="border-collapse">
            <thead>
              <tr>
                <th className="border p-2"></th>
                {alignmentGrid.targetWords.map((word, i) => (
                  <th key={i} className="border p-2 font-normal">{word}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {alignmentGrid.sourceWords.map((sourceWord, i) => (
                <tr key={i}>
                  <th className="border p-2 font-normal">{sourceWord}</th>
                  {alignmentGrid.grid[i].map((cell, j) => (
                    <td key={j} className="border p-2 text-center">
                      {cell === "X" ? "×" : ""}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default WordAligner;
