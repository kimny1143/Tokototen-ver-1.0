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
  };
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ results }) => {
  return (
    <div style={styles.container}>
      <h2 style={styles.title}>分析結果</h2>
      
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
                <span style={styles.sectionTime}>{section.start}s - {section.end}s</span>
              </div>
            );
          })}
        </div>
      </div>
      
      <div style={styles.aiInsights}>
        <h3 style={styles.insightsTitle}>AIによる音楽的洞察</h3>
        <p style={styles.insightsText}>
          この曲はCメジャーキーで、テンポは120 BPMと中程度の速さです。4/4拍子の一般的なポップ構造を持ち、
          イントロ、ヴァース、コーラスの明確な区分があります。ピアノとギターが主要な楽器として使用され、
          ドラムがリズムセクションをサポートしています。コード進行はポップミュージックでよく使われる
          I-V-vi-IVパターンを基本としています。
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
};

export default AnalysisResults;
