import React, { useState, useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { BarChart3, RefreshCw, Download, ChevronLeft, ChevronRight } from 'lucide-react';

interface HistorialItem {
  id: number;
  empresa: string;
  fundo: string;
  sector: string;
  lote: string;
  hilera: string;
  numero_planta: string;
  porcentaje_luz: number;
  porcentaje_sombra: number;
  fecha_tomada: string | null;
  latitud: number | null;
  longitud: number | null;
  timestamp: string;
  imagen_resultado_url?: string;
}

interface HistoryTabProps {
  historial: HistorialItem[];
  cargandoHistorial: boolean;
  onCargarHistorial: () => void;
}

export function HistoryTab({ historial, cargandoHistorial, onCargarHistorial }: HistoryTabProps) {
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  // Calcular datos paginados
  const paginatedData = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    return historial.slice(startIndex, endIndex);
  }, [historial, currentPage]);

  const totalPages = Math.ceil(historial.length / itemsPerPage);

  const exportarHistorial = () => {
    const csvContent = [
      ['ID', 'Empresa', 'Fundo', 'Sector', 'Lote', 'Hilera', 'N° Planta', 'Luz (%)', 'Sombra (%)', 'Fecha Tomada', 'Latitud', 'Longitud', 'Fecha Procesamiento'].join(','),
      ...historial.map(item => [
        item.id,
        `"${item.empresa || ''}"`,
        `"${item.fundo}"`,
        `"${item.sector || ''}"`,
        `"${item.lote || ''}"`,
        `"${item.hilera || ''}"`,
        `"${item.numero_planta || ''}"`,
        item.porcentaje_luz.toFixed(2),
        item.porcentaje_sombra.toFixed(2),
        item.fecha_tomada ? `"${new Date(item.fecha_tomada).toLocaleString()}"` : '""',
        item.latitud || '',
        item.longitud || '',
        `"${new Date(item.timestamp).toLocaleString()}"`
      ].join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `historial_luz_sombra_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center space-y-4">
        <h2 className="text-4xl font-bold text-balance">Historial de Procesamientos</h2>
      </div>

      {/* Actions */}
      <div className="flex justify-center gap-4">
        <Button 
          onClick={onCargarHistorial}
          disabled={cargandoHistorial}
          className="flex items-center gap-2"
        >
          {cargandoHistorial ? (
            <>
              <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
              Cargando...
            </>
          ) : (
            <>
              <RefreshCw className="h-4 w-4" />
              Actualizar Historial
            </>
          )}
        </Button>
        
        {historial.length > 0 && (
          <Button 
            variant="outline"
            onClick={exportarHistorial}
            className="flex items-center gap-2"
          >
            <Download className="h-4 w-4" />
            Exportar CSV
          </Button>
        )}
      </div>

      {/* Historial Table */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Historial
          </CardTitle>
        </CardHeader>
        <CardContent>
          {historial.length === 0 ? (
            <div className="text-center py-12">
              <BarChart3 className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-medium text-muted-foreground mb-2">
                No hay procesamientos guardados
              </h3>
              <p className="text-muted-foreground">
                Sube y analiza imágenes para ver el historial aquí
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-xs">
                        <thead>
                          <tr className="border-b">
                            <th className="text-left py-2 px-2 font-medium w-12">ID</th>
                            <th className="text-left py-2 px-2 font-medium w-20">Empresa</th>
                            <th className="text-left py-2 px-2 font-medium w-24">Fundo</th>
                            <th className="text-left py-2 px-2 font-medium w-16">Sector</th>
                            <th className="text-left py-2 px-2 font-medium w-16">Lote</th>
                            <th className="text-left py-2 px-2 font-medium w-12">Hilera</th>
                            <th className="text-left py-2 px-2 font-medium w-16">N° Planta</th>
                            <th className="text-right py-2 px-2 font-medium w-16">Luz (%)</th>
                            <th className="text-right py-2 px-2 font-medium w-16">Sombra (%)</th>
                            <th className="text-left py-2 px-2 font-medium w-20">Latitud</th>
                            <th className="text-left py-2 px-2 font-medium w-20">Longitud</th>
                            <th className="text-left py-2 px-2 font-medium w-28">Fecha</th>
                          </tr>
                        </thead>
                <tbody>
                  {paginatedData.map((item) => (
                    <tr key={item.id} className="border-b hover:bg-muted/50 transition-colors">
                      <td className="py-2 px-2 font-mono text-xs">{item.id}</td>
                      <td className="py-2 px-2 font-medium text-xs truncate max-w-20" title={item.empresa || 'N/A'}>
                        {item.empresa || 'N/A'}
                      </td>
                      <td className="py-2 px-2 font-medium text-xs truncate max-w-24" title={item.fundo}>
                        {item.fundo}
                      </td>
                      <td className="py-2 px-2 font-medium text-xs truncate max-w-16" title={item.sector || 'N/A'}>
                        {item.sector || 'N/A'}
                      </td>
                      <td className="py-2 px-2 font-medium text-xs truncate max-w-16" title={item.lote || 'N/A'}>
                        {item.lote || 'N/A'}
                      </td>
                      <td className="py-2 px-2 font-medium text-xs text-center">
                        {item.hilera || 'N/A'}
                      </td>
                      <td className="py-2 px-2 font-medium text-xs text-center">
                        {item.numero_planta || 'N/A'}
                      </td>
                      <td className="py-2 px-2 text-right font-medium text-xs text-chart-1">
                        {item.porcentaje_luz.toFixed(1)}%
                      </td>
                      <td className="py-2 px-2 text-right font-medium text-xs text-chart-2">
                        {item.porcentaje_sombra.toFixed(1)}%
                      </td>
                      <td className="py-2 px-2 text-muted-foreground text-xs">
                        {item.latitud ? item.latitud.toFixed(4) : 'N/A'}
                      </td>
                      <td className="py-2 px-2 text-muted-foreground text-xs">
                        {item.longitud ? item.longitud.toFixed(4) : 'N/A'}
                      </td>
                      <td className="py-2 px-2 text-muted-foreground text-xs">
                        {new Date(item.timestamp).toLocaleDateString('es-ES', {
                          day: '2-digit',
                          month: '2-digit',
                          year: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Paginación */}
          {historial.length > itemsPerPage && (
            <div className="flex items-center justify-between mt-6">
              <div className="text-sm text-muted-foreground">
                Mostrando {((currentPage - 1) * itemsPerPage) + 1} a {Math.min(currentPage * itemsPerPage, historial.length)} de {historial.length} resultados
              </div>
              
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                >
                  <ChevronLeft className="h-4 w-4" />
                  Anterior
                </Button>
                
                <div className="flex items-center gap-1">
                  {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => (
                    <Button
                      key={page}
                      variant={currentPage === page ? "default" : "outline"}
                      size="sm"
                      onClick={() => setCurrentPage(page)}
                      className="w-8 h-8 p-0"
                    >
                      {page}
                    </Button>
                  ))}
                </div>
                
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                  disabled={currentPage === totalPages}
                >
                  Siguiente
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
