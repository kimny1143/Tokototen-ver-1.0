import React, { useState } from 'react';
import Header from './components/Header';
import AudioUploader from './components/AudioUploader';
import AudioPlayer from './components/AudioPlayer';
import AnalysisResults from './components/AnalysisResults';
import { audioAPI } from './services/api';

interface UploadedFile {
  file: File;
  fileId: string;
  filename: string;
}

type AnalysisType = 'general' | 'music_theory' | 'production_feedback' | 'arrangement_analysis';

const App: React.FC = () => {
  const [audioFile, setAudioFile] = useState<UploadedFile | null>(null);
  const [analysisResults, setAnalysisResults] = useState<any>(null);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedAnalysisType, setSelectedAnalysisType] = useState<AnalysisType>('general');

  const handleFileUpload = async (file: File) => {
    try {
      setIsUploading(true);
      setError(null);
      setAnalysisResults(null);
      
      const response = await audioAPI.uploadAudio(file);
      
      setAudioFile({
        file,
        fileId: response.file_id,
        filename: response.filename
      });
    } catch (err) {
      console.error('Error uploading file:', err);
      setError('ファイルのアップロードに失敗しました。もう一度お試しください。');
    } finally {
      setIsUploading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!audioFile) return;

    try {
      setIsAnalyzing(true);
      setError(null);
      
      let result;
      
      switch (selectedAnalysisType) {
        case 'music_theory':
          result = await audioAPI.analyzeMusicTheory(audioFile.fileId);
          break;
        case 'production_feedback':
          result = await audioAPI.analyzeProduction(audioFile.fileId);
          break;
        case 'arrangement_analysis':
          result = await audioAPI.analyzeArrangement(audioFile.fileId);
          break;
        default:
          result = await audioAPI.analyzeAudio(audioFile.fileId);
      }
      
      const formattedResults = {
        key: result.key,
        tempo: result.tempo,
        timeSignature: result.time_signature,
        instruments: result.instruments || ['Unknown'],
        sections: result.structure ? 
          result.structure.map((section: string, index: number, arr: string[]) => {
            const duration = result.downbeats ? result.downbeats.length * 4 : 120;
            const sectionCount = arr.length;
            const sectionLength = duration / sectionCount;
            const start = index * sectionLength;
            const end = (index + 1) * sectionLength;
            return { name: section, start, end };
          }) : 
          [{ name: 'Full Track', start: 0, end: 120 }],
        analysisType: selectedAnalysisType,
        scale: result.scale,
        chordProgression: result.chord_progression,
        harmonicAnalysis: result.harmonic_analysis,
        mixBalance: result.mix_balance,
        eqRecommendations: result.eq_recommendations,
        dynamicsSuggestions: result.dynamics_suggestions,
        spatialRecommendations: result.spatial_recommendations,
        instrumentation: result.instrumentation,
        energyFlow: result.energy_flow,
        genre: result.genre,
        soundQuality: result.sound_quality,
        suggestions: result.suggestions
      };
      
      setAnalysisResults(formattedResults);
    } catch (err) {
      console.error('Error analyzing audio:', err);
      setError('音楽分析に失敗しました。もう一度お試しください。');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="app-container">
      <Header />
      <main className="main-content">
        {error && (
          <div className="error-message" style={{ 
            backgroundColor: '#ffebee', 
            color: '#c62828', 
            padding: '10px', 
            borderRadius: '4px', 
            marginBottom: '20px' 
          }}>
            {error}
          </div>
        )}
        
        {!audioFile && (
          <AudioUploader 
            onFileUpload={handleFileUpload} 
            isUploading={isUploading} 
          />
        )}
        
        {audioFile && (
          <>
            <div style={{ marginBottom: '20px' }}>
              <h3 style={{ marginBottom: '10px' }}>アップロードされたファイル: {audioFile.filename}</h3>
              <AudioPlayer audioFile={audioFile.file} />
              
              <div style={{ marginTop: '20px', marginBottom: '20px' }}>
                <h3 style={{ marginBottom: '10px' }}>分析タイプを選択:</h3>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <button 
                    onClick={() => setSelectedAnalysisType('general')}
                    className={`analysis-type-button ${selectedAnalysisType === 'general' ? 'selected' : ''}`}
                    style={{
                      padding: '8px 16px',
                      backgroundColor: selectedAnalysisType === 'general' ? 'var(--primary-color)' : '#f0f0f0',
                      color: selectedAnalysisType === 'general' ? 'white' : 'var(--text-color)',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer'
                    }}
                  >
                    一般分析
                  </button>
                  <button 
                    onClick={() => setSelectedAnalysisType('music_theory')}
                    className={`analysis-type-button ${selectedAnalysisType === 'music_theory' ? 'selected' : ''}`}
                    style={{
                      padding: '8px 16px',
                      backgroundColor: selectedAnalysisType === 'music_theory' ? 'var(--primary-color)' : '#f0f0f0',
                      color: selectedAnalysisType === 'music_theory' ? 'white' : 'var(--text-color)',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer'
                    }}
                  >
                    音楽理論
                  </button>
                  <button 
                    onClick={() => setSelectedAnalysisType('production_feedback')}
                    className={`analysis-type-button ${selectedAnalysisType === 'production_feedback' ? 'selected' : ''}`}
                    style={{
                      padding: '8px 16px',
                      backgroundColor: selectedAnalysisType === 'production_feedback' ? 'var(--primary-color)' : '#f0f0f0',
                      color: selectedAnalysisType === 'production_feedback' ? 'white' : 'var(--text-color)',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer'
                    }}
                  >
                    プロダクション
                  </button>
                  <button 
                    onClick={() => setSelectedAnalysisType('arrangement_analysis')}
                    className={`analysis-type-button ${selectedAnalysisType === 'arrangement_analysis' ? 'selected' : ''}`}
                    style={{
                      padding: '8px 16px',
                      backgroundColor: selectedAnalysisType === 'arrangement_analysis' ? 'var(--primary-color)' : '#f0f0f0',
                      color: selectedAnalysisType === 'arrangement_analysis' ? 'white' : 'var(--text-color)',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer'
                    }}
                  >
                    アレンジメント
                  </button>
                </div>
              </div>
              
              <button 
                onClick={handleAnalyze} 
                disabled={isAnalyzing}
                className="analyze-button"
                style={{
                  padding: '12px 24px',
                  backgroundColor: 'var(--primary-color)',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  fontSize: '16px',
                  cursor: isAnalyzing ? 'not-allowed' : 'pointer',
                  opacity: isAnalyzing ? 0.7 : 1
                }}
              >
                {isAnalyzing ? '分析中...' : '音楽を分析する'}
              </button>
            </div>
          </>
        )}
        
        {analysisResults && <AnalysisResults results={analysisResults} />}
      </main>
    </div>
  );
};

export default App;
