// frontend/src/types/frontend.d.ts

// Defines the interface for a single tag returned by the API
export interface Tag {
  name: string;
  confidence: number; // The tag confidence, from 0.0 to 1.0
  source_model: string; // O modelo de IA que gerou esta tag
}

// Defines the interface for the full image analysis API response
export interface ImageAnalysisResponse {
  image_id?: string; 
  filename?: string;
  tags: Tag[];
  message: string;
}

// Define a interface para os dados de CADA imagem selecionada no frontend
export interface SelectedImage {
  id: string; // Unique ID for each image in the frontend (useful for React keys)
  file: File;
  previewUrl: string; // URL para exibir a imagem no navegador
}

// Defines the interface for the COMPLETE result of the analysis of ONE image in the frontend
export interface ImageAnalysisResult {
  selectedImage: SelectedImage;
  response: ImageAnalysisResponse | null; // A resposta da API para esta imagem
  isLoading: boolean; // Estado de carregamento individual para esta imagem
  error: string | null; // Mensagem de erro individual para esta imagem
}
