import React, { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { AnalyzeTab } from './components/AnalyzeTab';
import { HistoryTab } from './components/HistoryTab';
import { ModelTest } from './components/ModelTest';
import { Modal } from './components/ui/modal';
import { Button } from './components/ui/button';

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
  const [showTabChangeModal, setShowTabChangeModal] = useState(false);
  const [pendingTab, setPendingTab] = useState<'analizar' | 'historial' | 'probar' | null>(null);
  const [hasUnsavedData, setHasUnsavedData] = useState(false);

  const handleAnalysisComplete = (result: AnalysisResult) => {
    setAnalysisResults((prev) => [...prev, result]);
    setHasUnsavedData(false); // Los datos se han guardado
  };

  const handleTabChange = (newTab: 'analizar' | 'historial' | 'probar') => {
    // Si hay datos sin guardar y estamos en la pestaña de analizar
    if (hasUnsavedData && activeTab === 'analizar') {
      setPendingTab(newTab);
      setShowTabChangeModal(true);
    } else {
      setActiveTab(newTab);
    }
  };

  const confirmTabChange = () => {
    if (pendingTab) {
      setActiveTab(pendingTab);
      setHasUnsavedData(false);
    }
    setShowTabChangeModal(false);
    setPendingTab(null);
  };

  const cancelTabChange = () => {
    setShowTabChangeModal(false);
    setPendingTab(null);
  };

  const handleDataChange = () => {
    setHasUnsavedData(true);
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
  }, [activeTab, historial.length]);

  return (
    <div className="min-h-screen bg-background flex">
      {/* Sidebar */}
      <Sidebar activeTab={activeTab} onTabChange={handleTabChange} />
      
      {/* Main Content */}
      <div className="flex-1 ml-64 p-8">
        <div className="max-w-6xl mx-auto">
          {activeTab === 'analizar' ? (
            <AnalyzeTab 
              analysisResults={analysisResults} 
              onAnalysisComplete={handleAnalysisComplete}
              onDataChange={handleDataChange}
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

      {/* Modal de confirmación de cambio de pestaña */}
      <Modal
        isOpen={showTabChangeModal}
        onClose={cancelTabChange}
        title=""
      >
        <div className="space-y-6">
          <div className="text-center">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-amber-100 mb-4">
              <svg className="h-6 w-6 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <p className="text-sm text-gray-300">
              Tienes información sin guardar en la pestaña "Analizar Imágenes". 
              Si cambias de pestaña, se perderán los datos ingresados.
            </p>
          </div>
          
          <div className="flex justify-center space-x-4">
            <Button 
              onClick={confirmTabChange}
              className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white"
            >
              Aceptar
            </Button>
            <Button 
              onClick={cancelTabChange}
              className="px-6 py-2 bg-red-600 hover:bg-red-700 text-white"
            >
              Cancelar
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}

export default App;
