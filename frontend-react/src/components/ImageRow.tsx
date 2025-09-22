import React, { useState } from 'react';
import { X, Eye, FileImage, Crop } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { ImageModal } from './ImageModal';

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

interface ImageRowProps {
  image: UploadedImage;
  index: number;
  onRemove: (index: number) => void;
  onCrop?: (index: number) => void;
  onUpdateImage?: (index: number, updates: Partial<UploadedImage>) => void;
}

export function ImageRow({ image, index, onRemove, onCrop, onUpdateImage }: ImageRowProps) {
  const [showModal, setShowModal] = useState(false);

  return (
    <>
      <Card className="hover:shadow-md transition-shadow">
        <CardContent className="p-4">
          <div className="flex items-center gap-4">
            {/* Thumbnail */}
            <div className="flex-shrink-0">
              <div className="w-16 h-16 rounded-lg overflow-hidden bg-muted">
                <img
                  src={image.preview}
                  alt={`Preview ${index + 1}`}
                  className="w-full h-full object-cover"
                />
              </div>
            </div>

            {/* File Info */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <FileImage className="h-4 w-4 text-muted-foreground" />
                <p className="font-medium truncate">{image.file.name}</p>
              </div>
              <p className="text-sm text-muted-foreground">
                {(image.file.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>

            {/* Analysis Results */}
            {image.analysis ? (
              <div className="flex items-center gap-6">
                <div className="text-center">
                  <div className="text-lg font-bold text-chart-1">
                    {image.analysis.light_percentage.toFixed(1)}%
                  </div>
                  <div className="text-xs text-muted-foreground">Luz</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-chart-2">
                    {image.analysis.shadow_percentage.toFixed(1)}%
                  </div>
                  <div className="text-xs text-muted-foreground">Sombra</div>
                </div>
                <div className="text-center">
                  <div className="text-sm font-medium">
                    {image.analysis.processing_time}ms
                  </div>
                  <div className="text-xs text-muted-foreground">Tiempo</div>
                </div>
              </div>
            ) : null}

            {/* Actions */}
            <div className="flex items-center gap-2">
              {/* Campos de ubicación específica */}
              <div className="flex gap-1">
                <input
                  type="text"
                  placeholder="Hilera"
                  value={image.hilera || ''}
                  onChange={(e) => onUpdateImage?.(index, { hilera: e.target.value })}
                  className="w-16 px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 text-gray-900"
                />
                <input
                  type="text"
                  placeholder="N° planta"
                  value={image.numeroPlanta || ''}
                  onChange={(e) => onUpdateImage?.(index, { numeroPlanta: e.target.value })}
                  className="w-16 px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 text-gray-900"
                />
              </div>
              
              {onCrop && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onCrop(index)}
                  className="flex items-center gap-2"
                >
                  <Crop className="h-4 w-4" />
                  Crop
                </Button>
              )}
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowModal(true)}
                className="flex items-center gap-2"
              >
                <Eye className="h-4 w-4" />
                Ver
              </Button>
              <Button
                variant="destructive"
                size="sm"
                onClick={() => onRemove(index)}
                className="h-8 w-8 p-0"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Modal */}
      <ImageModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        image={image}
      />
    </>
  );
}

