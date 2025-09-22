import React, { useState, useCallback, useRef } from 'react';
import { Upload, Loader2, Eye, EyeOff } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

interface ModelTestProps {
  onTestComplete?: (result: any) => void;
}

export function ModelTest({ onTestComplete }: ModelTestProps) {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [testing, setTesting] = useState(false);
  const [showVisual, setShowVisual] = useState(true);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
      setAnalysisResult(null);
    }
  }, []);

  const testModel = useCallback(async () => {
    if (!selectedImage) return;

    setTesting(true);
    try {
      const formData = new FormData();
      formData.append('imagen', selectedImage);
      formData.append('empresa', 'Test Modelo');
      formData.append('fundo', 'Test Modelo');
      formData.append('sector', '');
      formData.append('lote', '');

      console.log('Enviando datos:', {
        imagen: selectedImage.name,
        empresa: 'Test Modelo',
        fundo: 'Test Modelo',
        sector: '',
        lote: ''
      });

      const response = await fetch('http://localhost:8000/procesar-imagen-visual', {
        method: 'POST',
        body: formData,
      });

      console.log('Respuesta del servidor:', response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error del servidor:', errorText);
        throw new Error(`Error en la API: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      
      if (data.success) {
        setAnalysisResult({
          light_percentage: data.porcentaje_luz,
          shadow_percentage: data.porcentaje_sombra,
          filename: selectedImage.name,
          imagen_visual: data.imagen_visual
        });
        
        if (onTestComplete) {
          onTestComplete(data);
        }
      } else {
        throw new Error(data.mensaje || 'Error en el procesamiento');
      }
    } catch (error) {
      console.error('Error probando modelo:', error);
      alert(`Error probando modelo: ${error.message}`);
    } finally {
      setTesting(false);
    }
  }, [selectedImage, onTestComplete]);

  const resetTest = useCallback(() => {
    setSelectedImage(null);
    setImagePreview(null);
    setAnalysisResult(null);
    setShowVisual(true);
  }, []);

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Eye className="h-5 w-5" />
            Probar Modelo de Reconocimiento
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Instrucciones */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-semibold text-blue-900 mb-2">¿Cómo funciona?</h3>
            <p className="text-blue-800 text-sm mb-3">
              Sube una imagen para ver cómo el modelo identifica las áreas de luz y sombra. 
              El modelo generará una imagen de análisis completa con colores distintivos y estadísticas.
            </p>
            <div className="flex items-center gap-4 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-yellow-400 rounded"></div>
                <span className="text-blue-800">Luz detectada (Amarillo)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-gray-600 rounded"></div>
                <span className="text-blue-800">Sombra detectada (Gris)</span>
              </div>
            </div>
            <p className="text-blue-800 text-xs mt-2 italic">
              La imagen de análisis incluye una leyenda con los porcentajes calculados
            </p>
          </div>

          {/* Selector de imagen */}
          <div className="space-y-4">
            <div className="flex items-center gap-4">
              <Button
                onClick={() => fileInputRef.current?.click()}
                disabled={testing}
                className="flex items-center gap-2"
              >
                <Upload className="h-4 w-4" />
                {selectedImage ? 'Cambiar Imagen' : 'Seleccionar Imagen'}
              </Button>
              
              {selectedImage && (
                <Button
                  onClick={resetTest}
                  variant="outline"
                  disabled={testing}
                >
                  Limpiar
                </Button>
              )}
            </div>

            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageSelect}
              className="hidden"
            />
          </div>

          {/* Vista previa y análisis */}
          {imagePreview && (
            <div className="space-y-4">
              <div className="relative">
                {analysisResult && analysisResult.imagen_visual && showVisual ? (
                  <div className="text-center">
                    <h3 className="text-lg font-semibold mb-3 text-gray-800">Análisis Visual del Modelo</h3>
                    <img
                      src={analysisResult.imagen_visual}
                      alt="Análisis de luz y sombra"
                      className="w-full max-w-lg mx-auto rounded-lg border-2 border-gray-300 shadow-xl"
                    />
                  </div>
                ) : (
                  <div className="text-center">
                    <h3 className="text-lg font-semibold mb-3 text-gray-800">Imagen Original</h3>
                    <img
                      src={imagePreview}
                      alt="Imagen de prueba"
                      className="w-full max-w-lg mx-auto rounded-lg border-2 border-gray-300 shadow-xl"
                    />
                  </div>
                )}
              </div>

              {/* Controles */}
              <div className="flex items-center justify-center gap-4 flex-wrap">
                <Button
                  onClick={testModel}
                  disabled={testing}
                  className="flex items-center gap-2"
                >
                  {testing ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                  {testing ? 'Analizando...' : 'Probar Modelo'}
                </Button>

                {analysisResult && (
                  <Button
                    onClick={() => setShowVisual(!showVisual)}
                    variant="outline"
                    className="flex items-center gap-2"
                  >
                    {showVisual ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    {showVisual ? 'Ver Original' : 'Ver Análisis'}
                  </Button>
                )}
              </div>

              {/* Ventana de análisis debajo de los controles */}
              {analysisResult && (
                <div className="bg-white p-6 rounded-lg shadow-xl max-w-2xl mx-auto border">
                  <h3 className="font-semibold text-lg mb-4 text-center text-black">Análisis del Modelo</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Luz detectada:</span>
                      <span className="font-semibold text-yellow-600">
                        {analysisResult.light_percentage.toFixed(1)}%
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Sombra detectada:</span>
                      <span className="font-semibold text-gray-600">
                        {analysisResult.shadow_percentage.toFixed(1)}%
                      </span>
                    </div>
                    <div className="pt-2 border-t">
                      <div className="flex justify-between items-center text-sm text-gray-500">
                        <span>Archivo:</span>
                        <span className="truncate max-w-32">{analysisResult.filename}</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Resultados detallados */}
          {analysisResult && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Resultados del Análisis</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div className="text-center">
                      <div className="text-3xl font-bold text-green-600">
                        {analysisResult.light_percentage.toFixed(1)}%
                      </div>
                      <div className="text-sm text-gray-600">Área de Luz</div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div 
                        className="bg-green-500 h-3 rounded-full transition-all duration-500"
                        style={{ width: `${analysisResult.light_percentage}%` }}
                      ></div>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="text-center">
                      <div className="text-3xl font-bold text-blue-600">
                        {analysisResult.shadow_percentage.toFixed(1)}%
                      </div>
                      <div className="text-sm text-gray-600">Área de Sombra</div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div 
                        className="bg-blue-500 h-3 rounded-full transition-all duration-500"
                        style={{ width: `${analysisResult.shadow_percentage}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
