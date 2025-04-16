**【完全版・AIエージェント協業体制版】開発企画書：インテリジェント音楽制作アシスタント「Tokoroten」（仮称）**

**1. エグゼクティブサマリー**

本プロジェクト「Tokoroten」は、音楽クリエイターがオーディオファイルから高品質なMIDIデータや分析情報を効率的に得るための、Webベースのインテリジェント・アシスタントツールを開発するものである。最先端のAI技術（音声分析、音源分離、自動採譜）に加え、先進的な大規模言語モデル（LLM）/マルチモーダルAPI（Google Gemini API等を想定）を活用し、深い音楽的洞察、解釈の言語化、創造的な提案を提供する。開発は、**プロジェクトマネージャー/プロダクトオーナー（PM/PO）であるあなた、プロダクト管理AIエージェント『Cursor』、そしてコーディングAIエージェント『Devin』という革新的な少数精鋭体制**で行い、AI駆動による高速な開発サイクルと高度な機能実装を目指す。生成されるデータは「完璧な叩き台」として、DAWでの最終仕上げを前提とし、クリエイターの創造性と生産性を飛躍的に向上させることを目的とする。

**2. プロジェクトゴールと目的**

*   **ゴール:** 音楽クリエイターの耳コピ・データ準備・初期アイデア創出ワークフローを革新し、制作時間を大幅に短縮するとともに、創造性を刺激する最高品質のWebアシスタントツールを提供する。
*   **目的:**
    *   オーディオファイルから高精度な楽曲分析情報（キー、テンポ、コード、構造等）を自動抽出する。
    *   最先端AI技術を用いて、オーディオファイルを高品質な楽器別ステム音源に分離する。
    *   分離されたステム音源から、各楽器パートの詳細なMIDIデータを高精度に自動採譜する。
    *   Gemini API等を活用し、分析結果に対する音楽理論的解説、感情的効果の推測、編曲上の提案などを自然言語で生成・提示する。
    *   Gemini API等を活用し、高精度な歌詞起こし、翻訳、テーマ・感情分析を行う。
    *   分析情報、ステム音源、MIDIデータ、AIによる解説・提案を同期表示し、Web上でインタラクティブに確認・簡易編集できる環境を提供する。
    *   DAWでの後続作業に最適化された、多様な形式（SMF, ステムWAV, プロジェクト情報, 分析レポート）でデータを出力する。
    *   ユーザーが分析・採譜の精度や詳細度をコントロールできるオプションを提供する。
    *   （将来的には）自然言語による操作指示を可能にするインターフェースを検討する。

**3. ターゲットオーディエンス**

*   音楽プロデューサー、アレンジャー、作曲家
*   DTMユーザー、トラックメイカー
*   カラオケ音源制作者
*   演奏家（練習用マイナスワン音源作成、譜面起こし補助、楽曲分析・理解深化）
*   音楽教育関係者（教材作成、楽曲分析指導補助）

**4. キーフィーチャー（実現可能な最大限の機能）**

*   **4.1. 高度分析エンジン:**
    *   マルチAIによるキー(転調含む)・テンポ(変動含む)・拍子(変動含む)の高精度推定＆マップ生成
    *   詳細コード進行認識（テンション、オンコード含む）＆ローマ数字表記
    *   楽曲構造（イントロ、サビ等）自動検出＆マーカー生成
    *   ダウンビート/小節線検出
*   **4.2. 最先端音源分離 (Source Separation):**
    *   複数AIモデル利用による高精度分離（ボーカル、ドラム、ベース、ピアノ、ギター、シンセ等、多パート分離）
    *   高音質ステムファイル出力 (WAV/FLAC)
*   **4.3. 高解像度自動採譜 (AMT):**
    *   パート別最適化AMTモデルによる詳細MIDI生成 (SMF Format 1)
        *   **ボーカル:** ピッチベンド、ビブラート情報含む。**Gemini API連携による高精度歌詞認識・同期（.lrc形式互換）と多言語翻訳。**
        *   **ドラム:** 詳細な奏法ニュアンス（ゴーストノート、リムショット等）を含むGM準拠マッピング
        *   **ベース:** 奏法ニュアンス（スライド、ミュート等）を含む高精度採譜
        *   **コード楽器(Piano/Guitar):** ボイシング、アルペジオ、ストローク、奏法ニュアンス抽出
        *   **その他楽器(Synth/Strings等):** メロディ、パッド、シーケンス、モジュレーション情報抽出
