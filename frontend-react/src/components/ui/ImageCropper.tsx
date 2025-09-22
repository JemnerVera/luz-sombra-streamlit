import React, { useState, useRef, useCallback, useEffect } from 'react';
import ReactCrop, { Crop, PixelCrop, centerCrop, makeAspectCrop } from 'react-image-crop';
import { Button } from './button';
import { X, Crop as CropIcon, RotateCcw } from 'lucide-react';
import 'react-image-crop/dist/ReactCrop.css';

interface ImageCropperProps {
  imageSrc: string;
  onCropComplete: (croppedImageBlob: Blob) => void;
  onClose: () => void;
}

export function ImageCropper({ imageSrc, onCropComplete, onClose }: ImageCropperProps) {
  const [crop, setCrop] = useState<Crop>();
  const [completedCrop, setCompletedCrop] = useState<PixelCrop>();
  const [scale, setScale] = useState(1);
  const [rotate, setRotate] = useState(0);
  const [aspect, setAspect] = useState<number | undefined>(undefined);
  const imgRef = useRef<HTMLImageElement>(null);
  const previewCanvasRef = useRef<HTMLCanvasElement>(null);

  const onImageLoad = useCallback((e: React.SyntheticEvent<HTMLImageElement>) => {
    const { width, height } = e.currentTarget;
    const crop = centerCrop(
      makeAspectCrop(
        {
          unit: '%',
          width: 90,
        },
        16 / 9,
        width,
        height
      ),
      width,
      height
    );
    setCrop(crop);
  }, []);

  const drawCroppedImage = useCallback(() => {
    if (!imgRef.current || !previewCanvasRef.current || !completedCrop) {
      return;
    }

    const image = imgRef.current;
    const canvas = previewCanvasRef.current;
    const ctx = canvas.getContext('2d');

    if (!ctx) {
      return;
    }

    const scaleX = image.naturalWidth / image.width;
    const scaleY = image.naturalHeight / image.height;
    const pixelRatio = window.devicePixelRatio;

    canvas.width = Math.floor(completedCrop.width * scaleX * pixelRatio);
    canvas.height = Math.floor(completedCrop.height * scaleY * pixelRatio);

    ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    ctx.imageSmoothingQuality = 'high';

    ctx.drawImage(
      image,
      Math.floor(completedCrop.x * scaleX),
      Math.floor(completedCrop.y * scaleY),
      Math.floor(completedCrop.width * scaleX),
      Math.floor(completedCrop.height * scaleY),
      0,
      0,
      Math.floor(completedCrop.width * scaleX),
      Math.floor(completedCrop.height * scaleY)
    );
  }, [completedCrop]);

  const onDownloadCropClick = useCallback(() => {
    if (!previewCanvasRef.current || !completedCrop) {
      return;
    }

    // Dibujar la imagen cropeada en el canvas
    drawCroppedImage();

    const canvas = previewCanvasRef.current;
    canvas.toBlob((blob) => {
      if (blob) {
        onCropComplete(blob);
      }
    }, 'image/jpeg', 0.9);
  }, [completedCrop, onCropComplete, drawCroppedImage]);

  // Actualizar vista previa cuando cambie el crop
  useEffect(() => {
    if (completedCrop) {
      drawCroppedImage();
    }
  }, [completedCrop, drawCroppedImage]);

  const resetCrop = () => {
    setCrop(undefined);
    setCompletedCrop(undefined);
    setScale(1);
    setRotate(0);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl max-h-[90vh] w-full overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <div className="flex items-center gap-2">
            <CropIcon className="w-5 h-5 text-blue-600" />
            <h2 className="text-lg font-semibold text-gray-900">Recortar Imagen</h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 p-1"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-4 overflow-auto max-h-[calc(90vh-120px)]">
          <div className="space-y-4">
            {/* Controls */}
            <div className="flex flex-wrap gap-4 items-center justify-center p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-2">
                <label className="text-sm font-medium text-gray-700">Escala:</label>
                <input
                  type="range"
                  min="0.5"
                  max="2"
                  step="0.1"
                  value={scale}
                  onChange={(e) => setScale(Number(e.target.value))}
                  className="w-20"
                />
                <span className="text-sm text-gray-600 w-8">{scale.toFixed(1)}x</span>
              </div>
              
              <div className="flex items-center gap-2">
                <label className="text-sm font-medium text-gray-700">Rotar:</label>
                <input
                  type="range"
                  min="-180"
                  max="180"
                  step="1"
                  value={rotate}
                  onChange={(e) => setRotate(Number(e.target.value))}
                  className="w-20"
                />
                <span className="text-sm text-gray-600 w-12">{rotate}°</span>
              </div>

              <div className="flex items-center gap-2">
                <label className="text-sm font-medium text-gray-700">Aspecto:</label>
                <select
                  value={aspect || ''}
                  onChange={(e) => setAspect(e.target.value ? Number(e.target.value) : undefined)}
                  className="px-2 py-1 border border-gray-300 rounded text-sm"
                >
                  <option value="">Libre</option>
                  <option value={16/9}>16:9</option>
                  <option value={4/3}>4:3</option>
                  <option value={1}>1:1</option>
                  <option value={3/4}>3:4</option>
                </select>
              </div>

              <Button
                onClick={resetCrop}
                variant="outline"
                size="sm"
                className="flex items-center gap-1"
              >
                <RotateCcw className="w-4 h-4" />
                Reset
              </Button>
            </div>

            {/* Image Crop Area */}
            <div className="flex justify-center">
              <ReactCrop
                crop={crop}
                onChange={(_, percentCrop) => setCrop(percentCrop)}
                onComplete={(c) => setCompletedCrop(c)}
                aspect={aspect}
                className="max-w-full max-h-96"
              >
                <img
                  ref={imgRef}
                  alt="Crop me"
                  src={imageSrc}
                  style={{
                    transform: `scale(${scale}) rotate(${rotate}deg)`,
                    maxHeight: '400px',
                    maxWidth: '100%'
                  }}
                  onLoad={onImageLoad}
                />
              </ReactCrop>
            </div>

            {/* Preview */}
            {completedCrop && (
              <div className="text-center">
                <h3 className="text-sm font-medium text-gray-700 mb-2">Vista Previa:</h3>
                <canvas
                  ref={previewCanvasRef}
                  className="border border-gray-300 rounded max-w-full max-h-32"
                  style={{
                    maxWidth: '200px',
                    maxHeight: '150px',
                    width: 'auto',
                    height: 'auto'
                  }}
                />
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 p-4 border-t bg-gray-50">
          <Button
            onClick={onClose}
            variant="outline"
          >
            Cancelar
          </Button>
          <Button
            onClick={onDownloadCropClick}
            disabled={!completedCrop}
            className="flex items-center gap-2"
          >
            <CropIcon className="w-4 h-4" />
            Aplicar Recorte
          </Button>
        </div>
      </div>
    </div>
  );
}
