import React, { useState } from 'react';
import Header from './components/Header';
import AudioUploader from './components/AudioUploader';
import AudioPlayer from './components/AudioPlayer';
import AnalysisResults from './components/AnalysisResults';

const App: React.FC = () => {
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [analysisResults, setAnalysisResults] = useState<any>(null);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);

  const handleFileUpload = (file: File) => {
    setAudioFile(file);
    setAnalysisResults(null);
  };

  const handleAnalyze = async () => {
    if (!audioFile) return;

    setIsAnalyzing(true);
    
    setTimeout(() => {
      setAnalysisResults({
        key: 'C Major',
        tempo: 120,
        timeSignature: '4/4',
        instruments: ['Piano', 'Guitar', 'Drums'],
        sections: [
          { name: 'Intro', start: 0, end: 15 },
          { name: 'Verse', start: 15, end: 45 },
          { name: 'Chorus', start: 45, end: 75 }
        ]
      });
      setIsAnalyzing(false);
    }, 2000);
  };

  return (
    <div className="app-container">
      <Header />
      <main className="main-content">
        <AudioUploader onFileUpload={handleFileUpload} />
        {audioFile && (
          <>
            <AudioPlayer audioFile={audioFile} />
            <button 
              onClick={handleAnalyze} 
              disabled={isAnalyzing}
              className="analyze-button"
            >
              {isAnalyzing ? '分析中...' : '音楽を分析する'}
            </button>
          </>
        )}
        {analysisResults && <AnalysisResults results={analysisResults} />}
      </main>
    </div>
  );
};

export default App;
