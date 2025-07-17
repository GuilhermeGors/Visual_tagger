// frontend/src/services/api.ts

import { ImageAnalysisResponse } from '../types/frontend.d'; // Importa a interface de tipo

// URL base da sua API FastAPI
// In production, this would be an environment variable or configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:8000';

/**
 * Sends an image to the backend for analysis.
 * @param imageFile O arquivo de imagem a ser enviado.
 * @returns A Promise that resolves with the image analysis response.
 */
export const analyzeImage = async (imageFile: File): Promise<ImageAnalysisResponse> => {
  const formData = new FormData();
  formData.append('file', imageFile); // 'file' must match the parameter name in your FastAPI endpoint

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/analyze`, {
      method: 'POST',
      body: formData, // Para upload de arquivo, use FormData
      // Do not set 'Content-Type' for FormData; the browser will do this automatically with the correct boundary
    });

    if (!response.ok) {
      // Try to read the error message from the backend if the response is not OK
      const errorData = await response.json().catch(() => ({ detail: 'Erro desconhecido no servidor.' }));
      throw new Error(errorData.detail || `Erro HTTP: ${response.status} - ${response.statusText}`);
    }

    const data: ImageAnalysisResponse = await response.json();
    return data;
  } catch (error) {
    console.error('Error analyzing image:', error);
    throw error; // Propaga o erro para o hook/componente que chamou
  }
};
