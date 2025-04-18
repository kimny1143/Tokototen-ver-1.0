# Tokoroten - インテリジェント音楽制作アシスタント

![Tokoroten Logo](./assets/logo.png) *(ロゴは開発段階で追加予定)*

## 📝 概要

Tokoroten（ところてん）は、音楽クリエイターのためのWebベースのインテリジェント・アシスタントツールです。最先端のAI技術を活用し、オーディオファイルから高品質なMIDIデータや詳細な音楽分析情報を効率的に抽出することができます。耳コピ・データ準備・初期アイデア創出プロセスを革新し、制作時間を大幅に短縮しながら創造性を刺激します。

## ✨ 主要機能

### 🔍 高度分析エンジン
- キー（調）・テンポ・拍子の高精度推定（転調・変動含む）
- 詳細コード進行認識（テンション、オンコード含む）
- 楽曲構造（イントロ、サビ等）自動検出
- ダウンビート/小節線検出

### 🎵 最先端音源分離
- 複数AIモデル連携による高精度分離
- ボーカル、ドラム、ベース、ピアノ、ギター、シンセなど多彩な楽器パート分離
- 高音質ステムファイル出力 (WAV/FLAC)

### 🎹 高解像度自動採譜
- パート別に最適化されたAMTモデルによる詳細MIDI生成
- ボーカル：ピッチベンド、ビブラート情報、歌詞認識・同期
- ドラム：詳細な奏法ニュアンス（ゴーストノート、リムショット等）
- ベース：スライド、ミュートなどの奏法ニュアンス
- コード楽器：ボイシング、アルペジオ、ストローク
- その他楽器：メロディ、パッド、シーケンス情報

### 🧠 インテリジェント分析＆サジェスチョン
- 音楽理論に基づいた解説と感情的ムード分析
- スタイル・ジャンル分析レポート
- 編曲・構成アイデア提案
- 歌詞のテーマ・ストーリー分析

### 🖥️ インタラクティブWebエディタ
- 統合タイムラインビューア
- MIDIピアノロールエディタ
- ステム音源ミキサー
- 高品質Web Audio再生エンジン

### 📤 包括的エクスポート
- SMF Format 1（フルMIDIデータ）
- 分離ステム音源ファイル (WAV/FLAC)
- プロジェクト情報ファイル (JSON/XML)
- 簡易コードシート/リードシート
- AI分析レポート
- 主要DAWプロジェクトファイル生成（実験的機能）

## 🛠️ 技術スタック

### フロントエンド
- TypeScript
- React/Vue.js
- Web Audio API
- WaveSurfer.js, Tone.js

### バックエンド
- Python 3.10+
- FastAPI
- Celery + Redis/RabbitMQ
- PostgreSQL
- Librosa, Pydub, SoundFile
- Mido, PrettyMIDI
- PyTorch, TensorFlow, Transformers
- MT3 (MIDI-Text-to-Text Transformer)
- Demucs (音源分離)
- Google AI Python SDK (Gemini), OpenAI Python Library

### インフラストラクチャ
- Docker, Docker Compose
- Nginx, Uvicorn + Gunicorn
- AWS/GCP/Azure (予定)

## 📋 前提条件

- Node.js 18.x以上
- Python 3.10以上
- Docker, Docker Compose
- GPU 推奨 (A10G / RTX4090) CPU 時は 4‑5× 遅延
- MT3モデル: 約1GB（初回ダウンロード時）
- （その他必要に応じて追加予定）

## 🚀 クイックスタート

### 開発環境のセットアップ

```bash
# リポジトリのクローン
git clone https://github.com/your-organization/tokoroten.git
cd tokoroten

# 開発環境の起動
docker-compose up -d
```

### 利用方法

1. ブラウザで `http://localhost:3000` にアクセス
2. オーディオファイルをアップロード
3. 分析・処理オプションを選択
4. 処理完了後、Web上でMIDIや分析結果を確認・編集
5. 必要なデータをエクスポート

## 🧑‍💻 開発ガイド

### プロジェクト構造

```
Tokoroten-project/
├── client/         # フロントエンド
├── server/         # バックエンド
├── ai_models/      # AIモデル
├── docker-compose.yml
├── .github/workflows/ # CI/CDパイプライン
├── terraform/      # IaC
└── README.md       # このファイル
```

### 開発ワークフロー

本プロジェクトはAI駆動型アジャイル開発を採用しています：

1. PM/POがプロダクトバックログ管理とスプリントゴール設定
2. プロダクト管理AIエージェント『Cursor』がタスクのブレークダウンと優先順位付け
3. コーディングAIエージェント『Devin』がタスクの実装
4. PM/POが成果物のレビューと承認

## 👨‍👩‍👧‍👦 チーム構成

- **PM/PO**: プロダクトビジョン策定、要求定義、品質保証
- **Cursor**: タスク管理、ドキュメンテーション、情報分析
- **Devin**: コーディング、テスト、インフラ構築、デプロイ

## 🔮 ロードマップ

- **v0.1**: 基本的な分析エンジンとWebインターフェース
- **v0.2**: 音源分離と基本的な自動採譜機能
- **v0.3**: LLM連携によるインテリジェント分析
- **v0.4**: インタラクティブエディタの強化
- **v0.5**: 包括的エクスポート機能
- **v1.0**: 全機能統合と最適化

## 📜 ライセンス

[MIT License](LICENSE) (または適切なライセンスを選択)

## 🙏 謝辞

- [MT3 (MIDI-Text-to-Text Transformer)](https://github.com/magenta/mt3) - Apache-2.0 ライセンス
- [Demucs](https://github.com/facebookresearch/demucs) - MIT ライセンス

## 📞 連絡先

- GitHub Issues: プロジェクトのIssueページで質問・提案を受け付けています
- Email: [your-email@example.com] (適切な連絡先に変更してください)

---

*このプロジェクトは開発中です。機能や仕様は変更される可能性があります。*
