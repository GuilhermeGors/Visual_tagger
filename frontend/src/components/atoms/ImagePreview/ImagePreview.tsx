import React from 'react';

interface ImagePreviewProps {
  src: string | null;
  alt: string;
  className?: string;
}

const ImagePreview: React.FC<ImagePreviewProps> = ({ src, alt, className = '' }) => {
  if (!src) {
    return (
      <div className={`flex items-center justify-center bg-gray-200 text-gray-500 rounded-xl border-2 border-dashed border-gray-300 h-48 w-full ${className}`}>
        <span className="text-center text-lg font-medium">Nenhuma imagem selecionada</span>
      </div>
    );
  }

  return (
    <div className={`relative rounded-xl overflow-hidden shadow-lg border border-gray-200 ${className}`}>
      <img
        src={src}
        alt={alt}
        className="w-full h-full object-contain bg-gray-50" // Adicionado bg-gray-50 para fundo do preview
        onError={(e) => {
          e.currentTarget.onerror = null;
          e.currentTarget.src = "https://placehold.co/400x300/E0E0E0/A0A0A0?text=Erro+ao+carregar+imagem";
        }}
      />
    </div>
  );
};

export default ImagePreview;
