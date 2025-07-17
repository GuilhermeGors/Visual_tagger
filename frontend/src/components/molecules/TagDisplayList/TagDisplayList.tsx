import React from 'react';
import { Tag } from '../../../types/frontend.d'; // Importa a interface de tipo

interface TagDisplayListProps {
  tags: Tag[]; // Lista de tags a serem exibidas
  isLoading?: boolean; // Estado de carregamento
  error?: string; // Mensagem de erro
}

const TagDisplayList: React.FC<TagDisplayListProps> = ({ tags, isLoading = false, error }) => {

  // Helper function to determine color class based on confidence
  const getConfidenceColorClass = (confidence: number): string => {
    if (confidence >= 0.75) {
      return 'text-green-600'; // High confidence
    } else if (confidence >= 0.50) {
      return 'text-yellow-600'; // Medium confidence
    } else {
      return 'text-red-600'; // Low confidence
    }
  };

  if (isLoading) {
    return (
      <div className="p-4 bg-white rounded-lg shadow-md text-center text-gray-600">
        <svg className="animate-spin h-5 w-5 text-primary mx-auto mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Analisando imagem...
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg shadow-md">
        <p className="font-semibold">Analysis error:</p>
        <p className="text-sm">{error}</p>
      </div>
    );
  }

  if (!tags || tags.length === 0) {
    return (
      <div className="p-4 bg-white rounded-lg shadow-md text-center text-gray-500">
        No tag detected with sufficient confidence.
      </div>
    );
  }

  return (
    <div className="p-4 bg-white rounded-lg shadow-md">
      <h3 className="text-lg font-semibold text-gray-800 mb-3">Tags Detectadas:</h3>
      <ul className="space-y-2">
        {tags.map((tag, index) => (
          <li key={index} className="flex justify-between items-center bg-gray-50 p-3 rounded-md border border-gray-200">
            <span className="text-gray-700 font-medium">{tag.name}</span>
            {/* Applies color class based on confidence */}
            <span className={`text-sm font-semibold ${getConfidenceColorClass(tag.confidence)}`}>
              {(tag.confidence * 100).toFixed(2)}%
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TagDisplayList;
