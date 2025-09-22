import React from 'react';
import { ImageUpload } from './ImageUpload';
import { AnalysisResults } from './AnalysisResults';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Upload } from 'lucide-react';

interface AnalysisResult {
  light_percentage: number;
  shadow_percentage: number;
  processing_time: number;
  filename: string;
  imagen_resultado_url?: string;
  imagen_original_url?: string;
}

interface AnalyzeTabProps {
  analysisResults: AnalysisResult[];
  onAnalysisComplete: (result: AnalysisResult) => void;
  onDataChange?: () => void;
}

export function AnalyzeTab({ analysisResults, onAnalysisComplete, onDataChange }: AnalyzeTabProps) {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center space-y-4">
        <h2 className="text-4xl font-bold text-balance">Análisis de Imágenes</h2>
      </div>

      {/* Upload Section - Solo se muestra si no hay resultados */}
      {analysisResults.length === 0 && (
        <Card className="border-2">
          <CardContent className="p-6">
            <ImageUpload onAnalysisComplete={onAnalysisComplete} onDataChange={onDataChange} />
          </CardContent>
        </Card>
      )}

      {/* Results Section - Solo se muestra si hay resultados */}
      {analysisResults.length > 0 && (
        <div className="space-y-6">
          <div className="flex justify-center">
            <Button 
              variant="outline" 
              onClick={() => window.location.reload()}
              className="flex items-center gap-2"
            >
              <Upload className="h-4 w-4" />
              Subir Nuevas Imágenes
            </Button>
          </div>
          <AnalysisResults results={analysisResults} />
        </div>
      )}
    </div>
  );
}
