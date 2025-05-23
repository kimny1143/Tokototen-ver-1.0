import React, { useRef, useState } from 'react';

interface AudioUploaderProps {
  onFileUpload: (file: File) => void;
  isUploading?: boolean;
}

const AudioUploader: React.FC<AudioUploaderProps> = ({ onFileUpload, isUploading = false }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [dragActive, setDragActive] = useState<boolean>(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      onFileUpload(files[0]);
    }
  };

  const handleDrag = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div 
      className={`uploader-container ${dragActive ? 'drag-active' : ''} ${isUploading ? 'uploading' : ''}`}
      onDragEnter={isUploading ? undefined : handleDrag}
      onDragLeave={isUploading ? undefined : handleDrag}
      onDragOver={isUploading ? undefined : handleDrag}
      onDrop={isUploading ? undefined : handleDrop}
      style={{
        border: `2px dashed ${dragActive ? 'var(--primary-color)' : '#ccc'}`,
        borderRadius: '8px',
        padding: '40px',
        textAlign: 'center',
        cursor: isUploading ? 'wait' : 'pointer',
        backgroundColor: dragActive ? 'rgba(98, 0, 234, 0.05)' : 'white',
        transition: 'all 0.3s ease',
        opacity: isUploading ? 0.7 : 1,
        pointerEvents: isUploading ? 'none' : 'auto'
      }}
      onClick={isUploading ? undefined : handleButtonClick}
    >
      <input 
        type="file" 
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="audio/*"
        style={{ display: 'none' }}
        disabled={isUploading}
      />
      <div>
        {isUploading ? (
          <>
            <div style={{ 
              width: '64px', 
              height: '64px', 
              margin: '0 auto 16px',
              border: '4px solid rgba(98, 0, 234, 0.1)',
              borderRadius: '50%',
              borderTop: '4px solid var(--primary-color)',
              animation: 'spin 1s linear infinite'
            }} />
            <style>
              {`
                @keyframes spin {
                  0% { transform: rotate(0deg); }
                  100% { transform: rotate(360deg); }
                }
              `}
            </style>
            <h3 style={{ marginBottom: '8px', color: 'var(--text-color)' }}>
              アップロード中...
            </h3>
            <p style={{ color: '#666' }}>しばらくお待ちください</p>
          </>
        ) : (
          <>
            <svg 
              width="64" 
              height="64" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round"
              style={{ margin: '0 auto 16px', color: 'var(--primary-color)' }}
            >
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17 8 12 3 7 8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            <h3 style={{ marginBottom: '8px', color: 'var(--text-color)' }}>
              音楽ファイルをドラッグ＆ドロップ
            </h3>
            <p style={{ color: '#666' }}>または、クリックしてファイルを選択</p>
          </>
        )}
      </div>
    </div>
  );
};

export default AudioUploader;
