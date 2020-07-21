# Auto Screening

- xlsx で記述されたスキルシートを元に自動評価を行う
- 全てのスキルを主成分分析で次元圧縮しリッジ回帰を行う
- ランクは S, A, B, NG に別れる

## 使用方法

### Predict

`python src/predict.py skill.xlsx --model_name=model`

1. ファイルを指定して自動評価を行う
2. 評価結果を標準出力してファイルに書き戻す

### Train

`python src/train.py data master.xlsx --model_name=model`

1. ディレクトリとマスター（フォーマット決定用）を指定して訓練を行う
2. モデルが指定されたディレクトリに格納される

## スキルチェックシート回答方法

### 想定.1

- Google アンケートフォームを使用して結果をスプレッドシートに出力
- スプレッドシートからデータの読み書き
