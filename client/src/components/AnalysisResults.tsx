import React from 'react';

interface Section {
  name: string;
  start: number;
  end: number;
}

interface AnalysisResultsProps {
  results: {
    key: string;
    tempo: number;
    timeSignature: string;
    instruments: string[];
    sections: Section[];
    analysisType?: string;
    scale?: string[];
    chordProgression?: string[];
    harmonicAnalysis?: string;
    mixBalance?: string;
    eqRecommendations?: string[];
    dynamicsSuggestions?: string[];
    spatialRecommendations?: string[];
    instrumentation?: string;
    energyFlow?: string;
    genre?: string;
    soundQuality?: string;
    suggestions?: string[];
  };
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ results }) => {
  const renderMusicTheoryAnalysis = () => {
    if (results.analysisType !== 'music_theory' || (!results.scale && !results.chordProgression && !results.harmonicAnalysis)) {
      return null;
    }
    
    return (
      <div style={styles.analysisSection}>
        <h3 style={styles.sectionTitle}>音楽理論分析</h3>
        
        {results.scale && (
          <div style={styles.resultCard}>
            <h3 style={styles.cardTitle}>スケール</h3>
            <ul style={styles.list}>
              {results.scale.map((note, index) => (
                <li key={index} style={styles.listItem}>{note}</li>
              ))}
            </ul>
          </div>
        )}
        
        {results.chordProgression && (
          <div style={styles.resultCard}>
            <h3 style={styles.cardTitle}>コード進行</h3>
            <div style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '10px'
              }}>
              {results.chordProgression.map((chord, index) => (
                <div key={index} style={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  padding: '10px',
                  backgroundColor: '#f0f0f0',
                  borderRadius: '4px',
                  minWidth: '60px'
                }}>
                  <span style={{
                    fontSize: '12px',
                    color: '#666',
                    marginBottom: '4px'
                  }}>{index + 1}</span>
                  <span style={{
                    fontWeight: 600,
                    color: 'var(--text-color)'
                  }}>{chord}</span>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {results.harmonicAnalysis && (
          <div style={styles.resultCard}>
            <h3 style={styles.cardTitle}>和声分析</h3>
            <p style={styles.analysisText}>{results.harmonicAnalysis}</p>
          </div>
        )}
      </div>
    );
  };
  
  const renderProductionAnalysis = () => {
    if (results.analysisType !== 'production_feedback' || 
        (!results.mixBalance && !results.eqRecommendations && 
         !results.dynamicsSuggestions && !results.spatialRecommendations)) {
      return null;
    }
    
    return (
      <div style={styles.analysisSection}>
        <h3 style={styles.sectionTitle}>プロダクション分析</h3>
        
        {results.mixBalance && (
          <div style={styles.resultCard}>
            <h3 style={styles.cardTitle}>ミックスバランス</h3>
            <p style={styles.analysisText}>{results.mixBalance}</p>
          </div>
        )}
        
        {results.eqRecommendations && results.eqRecommendations.length > 0 && (
          <div style={styles.resultCard}>
            <h3 style={styles.cardTitle}>EQレコメンデーション</h3>
            <ul style={styles.list}>
              {results.eqRecommendations.map((rec, index) => (
                <li key={index} style={styles.listItem}>{rec}</li>
              ))}
            </ul>
          </div>
        )}
        
        {results.dynamicsSuggestions && results.dynamicsSuggestions.length > 0 && (
          <div style={styles.resultCard}>
            <h3 style={styles.cardTitle}>ダイナミクス提案</h3>
            <ul style={styles.list}>
              {results.dynamicsSuggestions.map((sug, index) => (
                <li key={index} style={styles.listItem}>{sug}</li>
              ))}
            </ul>
          </div>
        )}
        
        {results.spatialRecommendations && results.spatialRecommendations.length > 0 && (
          <div style={styles.resultCard}>
            <h3 style={styles.cardTitle}>空間処理提案</h3>
            <ul style={styles.list}>
              {results.spatialRecommendations.map((rec, index) => (
                <li key={index} style={styles.listItem}>{rec}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };
  
  const renderArrangementAnalysis = () => {
    if (results.analysisType !== 'arrangement_analysis' || (!results.instrumentation && !results.energyFlow)) {
      return null;
    }
    
    return (
      <div style={styles.analysisSection}>
        <h3 style={styles.sectionTitle}>アレンジメント分析</h3>
        
        {results.instrumentation && (
          <div style={styles.resultCard}>
            <h3 style={styles.cardTitle}>楽器編成</h3>
            <p style={styles.analysisText}>{results.instrumentation}</p>
          </div>
        )}
        
        {results.energyFlow && (
          <div style={styles.resultCard}>
            <h3 style={styles.cardTitle}>エネルギーフロー</h3>
            <p style={styles.analysisText}>{results.energyFlow}</p>
          </div>
        )}
      </div>
    );
  };
  
  const renderSuggestions = () => {
    if (!results.suggestions || results.suggestions.length === 0) {
      return null;
    }
    
    return (
      <div style={styles.suggestionsContainer}>
        <h3 style={styles.sectionTitle}>改善提案</h3>
        <ul style={styles.suggestionsList}>
          {results.suggestions.map((suggestion, index) => (
            <li key={index} style={{
              padding: '8px 0',
              borderBottom: '1px solid #eee',
              color: 'var(--text-color)',
              position: 'relative',
              paddingLeft: '20px'
            }}>{suggestion}</li>
          ))}
        </ul>
      </div>
    );
  };
  
  return (
    <div style={styles.container}>
      <h2 style={styles.title}>
        分析結果
        {results.analysisType && (
          <span style={styles.analysisTypeTag}>
            {results.analysisType === 'music_theory' && '音楽理論'}
            {results.analysisType === 'production_feedback' && 'プロダクション'}
            {results.analysisType === 'arrangement_analysis' && 'アレンジメント'}
            {results.analysisType === 'general' && '一般分析'}
          </span>
        )}
      </h2>
      
      <div style={styles.resultsGrid}>
        <div style={styles.resultCard}>
          <h3 style={styles.cardTitle}>基本情報</h3>
          <div style={styles.infoItem}>
            <span style={styles.label}>キー:</span>
            <span style={styles.value}>{results.key}</span>
          </div>
          <div style={styles.infoItem}>
            <span style={styles.label}>テンポ:</span>
            <span style={styles.value}>{results.tempo} BPM</span>
          </div>
          <div style={styles.infoItem}>
            <span style={styles.label}>拍子:</span>
            <span style={styles.value}>{results.timeSignature}</span>
          </div>
          {results.genre && (
            <div style={styles.infoItem}>
              <span style={styles.label}>ジャンル:</span>
              <span style={styles.value}>{results.genre}</span>
            </div>
          )}
          {results.soundQuality && (
            <div style={styles.infoItem}>
              <span style={styles.label}>音質:</span>
              <span style={styles.value}>{results.soundQuality}</span>
            </div>
          )}
        </div>
        
        <div style={styles.resultCard}>
          <h3 style={styles.cardTitle}>検出された楽器</h3>
          <ul style={styles.instrumentList}>
            {results.instruments.map((instrument, index) => (
              <li key={index} style={styles.instrument}>{instrument}</li>
            ))}
          </ul>
        </div>
      </div>
      
      <div style={styles.sectionsContainer}>
        <h3 style={styles.sectionTitle}>曲の構成</h3>
        <div style={styles.timeline}>
          {results.sections.map((section, index) => {
            const width = `${((section.end - section.start) / results.sections[results.sections.length - 1].end) * 100}%`;
            return (
              <div 
                key={index}
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  alignItems: 'center',
                  padding: '5px',
                  color: 'white',
                  transition: 'all 0.3s',
                  cursor: 'pointer',
                  width,
                  backgroundColor: getSectionColor(index),
                }}
              >
                <span style={styles.sectionName}>{section.name}</span>
                <span style={styles.sectionTime}>{section.start.toFixed(1)}s - {section.end.toFixed(1)}s</span>
              </div>
            );
          })}
        </div>
      </div>
      
      {renderMusicTheoryAnalysis()}
      {renderProductionAnalysis()}
      {renderArrangementAnalysis()}
      {renderSuggestions()}
      
      <div style={styles.aiInsights}>
        <h3 style={styles.insightsTitle}>AIによる音楽的洞察</h3>
        <p style={styles.insightsText}>
          この曲は{results.key}キーで、テンポは{results.tempo} BPMです。{results.timeSignature}拍子の
          {results.sections.map(s => s.name).join('、')}の構成を持っています。
          {results.instruments.length > 0 && `主な楽器として${results.instruments.join('、')}が使用されています。`}
          {results.chordProgression && `コード進行は${results.chordProgression.join(' - ')}です。`}
          {results.harmonicAnalysis && results.harmonicAnalysis}
        </p>
      </div>
    </div>
  );
};

const getSectionColor = (index: number): string => {
  const colors = [
    'rgba(98, 0, 234, 0.7)',
    'rgba(3, 218, 198, 0.7)',
    'rgba(255, 145, 0, 0.7)',
    'rgba(233, 30, 99, 0.7)',
  ];
  return colors[index % colors.length];
};

const styles = {
  container: {
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '25px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
  },
  title: {
    fontSize: '24px',
    fontWeight: 600,
    marginBottom: '20px',
    color: 'var(--primary-color)',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  analysisTypeTag: {
    fontSize: '14px',
    fontWeight: 500,
    padding: '4px 10px',
    borderRadius: '4px',
    backgroundColor: 'var(--primary-color)',
    color: 'white',
  },
  resultsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
    marginBottom: '30px',
  },
  resultCard: {
    backgroundColor: '#f9f9f9',
    borderRadius: '8px',
    padding: '15px',
    marginBottom: '15px',
  },
  cardTitle: {
    fontSize: '18px',
    fontWeight: 500,
    marginBottom: '15px',
    color: 'var(--text-color)',
  },
  infoItem: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '10px',
  },
  label: {
    fontWeight: 500,
    color: '#666',
  },
  value: {
    fontWeight: 600,
    color: 'var(--text-color)',
  },
  instrumentList: {
    listStyleType: 'none',
    padding: 0,
  },
  instrument: {
    padding: '8px 0',
    borderBottom: '1px solid #eee',
    color: 'var(--text-color)',
  },
  sectionsContainer: {
    marginBottom: '30px',
  },
  sectionTitle: {
    fontSize: '18px',
    fontWeight: 500,
    marginBottom: '15px',
    color: 'var(--text-color)',
  },
  timeline: {
    display: 'flex',
    width: '100%',
    height: '60px',
    borderRadius: '4px',
    overflow: 'hidden',
  },
  section: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    padding: '5px',
    color: 'white',
    transition: 'all 0.3s',
    cursor: 'pointer',
  },
  sectionName: {
    fontWeight: 600,
    fontSize: '14px',
  },
  sectionTime: {
    fontSize: '12px',
    opacity: 0.8,
  },
  aiInsights: {
    backgroundColor: '#f0f0f0',
    borderRadius: '8px',
    padding: '20px',
    marginTop: '20px',
  },
  insightsTitle: {
    fontSize: '18px',
    fontWeight: 500,
    marginBottom: '15px',
    color: 'var(--primary-color)',
  },
  insightsText: {
    lineHeight: 1.6,
    color: 'var(--text-color)',
  },
  analysisSection: {
    marginBottom: '30px',
    borderTop: '1px solid #eee',
    paddingTop: '20px',
  },
  list: {
    listStyleType: 'none',
    padding: 0,
  },
  listItem: {
    padding: '8px 0',
    borderBottom: '1px solid #eee',
    color: 'var(--text-color)',
  },
  chordProgression: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '10px',
  },
  chord: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '10px',
    backgroundColor: '#f0f0f0',
    borderRadius: '4px',
    minWidth: '60px',
  },
  chordNumber: {
    fontSize: '12px',
    color: '#666',
    marginBottom: '4px',
  },
  chordName: {
    fontWeight: 600,
    color: 'var(--text-color)',
  },
  analysisText: {
    lineHeight: 1.6,
    color: 'var(--text-color)',
  },
  suggestionsContainer: {
    marginBottom: '30px',
    backgroundColor: '#f9f9f9',
    borderRadius: '8px',
    padding: '15px',
  },
  suggestionsList: {
    listStyleType: 'none',
    padding: 0,
  },
  suggestion: {
    padding: '8px 0',
    borderBottom: '1px solid #eee',
    color: 'var(--text-color)',
    position: 'relative',
    paddingLeft: '20px',
  },
};

export default AnalysisResults;
