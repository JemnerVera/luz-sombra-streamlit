import React from 'react';
import { Button } from './ui/button';
import { Upload, History, BarChart3, Eye } from 'lucide-react';

interface SidebarProps {
  activeTab: 'analizar' | 'historial' | 'probar';
  onTabChange: (tab: 'analizar' | 'historial' | 'probar') => void;
}

export function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  return (
    <div className="w-64 bg-card border-r border-border h-screen fixed left-0 top-0 p-6">
      <div className="space-y-6">
        {/* Logo/Title */}
        <div className="text-center">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            Análisis Luz-Sombra
          </h1>
        </div>

        {/* Navigation */}
        <nav className="space-y-2">
          <Button
            variant={activeTab === 'analizar' ? 'default' : 'ghost'}
            className="w-full justify-start gap-3 h-12"
            onClick={() => onTabChange('analizar')}
          >
            <Upload className="h-5 w-5" />
            Analizar Imágenes
          </Button>
          
          <Button
            variant={activeTab === 'historial' ? 'default' : 'ghost'}
            className="w-full justify-start gap-3 h-12"
            onClick={() => onTabChange('historial')}
          >
            <History className="h-5 w-5" />
            Historial
          </Button>
          
          <Button
            variant={activeTab === 'probar' ? 'default' : 'ghost'}
            className="w-full justify-start gap-3 h-12"
            onClick={() => onTabChange('probar')}
          >
            <Eye className="h-5 w-5" />
            Probar Modelo
          </Button>
        </nav>

        {/* Stats */}
        <div className="pt-6 border-t border-border">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <BarChart3 className="h-4 w-4" />
            <span>Sistema Activo</span>
          </div>
        </div>
      </div>
    </div>
  );
}
