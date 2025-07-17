import React, { useState, useCallback, ChangeEvent, DragEvent, useEffect } from 'react'; // Adicionado useEffect
import Button from '../../atoms/Button/Button';
import ImagePreview from '../../atoms/ImagePreview/ImagePreview';
import { SelectedImage } from '../../../types/frontend.d';
import { v4 as uuidv4 } from 'uuid'; 

interface ImageUploadAreaProps {
  onImagesSelect: (images: SelectedImage[]) => void; 
  isLoading?: boolean; 
}

const ImageUploadArea: React.FC<ImageUploadAreaProps> = ({ onImagesSelect, isLoading = false }) => {
  const [internalSelectedImages, setInternalSelectedImages] = useState<SelectedImage[]>([]); // Estado interno
  const [dragActive, setDragActive] = useState<boolean>(false);
  const fileInputRef = React.useRef<HTMLInputElement>(null);

  // Sincroniza o estado interno com a prop onImagesSelect quando internalSelectedImages muda
  useEffect(() => {
    onImagesSelect(internalSelectedImages);
  }, [internalSelectedImages, onImagesSelect]);


  // Processa uma lista de arquivos (do input ou drag/drop)
  const processFiles = useCallback((files: FileList | null) => {
    if (!files) return;

    const newImagesToProcess: File[] = Array.from(files);
    let processedCount = 0;
    const tempNewImages: SelectedImage[] = [];
    const invalidFiles: string[] = [];

    if (newImagesToProcess.length === 0) return; // Nenhuma imagem para processar

    newImagesToProcess.forEach(file => {
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onloadend = () => {
          tempNewImages.push({
            id: uuidv4(), 
            file: file,
            previewUrl: reader.result as string,
          });
          processedCount++;
          if (processedCount === newImagesToProcess.length) {
            // Quando todas as imagens foram lidas, atualiza o estado de uma vez
            setInternalSelectedImages(prevImages => [...prevImages, ...tempNewImages]);
          }
        };
        reader.readAsDataURL(file);
      } else {
        invalidFiles.push(file.name);
        processedCount++; // Also count invalid files for the total
        if (processedCount === newImagesToProcess.length) {
            setInternalSelectedImages(prevImages => [...prevImages, ...tempNewImages]);
        }
      }
    });

    if (invalidFiles.length > 0) {
      alert(`The following files are not images and were ignored: ${invalidFiles.join(', ')}`);
    }
  }, []); // Adjusted dependencies

  // Handles file selection via input (now accepts multiple)
  const handleFileChange = useCallback((event: ChangeEvent<HTMLInputElement>) => {
    processFiles(event.target.files);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  }, [processFiles]);

  // Handles drag event over the area
  const handleDrag = useCallback((e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  // Handles file drop event (now accepts multiple)
  const handleDrop = useCallback((e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    processFiles(e.dataTransfer.files);
  }, [processFiles]);

  // Handles click on the "Select Image" button
  const onButtonClick = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  // Handles removal of ALL selected images
  const handleClearAllImages = useCallback(() => {
    setInternalSelectedImages([]); // Limpa o estado interno
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  }, []); // Adjusted dependencies

  return (
    <div
      className={`relative p-6 border-2 border-dashed rounded-lg text-center transition-colors duration-200 ${
        dragActive ? 'border-primary bg-blue-50' : 'border-gray-300 bg-white'
      }`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input
        type="file"
        id="file-upload"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="image/*"
        multiple
        className="hidden"
      />

      {internalSelectedImages.length > 0 ? (
        <div className="flex flex-col items-center space-y-4">
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 w-full max-h-60 overflow-y-auto p-2 border rounded-lg bg-gray-50">
            {internalSelectedImages.map(image => (
              <ImagePreview 
                key={image.id} 
                src={image.previewUrl} 
                alt={image.file.name} 
                className="w-full h-24 object-cover" 
              />
            ))}
          </div>
          <p className="text-gray-700 text-sm">
            {internalSelectedImages.length} image(s) selected.
          </p>
          <Button onClick={handleClearAllImages} variant="outline" size="sm">
            Clear All Images
          </Button>
        </div>
      ) : (
        <div className="flex flex-col items-center space-y-4">
          <p className="text-gray-600">drag and drop images here, or</p>
          <Button onClick={onButtonClick} isLoading={isLoading}>
            Select Images
          </Button>
          <p className="text-gray-500 text-sm mt-2">supported formats: JPEG, PNG, GIF</p>
        </div>
      )}
    </div>
  );
};

export default ImageUploadArea;
