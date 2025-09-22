import React from 'react';
import { X, Download, ExternalLink } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';

interface ImageModalProps {
  isOpen: boolean;
  onClose: () => void;
  image: {
    file: File;
    preview: string;
    analysis?: {
      light_percentage: number;
      shadow_percentage: number;
      processing_time: number;
    };
  };
}

export function ImageModal({ isOpen, onClose, image }: ImageModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
      <Card className="max-w-4xl w-full max-h-[90vh] overflow-hidden">
        <CardContent className="p-0">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b">
            <div>
              <h3 className="text-lg font-semibold">{image.file.name}</h3>
              <p className="text-sm text-muted-foreground">
                {(image.file.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* Image */}
          <div className="p-4">
            <div className="relative">
              <img
                src={image.preview}
                alt={image.file.name}
                className="w-full h-auto max-h-[60vh] object-contain rounded-lg"
              />
            </div>

            {/* Analysis Results */}
            {image.analysis && (
              <div className="mt-4 p-4 bg-muted rounded-lg">
                <h4 className="font-semibold mb-3">Resultados del Análisis</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-chart-1">
                      {image.analysis.light_percentage.toFixed(1)}%
                    </div>
                    <div className="text-sm text-muted-foreground">Luz</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-chart-2">
                      {image.analysis.shadow_percentage.toFixed(1)}%
                    </div>
                    <div className="text-sm text-muted-foreground">Sombra</div>
                  </div>
                </div>
                <div className="mt-3 text-center text-xs text-muted-foreground">
                  Procesado en {image.analysis.processing_time}ms
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