*   **4.4. インテリジェント・アナリシス & サジェスチョン (Gemini API活用):**
    *   **音楽的コンテキスト解説:** 分析されたキー、コード進行、構造等について、音楽理論に基づいた解説、機能和声的な役割、使用されているスケール、想定される感情的ムードなどを自然言語で生成。
    *   **スタイル・ジャンル分析レポート:** 表層的なジャンルだけでなく、サブジャンル特徴、リズムパターン、楽器編成、サウンドの特徴などを詳細に分析し、レポートとして提示。
    *   **編曲・構成アイデア提案:** 楽曲構造やコード進行に基づき、バリエーション展開、対旋律のアイデア、リズムパターンの変更案、楽器の追加/変更案などを提案。
    *   **歌詞インサイト:** 抽出/翻訳された歌詞のテーマ、ストーリー、感情的アークなどを分析・要約。
*   **4.5. インタラクティブWebエディタ:**
    *   統合タイムラインビューア（波形、MIDIピアノロール、コード、構造、歌詞同期表示）**＋ AI分析レポート/提案の表示エリア**
    *   高機能MIDIピアノロールエディタ（ノート編集、ベロシティ、ピッチベンド等）
    *   ステム音源ミキサー（Volume/Pan/Mute/Solo）
    *   コード、構造、テンポ/拍子マップの簡易編集機能
    *   高品質Web Audio再生エンジン（簡易GM + α）
    *   **（将来機能）自然言語コマンド入力インターフェース**
*   **4.6. 包括的エクスポート:**
    *   SMF Format 1 (フルMIDIデータ)
    *   分離ステム音源ファイル (WAV/FLAC)
    *   プロジェクト情報ファイル (JSON/XML - テンポ/拍子/キー/コード/構造/歌詞)
    *   個別トラックMIDIファイル
    *   簡易コードシート/リードシート (PDF/Text)
    *   **AI分析レポート (Text/PDF)**
    *   主要DAWプロジェクトファイル生成 (実験的機能)
*   **4.7. ユーザーカスタマイズ:**
    *   採譜詳細度、リズム解釈モード設定
    *   パート別優先度設定

**5. 技術アーキテクチャ**

*   **全体構成:** クライアント(Webブラウザ) - サーバー(API, Web) - 非同期タスクワーカー - AIモデル(特化型) - 外部AI API(LLM/Multimodal) - データストレージ の連携構成。アーキテクチャ自体は従来案を踏襲するが、各コンポーネントの実装はコーディングAIエージェント『Devin』が主導する。
*   **フロントエンド:** SPA。仕様はPM/POが定義し、『Devin』が実装。『Cursor』が仕様の整合性やタスク管理を補助。
*   **バックエンド:**
    *   APIサーバー (Python/FastAPI): 『Devin』が実装。『Cursor』がAPI設計やドキュメンテーション生成を補助。
    *   非同期タスクキューシステム (Celery + Redis/RabbitMQ): 『Devin』が実装・設定。
    *   ワーカープロセス (Python): 『Devin』が実装。特化AIモデルのロード・実行、外部LLM API連携処理を含む。
*   **AIモデル (特化型):** PM/POが選定・評価の指針を与え、『Cursor』が情報収集・比較を行い、『Devin』がインテグレーションを実装。
*   **外部AI API (LLM/Multimodal):** Gemini API, OpenAI API等。PM/POが活用方針を決定し、『Cursor』が最適なAPIコールやプロンプト設計を支援、『Devin』が連携部分を実装。
*   **データストア:** DB設計はPM/POが要件定義し、『Cursor』がスキーマ案を生成、『Devin』が実装。ファイルストレージ設定は『Devin』が担当。

