import React from 'react';
import ImageUploadArea from '../../molecules/ImageUploadArea/ImageUploadArea';
import TagDisplayList from '../../molecules/TagDisplayList/TagDisplayList';
import Button from '../../atoms/Button/Button';
import ImagePreview from '../../atoms/ImagePreview/ImagePreview'; 
import useImageAnalysis from '../../../hooks/useImageAnalysis';
import { ImageAnalysisResult } from '../../../types/frontend.d'; 

const VisualTaggerModule: React.FC = () => {
  const {
    imageAnalysisResults, 
    isLoadingOverall,     
    handleImagesSelect,   
    handleAnalyzeAllImages, 
    resetAllAnalysis,     
  } = useImageAnalysis();

  const hasSelectedImages = imageAnalysisResults.length > 0;
  const hasAnalysisInProgressOrDone = imageAnalysisResults.some(item => item.response || item.isLoading || item.error);

  return (
    <div className="bg-white p-8 rounded-2xl shadow-xl max-w-4xl w-full mx-auto space-y-6 border border-gray-200 transform transition-all duration-300 hover:shadow-2xl">
      <h2 className="text-3xl font-extrabold text-gray-800 text-center mb-6 tracking-tight">
       Visual Tagging
      </h2>

      {/* Image Upload Area */}
      <ImageUploadArea onImagesSelect={handleImagesSelect} isLoading={isLoadingOverall} />

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row justify-center space-y-3 sm:space-y-0 sm:space-x-4">
        {hasSelectedImages && !isLoadingOverall && !hasAnalysisInProgressOrDone && (
            <Button onClick={handleAnalyzeAllImages} isLoading={isLoadingOverall} size="lg" className="w-full sm:w-auto">
            Analyze All Images
            </Button>
        )}
        {(hasSelectedImages || hasAnalysisInProgressOrDone) && (
          <Button onClick={resetAllAnalysis} variant="outline" size="lg" disabled={isLoadingOverall} className="w-full sm:w-auto">
            Clear All
          </Button>
        )}
      </div>

      {/* Individual Results Display */}
      {hasSelectedImages && (
        <div className="space-y-8 mt-8">
          {imageAnalysisResults.map((resultItem: ImageAnalysisResult) => (
            <div key={resultItem.selectedImage.id} className="bg-gray-50 p-6 rounded-xl shadow-md border border-gray-200 flex flex-col md:flex-row items-start md:space-x-6 space-y-4 md:space-y-0">
              {/* Pré-visualização da Imagem */}
              <div className="w-full md:w-1/3 flex-shrink-0">
                <ImagePreview 
                  src={resultItem.selectedImage.previewUrl} 
                  alt={resultItem.selectedImage.file.name} 
                  className="w-full h-48 object-contain rounded-lg" 
                />
                <p className="text-center text-sm text-gray-600 mt-2 truncate" title={resultItem.selectedImage.file.name}>
                  {resultItem.selectedImage.file.name}
                </p>
              </div>
              
              {/* Lista de Tags para esta imagem */}
              <div className="w-full md:w-2/3">
                <TagDisplayList 
                  tags={resultItem.response?.tags || []} 
                  isLoading={resultItem.isLoading} 
                  error={resultItem.error || undefined} 
                />
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Mensagem inicial ou quando não há resultado */}
      {/* --- CORREÇÃO AQUI: Condição para a mensagem inicial --- */}
      {!hasSelectedImages && (
        <div className="p-6 bg-blue-50 rounded-lg text-center text-blue-700 border border-blue-200">
            <p className="text-lg font-medium">
            Select or drag images to start the analysis.
            </p>
            <p className="text-sm text-blue-600 mt-2">
            Discover what artificial intelligence "sees" in your photos!
            </p>
        </div>
      )}
    </div>
  );
};

export default VisualTaggerModule;
