import React, { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { AnalyzeTab } from './components/AnalyzeTab';
import { HistoryTab } from './components/HistoryTab';
import { ModelTest } from './components/ModelTest';

interface AnalysisResult {
  light_percentage: number;
  shadow_percentage: number;
  processing_time: number;
  filename: string;
  imagen_resultado_url?: string;
  imagen_original_url?: string;
}

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

function App() {
  const [activeTab, setActiveTab] = useState<'analizar' | 'historial' | 'probar'>('analizar');
  const [analysisResults, setAnalysisResults] = useState<AnalysisResult[]>([]);
  const [historial, setHistorial] = useState<HistorialItem[]>([]);
  const [cargandoHistorial, setCargandoHistorial] = useState(false);

  const handleAnalysisComplete = (result: AnalysisResult) => {
    setAnalysisResults((prev) => [...prev, result]);
  };

  const cargarHistorial = async () => {
    setCargandoHistorial(true);
    try {
      const response = await fetch('http://localhost:8000/historial');
      const data = await response.json();
      if (data.success) {
        setHistorial(data.procesamientos);
      }
    } catch (error) {
      console.error('Error cargando historial:', error);
      alert('Error cargando el historial');
    } finally {
      setCargandoHistorial(false);
    }
  };

  // Cargar historial automáticamente cuando se cambia a la pestaña
  React.useEffect(() => {
    if (activeTab === 'historial' && historial.length === 0) {
      cargarHistorial();
    }
  }, [activeTab]);

  return (
    <div className="min-h-screen bg-background flex">
      {/* Sidebar */}
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
      
      {/* Main Content */}
      <div className="flex-1 ml-64 p-8">
        <div className="max-w-6xl mx-auto">
          {activeTab === 'analizar' ? (
            <AnalyzeTab 
              analysisResults={analysisResults} 
              onAnalysisComplete={handleAnalysisComplete} 
            />
          ) : activeTab === 'historial' ? (
            <HistoryTab 
              historial={historial}
              cargandoHistorial={cargandoHistorial}
              onCargarHistorial={cargarHistorial}
            />
          ) : (
            <ModelTest 
              onTestComplete={handleAnalysisComplete}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