```mermaid
graph LR
    subgraph "User Device"
        Browser[Web Browser (User)]
    end

    subgraph "Cloud Infrastructure / Server Side (Managed by Devin & Cursor)"
        LB[Load Balancer]

        subgraph "Frontend Serving"
            WebServerFE[Web Server (Nginx)] --> FE[Frontend App (React/Vue) - Coded by Devin]
        end

        subgraph "Backend Services"
            APIGW[API Gateway (Optional)] --> API[Backend API (Python/FastAPI) - Coded by Devin]
            API --> TaskQueue[Task Queue (Celery + Redis/RabbitMQ) - Set up by Devin]
            API --> DB[Database (PostgreSQL) - Schema by Cursor, Implemented by Devin]
            API --> Cache[Cache (Redis) - Set up by Devin]

            subgraph "Async Workers (Implemented by Devin)"
                Worker1[Worker Process 1 (Analysis)] -- Job --> AI_Analysis[Audio Analysis Libs/Models - Integrated by Devin]
                Worker2[Worker Process 2 (Separation)] -- Job --> AI_Sep[Source Separation Models - Integrated by Devin]
                Worker3[Worker Process 3 (Transcription)] -- Job --> AI_AMT[AMT Models - Integrated by Devin]
                Worker4[Worker Process 4 (MIDI Gen)] -- Job --> MIDI_Gen[MIDI Struct/Gen Libs - Integrated by Devin]
                Worker5[Worker Process 5 (LLM Tasks)] -- Job --> ExternalAI[External LLM/Multimodal API (Gemini, OpenAI) - Integrated by Devin]

                TaskQueue --> Worker1 & Worker2 & Worker3 & Worker4 & Worker5

                Worker1 & Worker2 & Worker3 & Worker4 & Worker5 --> DB(Update Status/Results)
                Worker1 & Worker2 & Worker3 & Worker4 --> FileStorage[File Storage (S3/GCS/Local) - Set up by Devin]
                Worker5 -- AI Report/Insights --> DB/FileStorage
            end
        end
    end

    Browser -- HTTPS --> LB
    LB --> WebServerFE
    LB -- API Requests --> APIGW

    FE -- API Calls --> APIGW

    Browser -- Download Files/Reports --> FileStorage(via Signed URL etc.)

    %% External API Flow %%
    ExternalAI -- API Request/Response --> Internet[Internet]

    %% Management Flow %%
    PM_PO[You (PM/PO)] -- Instructions/Goals --> Cursor[Product Mgmt AI Agent 'Cursor']
    PM_PO -- Technical Direction --> Devin[Coding AI Agent 'Devin']
    Cursor -- Tasks/Specs --> Devin
    Cursor -- Reports/Status --> PM_PO
    Devin -- Code/Progress/Issues --> PM_PO
    Devin -- Code/Progress --> Cursor
```
*図の変更点: 各コンポーネントの実装・管理主体をAIエージェントとし、PM/POとAI間の指示・報告フローを追加。*

**6. テクノロジースタック**

*   **フロントエンド:**
    *   言語: **TypeScript**
    *   フレームワーク/ライブラリ: **React** or **Vue.js** (PM/PO指示 or Devin推奨)
    *   UIライブラリ: （PM/PO指示 or Devin/Cursor推奨に基づきDevinが実装）
    *   状態管理: （Devinが選択・実装）
    *   音声処理/再生: **Web Audio API**, WaveSurfer.js, Tone.js (Devinが実装)
    *   API通信: Axios or Fetch API (Devinが実装)
    *   ビルドツール: Vite or Webpack (Devinが設定)
*   **バックエンド:**
    *   言語: **Python 3.10+**
    *   フレームワーク: **FastAPI** (Devinが実装)
    *   タスクキュー: **Celery** (Devinが実装・設定)
    *   メッセージブローカー: **Redis** or RabbitMQ (Devinが実装・設定)
    *   データベース: **PostgreSQL** (Devinが実装)
    *   キャッシュ: **Redis** (Devinが実装・設定)
    *   ORM: SQLAlchemy (Devinが実装)
    *   データ検証/シリアライズ: Pydantic (Devinが実装)
    *   音声処理ライブラリ: **Librosa**, Pydub, SoundFile (Devinが利用・実装)
    *   MIDI処理ライブラリ: **Mido**, **PrettyMIDI** (Devinが利用・実装)
    *   AI/ML ライブラリ (特化モデル用): **PyTorch**, **TensorFlow** (Devinがインテグレーション)
    *   **外部AI APIクライアント:** **Google AI Python SDK (for Gemini)**, **OpenAI Python Library** (Devinが連携実装)
