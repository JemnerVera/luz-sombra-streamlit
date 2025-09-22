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
  analysis?: {
    light_percentage: number;
    shadow_percentage: number;
    processing_time: number;
  };
}

interface ImageUploadProps {
  onAnalysisComplete?: (result: any) => void;
}

export function ImageUpload({ onAnalysisComplete }: ImageUploadProps) {
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
  };

  const handleFundoChange = (value: string) => {
    setFundo(value);
    setSector('');
    setLote('');
  };

  const handleSectorChange = (value: string) => {
    setSector(value);
    setLote('');
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

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  }, []);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    handleFiles(files);
  }, []);

  const handleFiles = useCallback((files: File[]) => {
    const imageFiles = files.filter((file) => file.type.startsWith("image/"));

    imageFiles.forEach((file) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const preview = e.target?.result as string;
        setImages((prev) => [...prev, { file, preview }]);
        setShowUploadArea(false); // Ocultar área de upload después de cargar
      };
      reader.readAsDataURL(file);
    });
  }, []);

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
  }, []);

  const analyzeImages = useCallback(async () => {
    if (images.length === 0) {
      alert('Por favor, sube al menos una imagen antes de analizar');
      return;
    }
    
    if (!empresa.trim() || !fundo.trim()) {
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
  }, [images, onAnalysisComplete, empresa, fundo, sector, lote]);

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
                      onChange={setLote}
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

      {/* Modal de validación */}
      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title="Información requerida"
      >
        <div className="space-y-4">
          <p className="text-gray-600">
            Por favor, selecciona la empresa y el fundo antes de analizar las imágenes.
          </p>
          <div className="flex justify-end">
            <Button onClick={() => setShowModal(false)}>
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