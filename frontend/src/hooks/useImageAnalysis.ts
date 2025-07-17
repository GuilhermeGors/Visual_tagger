import { useState, useCallback } from 'react';
import { analyzeImage } from '../services/api'; 
// import { ImageAnalysisResponse, SelectedImage, ImageAnalysisResult } from '../types/frontend.d'; // <--- REMOVER ImageAnalysisResponse AQUI
import { SelectedImage, ImageAnalysisResult } from '../types/frontend.d'; // <--- CORRIGIDO

interface UseImageAnalysisResult {
  imageAnalysisResults: ImageAnalysisResult[]; 
  isLoadingOverall: boolean; 
  handleImagesSelect: (images: SelectedImage[]) => void; 
  handleAnalyzeAllImages: () => Promise<void>; 
  resetAllAnalysis: () => void; 
}

const useImageAnalysis = (): UseImageAnalysisResult => {
  const [imageAnalysisResults, setImageAnalysisResults] = useState<ImageAnalysisResult[]>([]);
  const [isLoadingOverall, setIsLoadingOverall] = useState<boolean>(false); 

  const handleImagesSelect = useCallback((images: SelectedImage[]) => {
    const newAnalysisResults: ImageAnalysisResult[] = images.map(image => ({
      selectedImage: image,
      response: null,
      isLoading: false, 
      error: null,
    }));
    setImageAnalysisResults(newAnalysisResults); 
    setIsLoadingOverall(false); 
  }, []);

  const handleAnalyzeAllImages = useCallback(async () => {
    if (imageAnalysisResults.length === 0) {
      console.warn("No image selected for analysis.");
      return;
    }

    setIsLoadingOverall(true); 

    const updatedResultsPromises = imageAnalysisResults.map(async (resultItem, index) => {
      const updatedItem: ImageAnalysisResult = { 
        ...resultItem, 
        isLoading: true, 
        error: null, 
        response: resultItem.response 
      };

      setImageAnalysisResults(prevResults => {
        const newArray = [...prevResults];
        newArray[index] = updatedItem;
        return newArray;
      });

      try {
        const apiResponse = await analyzeImage(resultItem.selectedImage.file);
        updatedItem.response = apiResponse;
      } catch (err: any) {
        updatedItem.error = err.message || 'Ocorreu um erro ao analisar esta imagem.';
        console.error(`Error analyzing image ${resultItem.selectedImage.file.name}:`, err); 
      } finally {
        updatedItem.isLoading = false; 
      }
      return updatedItem;
    });

    const finalUpdatedResults = await Promise.all(updatedResultsPromises);
    setImageAnalysisResults(finalUpdatedResults); 
    setIsLoadingOverall(false); 
  }, [imageAnalysisResults]);

  const resetAllAnalysis = useCallback(() => {
    setImageAnalysisResults([]);
    setIsLoadingOverall(false);
  }, []);

  return {
    imageAnalysisResults,
    isLoadingOverall,
    handleImagesSelect,
    handleAnalyzeAllImages,
    resetAllAnalysis,
  };
};

export default useImageAnalysis;
