import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

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

      {/* Múltiples Imágenes - Vista simplificada */}
      {results.length > 1 && (
        <Card>
          <CardContent className="p-6">
            <div className="space-y-6">
              <h4 className="text-lg font-semibold text-center">Resultados por Imagen</h4>
              
              <div className="space-y-4">
                {results.map((result, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-muted rounded-lg">
                    {/* Nombre de la imagen */}
                    <div className="flex-1">
                      <p className="font-medium text-sm text-gray-700">{result.filename}</p>
                    </div>
                    
                    {/* Porcentajes */}
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
                    
                    {/* Fecha */}
                    <div className="flex-1 text-right">
                      <p className="text-xs text-muted-foreground">
                        {new Date().toLocaleDateString('es-ES', {
                          day: '2-digit',
                          month: '2-digit',
                          year: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </p>
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