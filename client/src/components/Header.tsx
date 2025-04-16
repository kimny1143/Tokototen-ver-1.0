import React from 'react';

const Header: React.FC = () => {
  return (
    <header style={styles.header}>
      <h1 style={styles.title}>Tokoroten</h1>
      <p style={styles.subtitle}>インテリジェント音楽制作アシスタント</p>
    </header>
  );
};

const styles = {
  header: {
    padding: '20px 0',
    borderBottom: '1px solid #e0e0e0',
    marginBottom: '20px',
  },
  title: {
    fontSize: '2.5rem',
    color: 'var(--primary-color)',
    marginBottom: '8px',
  },
  subtitle: {
    fontSize: '1.2rem',
    color: '#666',
  }
};

export default Header;