*   **インフラストラクチャ:**
    *   コンテナ化: **Docker**, Docker Compose (DevinがDockerfile, Composeファイル作成)
    *   Webサーバー: **Nginx** (Devinが設定ファイル生成)
    *   Appサーバー (Python): **Uvicorn** + Gunicorn (Devinが設定)
    *   クラウドプロバイダー: **AWS**, GCP, or Azure (PM/POが選定、DevinがIaCツール(Terraform等)を用いて構築・設定)
    *   各種マネージドサービス (DB, Cache, Storage, GPU等): Devinが設定・連携
    *   CI/CD: GitHub Actions, GitLab CI等 (Devinがパイプライン設定)

**7. ディレクトリ構成（例）**

(前回の構成案を踏襲するが、ファイル生成・管理は『Devin』が行う)

```
Tokoroten-project/
├── client/         # フロントエンド (Devinが生成・管理)
│   ├── ...
│
├── server/         # バックエンド (Devinが生成・管理)
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── crud/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/ # llm_service.py 含む
│   │   ├── tasks/    # ai_analysis_reporting.py 含む
│   │   ├── utils/
│   │   ├── main.py
│   │   └── celery_app.py
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── ai_models/      # (PM/POが指定、Devinが配置 or 外部参照)
├── docker-compose.yml # (Devinが生成・管理)
├── .github/workflows/ # CI/CDパイプライン (Devinが生成)
├── terraform/        # IaCコード (Devinが生成)
├── .gitignore         # (Devinが生成・管理)
└── README.md          # (Cursorが草案生成、PM/POが監修、Devinが更新)
```

**8. 開発プロセスと方法論**

*   **方法論:** **AI駆動型アジャイル開発**。PM/POがプロダクトバックログを管理し、スプリントゴールを設定。『Cursor』がゴールに基づきタスクをブレークダウンし、優先順位付けを支援。『Devin』がタスクを受け取り、コーディング、テスト、デプロイメントを実行。PM/POは定期的に進捗を確認し、AIエージェントの成果物をレビュー・承認する。
*   **コミュニケーション:** PM/POからAIエージェントへの指示は、明確かつ具体的である必要がある（プロンプトエンジニアリングが重要）。『Cursor』が進捗レポートや潜在的な問題をPM/POに報告。『Devin』は実行ログや生成コード、テスト結果を提示。
*   **プロトタイピングとレビュー:** 『Devin』が迅速にプロトタイプを生成。PM/POが動作確認とフィードバックを行い、イテレーションを回す。UI/UXデザインは、PM/POがFigma等のツールで作成したワイヤーフレームやモックアップを『Devin』に読み込ませて実装させるか、『Devin』自身の提案能力に期待する。
*   **テスト戦略:**
    *   **ユニット/インテグレーションテスト:** 『Devin』がコード生成と同時にテストコードも生成。カバレッジ目標を設定。
    *   **E2Eテスト:** 『Devin』がテストシナリオに基づき自動テストを実装・実行。
    *   **AIモデル評価:** PM/POが評価基準を設定し、『Cursor』が評価プロセスを管理、『Devin』が評価を実行、PM/POが最終判断。
    *   **QA/受入テスト:** PM/POが最終的な品質保証と受入テストを行う責任を持つ。
*   **CI/CD:** 『Devin』がCI/CDパイプラインを構築・保守。コード変更時に自動テスト、ビルド、デプロイを実行。

**9. チーム構成（改訂版）**

*   **プロジェクトマネージャー / プロダクトオーナー (PM/PO):** **あなた**
    *   役割: プロダクトビジョンと戦略の策定、要求定義、優先順位付け、ロードマップ管理、AIエージェントへの指示・目標設定、成果物のレビュー・承認、最終的な品質保証、ステークホルダー（ユーザー等）とのコミュニケーション。デザインやQAに関する最終判断も担う。
