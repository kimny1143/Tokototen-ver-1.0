import React, { useEffect, useRef, useState } from 'react';

interface AudioPlayerProps {
  audioFile: File;
}

const AudioPlayer: React.FC<AudioPlayerProps> = ({ audioFile }) => {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [audioUrl, setAudioUrl] = useState<string>('');
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [currentTime, setCurrentTime] = useState<number>(0);
  const [duration, setDuration] = useState<number>(0);

  useEffect(() => {
    const url = URL.createObjectURL(audioFile);
    setAudioUrl(url);

    return () => {
      URL.revokeObjectURL(url);
    };
  }, [audioFile]);

  const handlePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
    }
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTime = parseFloat(e.target.value);
    setCurrentTime(newTime);
    if (audioRef.current) {
      audioRef.current.currentTime = newTime;
    }
  };

  const formatTime = (time: number): string => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  };

  return (
    <div style={styles.container}>
      <div style={styles.fileInfo}>
        <h3 style={styles.fileName}>{audioFile.name}</h3>
        <p style={styles.fileSize}>{(audioFile.size / (1024 * 1024)).toFixed(2)} MB</p>
      </div>
      
      <div style={styles.controls}>
        <button 
          onClick={handlePlayPause} 
          style={styles.playButton}
        >
          {isPlaying ? '⏸️' : '▶️'}
        </button>
        
        <div style={styles.timeControls}>
          <span style={styles.timeDisplay}>{formatTime(currentTime)}</span>
          <input
            type="range"
            min="0"
            max={duration || 0}
            value={currentTime}
            onChange={handleSeek}
            style={styles.seekBar}
          />
          <span style={styles.timeDisplay}>{formatTime(duration)}</span>
        </div>
      </div>
      
      <audio
        ref={audioRef}
        src={audioUrl}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        onEnded={() => setIsPlaying(false)}
        style={{ display: 'none' }}
      />
    </div>
  );
};

const styles = {
  container: {
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '20px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
  },
  fileInfo: {
    marginBottom: '15px',
  },
  fileName: {
    fontSize: '18px',
    fontWeight: 500,
    marginBottom: '5px',
    color: 'var(--text-color)',
  },
  fileSize: {
    fontSize: '14px',
    color: '#666',
  },
  controls: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
  },
  playButton: {
    backgroundColor: 'var(--primary-color)',
    color: 'white',
    border: 'none',
    borderRadius: '50%',
    width: '40px',
    height: '40px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
    fontSize: '18px',
  },
  timeControls: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    flex: 1,
  },
  timeDisplay: {
    fontSize: '14px',
    color: '#666',
    width: '40px',
  },
  seekBar: {
    flex: 1,
    height: '5px',
    accentColor: 'var(--primary-color)',
  },
};

export default AudioPlayer;
