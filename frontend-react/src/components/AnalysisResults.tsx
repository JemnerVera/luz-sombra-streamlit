import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';

interface AnalysisResult {
  light_percentage: number;
  shadow_percentage: number;
  processing_time: number;
  filename: string;
  imagen_resultado_url?: string;
  imagen_original_url?: string;
}

interface AnalysisResultsProps {
  results: AnalysisResult[];
}

export function AnalysisResults({ results }: AnalysisResultsProps) {
  if (results.length === 0) {
    return null;
  }

  const avgLight = results.reduce((acc, r) => acc + r.light_percentage, 0) / results.length;
  const avgShadow = results.reduce((acc, r) => acc + r.shadow_percentage, 0) / results.length;
  const avgProcessingTime = results.reduce((acc, r) => acc + r.processing_time, 0) / results.length;

  return (
    <div className="space-y-6">
      {/* Vista para una imagen */}
      {results.length === 1 && (
        <Card>
          <CardContent className="p-6">
            <div className="space-y-6">
              {/* Resultados por Imagen */}
                <div className="space-y-6">
                  <h4 className="text-lg font-semibold text-center">Resultados por Imagen</h4>
                  
                  {results.map((result, index) => (
                    <div key={index} className="text-center">
                      {/* Porcentajes lado a lado */}
                      <div className="flex justify-center gap-8">
                        <div className="text-center">
                          <div className="text-3xl font-bold text-chart-1 mb-1">
                            {result.light_percentage.toFixed(1)}%
                          </div>
                          <div className="text-sm font-medium text-muted-foreground">
                            Luz
                          </div>
                        </div>
                        
                        <div className="text-center">
                          <div className="text-3xl font-bold text-chart-2 mb-1">
                            {result.shadow_percentage.toFixed(1)}%
                          </div>
                          <div className="text-sm font-medium text-muted-foreground">
                            Sombra
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
          </CardContent>
        </Card>
      )}

      {/* Múltiples Imágenes - Vista de comparación */}
      {results.length > 1 && (
        <Card>
          <CardHeader>
            <CardTitle>Comparación de Imágenes</CardTitle>
            <CardDescription>Imágenes procesadas con análisis de luz y sombra</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {results.map((result, index) => (
                <div key={index} className="space-y-4">
                  <div className="text-center">
                    <h4 className="font-semibold text-lg mb-2">{result.filename}</h4>
                    
                    {/* Estadísticas de la imagen */}
                    <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
                      <div className="text-center">
                        <div className="font-semibold text-chart-1">{result.light_percentage.toFixed(1)}%</div>
                        <div className="text-muted-foreground">Luz</div>
                      </div>
                      <div className="text-center">
                        <div className="font-semibold text-chart-2">{result.shadow_percentage.toFixed(1)}%</div>
                        <div className="text-muted-foreground">Sombra</div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Resultados por Imagen para múltiples imágenes */}
            <div className="mt-8 pt-6 border-t">
              <div className="text-center mb-6">
                <h4 className="text-lg font-semibold">Resultados por Imagen</h4>
              </div>
              
              <div className="space-y-4">
                {results.map((result, index) => (
                  <div key={index} className="flex items-center justify-center p-4 bg-muted rounded-lg">
                    <div className="flex gap-8">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-chart-1">
                          {result.light_percentage.toFixed(1)}%
                        </div>
                        <div className="text-xs text-muted-foreground">Luz</div>
                      </div>
                      
                      <div className="text-center">
                        <div className="text-2xl font-bold text-chart-2">
                          {result.shadow_percentage.toFixed(1)}%
                        </div>
                        <div className="text-xs text-muted-foreground">Sombra</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}