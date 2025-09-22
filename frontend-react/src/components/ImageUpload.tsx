import React, { useState, useCallback, useRef, useEffect } from 'react';
import { Upload, Loader2, ImageIcon, Plus } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { Progress } from './ui/progress';
import { ImageRow } from './ImageRow';
import { Modal } from './ui/modal';
import { SearchableDropdown } from './ui/SearchableDropdown';
import { ImageCropper } from './ui/ImageCropper';

interface UploadedImage {
  file: File;
  preview: string;
  hilera?: string;
  numeroPlanta?: string;
  hasGps?: boolean;
  gpsData?: {
    latitud: number;
    longitud: number;
    direccion: string;
  };
  analysis?: {
    light_percentage: number;
    shadow_percentage: number;
    processing_time: number;
  };
}

interface ImageUploadProps {
  onAnalysisComplete?: (result: any) => void;
  onDataChange?: () => void;
}

export function ImageUpload({ onAnalysisComplete, onDataChange }: ImageUploadProps) {
  const [images, setImages] = useState<UploadedImage[]>([]);
  const [dragActive, setDragActive] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [showUploadArea, setShowUploadArea] = useState(true);
  const [empresa, setEmpresa] = useState('');
  const [fundo, setFundo] = useState('');
  const [sector, setSector] = useState('');
  const [lote, setLote] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [showCropper, setShowCropper] = useState(false);
  const [croppingImageIndex, setCroppingImageIndex] = useState<number | null>(null);
  const [validationErrors, setValidationErrors] = useState<{
    generalMissingFields: string[];
    imagesWithMissingFields: Array<{
      filename: string;
      missingFields: string[];
    }>;
  }>({
    generalMissingFields: [],
    imagesWithMissingFields: []
  });
  const [fieldData, setFieldData] = useState({
    empresa: [],
    fundo: [],
    sector: [],
    lote: [],
    hierarchical: {}
  });
  const fileInputRef = useRef<HTMLInputElement>(null);
  const addMoreInputRef = useRef<HTMLInputElement>(null);

  // Cargar datos de los dropdowns al montar el componente
  useEffect(() => {
    const loadFieldData = async () => {
      try {
        const response = await fetch('http://localhost:8000/google-sheets/field-data');
        if (response.ok) {
          const data = await response.json();
          setFieldData(data);
        } else {
          console.error('Error cargando datos de campo:', response.statusText);
        }
      } catch (error) {
        console.error('Error cargando datos de campo:', error);
      }
    };

    loadFieldData();
  }, []);

  // Funciones para filtros jerárquicos
  const getFilteredFundos = () => {
    if (!empresa || !fieldData.hierarchical[empresa]) {
      return fieldData.fundo;
    }
    return Object.keys(fieldData.hierarchical[empresa]);
  };

  const getFilteredSectores = () => {
    if (!empresa || !fundo || !fieldData.hierarchical[empresa] || !fieldData.hierarchical[empresa][fundo]) {
      return fieldData.sector;
    }
    return Object.keys(fieldData.hierarchical[empresa][fundo]);
  };

  const getFilteredLotes = () => {
    if (!empresa || !fundo || !sector || 
        !fieldData.hierarchical[empresa] || 
        !fieldData.hierarchical[empresa][fundo] || 
        !fieldData.hierarchical[empresa][fundo][sector]) {
      return fieldData.lote;
    }
    return fieldData.hierarchical[empresa][fundo][sector];
  };

  // Limpiar campos dependientes cuando cambia un campo padre
  const handleEmpresaChange = (value: string) => {
    setEmpresa(value);
    setFundo('');
    setSector('');
    setLote('');
    onDataChange?.();
  };

  const handleFundoChange = (value: string) => {
    setFundo(value);
    setSector('');
    setLote('');
    onDataChange?.();
  };

  const handleSectorChange = (value: string) => {
    setSector(value);
    setLote('');
    onDataChange?.();
  };

  const handleLoteChange = (value: string) => {
    setLote(value);
    onDataChange?.();
  };

  // Función para verificar si una imagen tiene GPS
  const checkImageGps = async (file: File): Promise<{hasGps: boolean, gpsData?: any}> => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch('http://localhost:8000/check-gps-info', {
        method: 'POST',
        body: formData
      });
      
      if (response.ok) {
        const data = await response.json();
        return {
          hasGps: data.has_gps,
          gpsData: data.gps_data
        };
      } else {
        console.error('Error verificando GPS:', response.statusText);
        return { hasGps: false };
      }
    } catch (error) {
      console.error('Error verificando GPS:', error);
      return { hasGps: false };
    }
  };

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleFiles = useCallback(async (files: File[]) => {
    const imageFiles = files.filter((file) => file.type.startsWith("image/"));

    for (const file of imageFiles) {
      const reader = new FileReader();
      reader.onload = async (e) => {
        const preview = e.target?.result as string;
        
        // Verificar si la imagen tiene GPS
        const gpsInfo = await checkImageGps(file);
        
        setImages((prev) => [...prev, { 
          file, 
          preview, 
          hasGps: gpsInfo.hasGps,
          gpsData: gpsInfo.gpsData
        }]);
        setShowUploadArea(false); // Ocultar área de upload después de cargar
        onDataChange?.(); // Notificar que hay datos sin guardar
      };
      reader.readAsDataURL(file);
    }
  }, [onDataChange]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  }, [handleFiles]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    handleFiles(files);
  }, [handleFiles]);

  const removeImage = useCallback((index: number) => {
    setImages((prev) => {
      const newImages = prev.filter((_, i) => i !== index);
      if (newImages.length === 0) {
        setShowUploadArea(true); // Mostrar área de upload si no hay imágenes
      }
      return newImages;
    });
  }, []);

  const addMoreImages = useCallback(() => {
    addMoreInputRef.current?.click();
  }, []);

  const handleCropImage = useCallback((index: number) => {
    setCroppingImageIndex(index);
    setShowCropper(true);
  }, []);

  const handleCropComplete = useCallback((croppedBlob: Blob) => {
    if (croppingImageIndex !== null) {
      const croppedFile = new File([croppedBlob], `cropped_${images[croppingImageIndex].file.name}`, {
        type: 'image/jpeg'
      });
      
      const reader = new FileReader();
      reader.onload = (e) => {
        const preview = e.target?.result as string;
        setImages((prev) => prev.map((img, idx) => 
          idx === croppingImageIndex 
            ? { ...img, file: croppedFile, preview } 
            : img
        ));
      };
      reader.readAsDataURL(croppedFile);
    }
    
    setShowCropper(false);
    setCroppingImageIndex(null);
  }, [croppingImageIndex, images]);

  const handleCropClose = useCallback(() => {
    setShowCropper(false);
    setCroppingImageIndex(null);
  }, []);

  const handleUpdateImage = useCallback((index: number, updates: Partial<UploadedImage>) => {
    setImages(prevImages => 
      prevImages.map((img, i) => 
        i === index ? { ...img, ...updates } : img
      )
    );
    onDataChange?.(); // Notificar que hay datos sin guardar
  }, [onDataChange]);

  // Función para validar todos los campos requeridos
  const validateRequiredFields = () => {
    const missingFields = [];
    
    // Validar campos generales obligatorios
    if (!empresa.trim()) missingFields.push('Empresa');
    if (!fundo.trim()) missingFields.push('Fundo');
    if (!sector.trim()) missingFields.push('Sector');
    if (!lote.trim()) missingFields.push('Lote');
    
    // Validar campos obligatorios para imágenes sin GPS
    const imagesWithoutGps = images.filter(img => !img.hasGps);
    const imagesWithMissingFields = [];
    
    for (let i = 0; i < imagesWithoutGps.length; i++) {
      const image = imagesWithoutGps[i];
      const imageMissingFields = [];
      
      if (!image.hilera?.trim()) imageMissingFields.push('Hilera');
      if (!image.numeroPlanta?.trim()) imageMissingFields.push('N° planta');
      
      if (imageMissingFields.length > 0) {
        imagesWithMissingFields.push({
          filename: image.file.name,
          missingFields: imageMissingFields
        });
      }
    }
    
    return {
      hasErrors: missingFields.length > 0 || imagesWithMissingFields.length > 0,
      generalMissingFields: missingFields,
      imagesWithMissingFields: imagesWithMissingFields
    };
  };

  const analyzeImages = useCallback(async () => {
    if (images.length === 0) {
      alert('Por favor, sube al menos una imagen antes de analizar');
      return;
    }
    
    // Validar todos los campos requeridos
    const validation = validateRequiredFields();
    if (validation.hasErrors) {
      setValidationErrors({
        generalMissingFields: validation.generalMissingFields,
        imagesWithMissingFields: validation.imagesWithMissingFields
      });
      setShowModal(true);
      return;
    }

    setAnalyzing(true);
    setProgress(0);

    const allResults = [];

    for (let i = 0; i < images.length; i++) {
      const image = images[i];

      try {
        // Llamada real a la API
        const analysis = await analyzeImageWithAPI(image.file, empresa, fundo, sector, lote, image.hilera, image.numeroPlanta);

        // Actualizar la imagen con el análisis
        setImages((prev) => prev.map((img, idx) => (idx === i ? { ...img, analysis } : img)));

        // Crear resultado para esta imagen
        const result = {
          filename: image.file.name,
          imagen_original_url: image.preview,
          ...analysis,
        };

        allResults.push(result);

        // Llamar al callback para cada imagen individualmente
        if (onAnalysisComplete) {
          onAnalysisComplete(result);
        }

        // Pequeña pausa entre análisis para mostrar progreso
        await new Promise(resolve => setTimeout(resolve, 500));

      } catch (error) {
        console.error("Error analyzing image:", error);
        // Mostrar error al usuario
        alert(`Error analizando ${image.file.name}: ${error.message}`);
      }

      setProgress(((i + 1) / images.length) * 100);
    }

    setAnalyzing(false);
  }, [images, onAnalysisComplete, empresa, fundo, sector, lote, validateRequiredFields]);

  return (
    <div className="space-y-6">
      {/* Información del Fundo - Siempre visible */}
      <Card>
        <CardContent className="p-6">
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div>
                    <label className="text-sm font-medium text-muted-foreground mb-2 block">
                      Empresa *
                    </label>
                    <SearchableDropdown
                      options={fieldData.empresa}
                      value={empresa}
                      onChange={handleEmpresaChange}
                      placeholder="Seleccionar empresa"
                      required
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium text-muted-foreground mb-2 block">
                      Fundo *
                    </label>
                    <SearchableDropdown
                      options={getFilteredFundos()}
                      value={fundo}
                      onChange={handleFundoChange}
                      placeholder="Seleccionar fundo"
                      required
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium text-muted-foreground mb-2 block">
                      Sector
                    </label>
                    <SearchableDropdown
                      options={getFilteredSectores()}
                      value={sector}
                      onChange={handleSectorChange}
                      placeholder="Seleccionar sector"
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium text-muted-foreground mb-2 block">
                      Lote
                    </label>
                    <SearchableDropdown
                      options={getFilteredLotes()}
                      value={lote}
                      onChange={handleLoteChange}
                      placeholder="Seleccionar lote"
                    />
                  </div>
                </div>
          </div>
        </CardContent>
      </Card>

      {/* Upload Area - Solo se muestra si no hay imágenes */}
      {showUploadArea && (
        <div className="space-y-6">
          {/* Área de Upload */}
          <Card className="border-2 border-dashed border-border hover:border-accent transition-colors">
            <CardContent className="p-8">
              <div
                className={`relative flex flex-col items-center justify-center space-y-4 ${
                  dragActive ? "bg-accent/10" : ""
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <div className="flex flex-col items-center space-y-2">
                  <div className="h-12 w-12 text-muted-foreground">
                    <Upload />
                  </div>
                  <div className="text-center">
                    <p className="text-lg font-medium text-balance">Arrastra y suelta tus imágenes aquí</p>
                    <p className="text-sm text-muted-foreground">o haz clic para seleccionar archivos</p>
                  </div>
                </div>

                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  accept="image/*"
                  onChange={handleFileInput}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />

                <Button variant="secondary" className="pointer-events-none">
                  Seleccionar Imágenes
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Progress Bar */}
      {analyzing && (
        <Card>
          <CardContent className="p-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span>Analizando imágenes...</span>
                <span>{Math.round(progress)}%</span>
              </div>
              <Progress value={progress} className="w-full" />
            </div>
          </CardContent>
        </Card>
      )}

      {/* Image List - Solo se muestra si hay imágenes */}
      {images.length > 0 && (
        <div className="space-y-4">
          {/* Input oculto para agregar más imágenes */}
          <input
            ref={addMoreInputRef}
            type="file"
            multiple
            accept="image/*"
            onChange={handleFileInput}
            className="hidden"
          />
          
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Imágenes Cargadas ({images.length})</h3>
            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={addMoreImages}
                disabled={analyzing}
                className="flex items-center gap-2"
              >
                <Plus className="h-4 w-4" />
                Agregar Imágenes
              </Button>
              <Button
                onClick={analyzeImages}
                disabled={analyzing || images.some((img) => img.analysis)}
                className="flex items-center gap-2"
              >
                {analyzing ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <ImageIcon className="h-4 w-4" />
                )}
                Analizar Imágenes
              </Button>
            </div>
          </div>

          {/* Image Rows */}
          <div className="space-y-3">
            {images.map((image, index) => (
              <ImageRow
                key={index}
                image={image}
                index={index}
                onRemove={removeImage}
                onCrop={handleCropImage}
                onUpdateImage={handleUpdateImage}
              />
            ))}
          </div>
        </div>
      )}

      {/* Modal de validación dinámico */}
      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title="Información requerida"
      >
        <div className="space-y-6">
          <div className="text-center">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
              <svg className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-white mb-2">
              Campos obligatorios faltantes
            </h3>
            <p className="text-sm text-gray-300">
              Completa la siguiente información antes de analizar las imágenes:
            </p>
          </div>
          
          {/* Campos generales faltantes */}
          {validationErrors.generalMissingFields.length > 0 && (
            <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-r-lg">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h4 className="text-sm font-medium text-red-800">Información general requerida:</h4>
                  <div className="mt-2 text-sm text-red-700">
                    <ul className="list-disc list-inside space-y-1">
                      {validationErrors.generalMissingFields.map((field, index) => (
                        <li key={index} className="font-medium">{field}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {/* Campos faltantes por imagen */}
          {validationErrors.imagesWithMissingFields.length > 0 && (
            <div className="bg-amber-50 border-l-4 border-amber-400 p-4 rounded-r-lg">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-amber-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h4 className="text-sm font-medium text-amber-800">Ubicación específica requerida (imágenes sin GPS):</h4>
                  <div className="mt-2 text-sm text-amber-700">
                    <div className="space-y-3">
                      {validationErrors.imagesWithMissingFields.map((imageError, index) => (
                        <div key={index} className="bg-amber-100 p-3 rounded-lg">
                          <p className="font-medium text-amber-900 mb-1">{imageError.filename}:</p>
                          <ul className="list-disc list-inside ml-4 space-y-1">
                            {imageError.missingFields.map((field, fieldIndex) => (
                              <li key={fieldIndex} className="font-medium">{field}</li>
                            ))}
                          </ul>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div className="flex justify-center pt-4">
            <Button 
              onClick={() => setShowModal(false)}
              className="px-6 py-2 bg-orange-600 hover:bg-orange-700 text-white font-medium rounded-lg transition-colors"
            >
              Entendido
            </Button>
          </div>
        </div>
      </Modal>

      {/* Image Cropper Modal */}
      {showCropper && croppingImageIndex !== null && (
        <ImageCropper
          imageSrc={images[croppingImageIndex].preview}
          onCropComplete={handleCropComplete}
          onClose={handleCropClose}
        />
      )}
    </div>
  );
}

// Función para análisis con la API (con fallback a simulación)
async function analyzeImageWithAPI(file: File, empresa: string, fundo: string, sector: string, lote: string, hilera?: string, numeroPlanta?: string): Promise<{
  light_percentage: number;
  shadow_percentage: number;
  processing_time: number;
  imagen_resultado_url: string;
}> {
  try {
    // Intentar conectar con la API real (endpoint simplificado)
    const formData = new FormData();
    formData.append('imagen', file);
    formData.append('empresa', empresa);
    formData.append('fundo', fundo);
    if (sector) formData.append('sector', sector);
    if (lote) formData.append('lote', lote);
    if (hilera) formData.append('hilera', hilera);
    if (numeroPlanta) formData.append('numero_planta', numeroPlanta);

    const response = await fetch('http://localhost:8000/procesar-imagen-simple', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Error en la API: ${response.status}`);
    }

    const data = await response.json();
    
    if (data.success) {
      return {
        light_percentage: data.porcentaje_luz,
        shadow_percentage: data.porcentaje_sombra,
        processing_time: Math.round(Math.random() * 1000 + 500), // Simular tiempo de procesamiento
        imagen_resultado_url: data.imagen_resultado_url || '/placeholder-resultado.png'
      };
    } else {
      throw new Error(data.mensaje || 'Error en el procesamiento');
    }
  } catch (error) {
    console.error('Error en la API:', error);
    throw new Error(`Error procesando imagen: ${error.message}`);
  }
}