*   **プロダクト管理AIエージェント: 『Cursor』（仮称 - 高度な管理・分析能力を想定）**
    *   役割: PM/POの指示に基づき、タスクのブレークダウン、依存関係の管理、進捗状況の追跡・報告、ドキュメンテーション（仕様書、README草案等）生成支援、リスク・課題の早期発見と報告、市場・技術動向の情報収集・分析、最適な技術・ライブラリの提案、プロンプト設計支援。
*   **コーディングAIエージェント: 『Devin』（仮称 - 高度な自律開発能力を想定）**
    *   役割: PM/POおよび『Cursor』からのタスク指示に基づき、フロントエンド・バックエンドのコーディング、テストコード生成・実行、インフラ構築(IaC)、CI/CDパイプライン設定、デプロイメント、バグ修正、リファクタリング、ライブラリ/モデルのインテグレーション、簡単なUI実装（指示があれば）、実行ログや成果物の報告。

**10. リスクと対策**

*   **AI精度限界:**
    *   リスク: 特化AIモデル(分離/採譜)およびLLMの能力限界により、期待通りの精度・品質が得られない。
    *   対策: PM/POによる厳密な評価とフィードバックループ。必要に応じてモデル変更やファインチューニングを『Devin』に指示。ユーザー編集機能の重要性を認識。
*   **AIエージェントの能力限界とブラックボックス化:**
    *   リスク: 『Cursor』『Devin』が特定のタスク（複雑なUI/UXデザイン、高度なセキュリティ対策、未知の問題解決）に対応できない、またはその判断プロセスが不透明。
    *   対策: PM/POによる綿密な指示と期待値調整。AIの判断根拠の説明を『Cursor』『Devin』に要求。重要な部分はPM/POがコードや設定を直接レビュー。限界が見えた場合は外部専門家の利用も検討。
*   **指示（プロンプト）の品質依存:**
    *   リスク: PM/POからAIへの指示が曖昧または不適切だと、意図しない成果物や手戻りが発生。
    *   対策: 指示の明確化・構造化。『Cursor』による指示内容の解釈・確認支援。段階的な指示と確認。
*   **AIエージェントへの過度な依存と単一障害点:**
    *   リスク: AIエージェントの不具合、API停止、性能劣化がプロジェクト全体を停止させる。
    *   対策: 定期的なバックアップとバージョン管理。『Cursor』『Devin』以外の代替手段（手動作業、別ツール）も想定。APIプロバイダーのSLA確認とリスク分散（可能なら）。
*   **コスト（計算資源＆API利用料）:**
    *   リスク: AIモデル推論(GPU)と外部LLM API利用コストが想定を超える。
    *   対策: 『Cursor』によるコストモニタリングと最適化提案。『Devin』による効率的なコード・クエリ実装。PM/POによる予算管理と料金プラン設計。
*   **セキュリティと倫理:**
    *   リスク: AIが生成したコードの脆弱性、データプライバシー侵害、著作権問題。
    *   対策: PM/POによるセキュリティ要件定義。『Devin』にセキュリティベストプラクティス遵守を指示。外部セキュリティ診断の実施検討。利用規約での責任範囲明確化。
*   **専門知識の不足（UI/UX, QA, DevOps）:**
    *   リスク: チーム内に専門家がいないため、デザイン品質、テスト網羅性、インフラ安定性に問題が生じる。
    *   対策: PM/POが関連知識を習得し、AIエージェントに具体的な指示を与える。『Cursor』『Devin』の提案能力を活用。重要な局面では外部リソース（フリーランス、コンサル等）の利用を検討。

**11. 将来的な考慮事項**

*   リアルタイム処理、パーソナライズ、楽譜生成、DAWプラグイン、コラボレーション機能、マルチモーダル機能拡張、高度な自然言語インタラクション：(変更なし)
*   **AIエージェントの能力向上への追従:** 『Cursor』『Devin』、および利用する各種AI技術の進化に合わせて、ツールの機能と開発プロセス自体を継続的に改善していく。

**12. 付録**

*   (必要に応じて) 用語集
*   (必要に応じて) 参考技術・論文リスト
*   (必要に応じて) 市場調査・競合分析

---
