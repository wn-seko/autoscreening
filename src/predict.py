import os
import argparse
import pickle
from score import number_to_score
from xlsx import read_xlsx_to_dataframe, write_score_to_xlsx

def predict(file_path, model_name, index=0):
    # ファイルを読み込んでデータフレームに変換
    df = read_xlsx_to_dataframe(file_path, 'シート1', skip_rows=2)

    # モデル読み込み
    with open(f'./models/{model_name}/pca.pickle', 'rb') as picklefile:
        pca = pickle.load(picklefile)

    with open(f'./models/{model_name}/clf.pickle', 'rb') as picklefile:
        clf = pickle.load(picklefile)

    # 予測
    pca_result = pca.transform(df)
    clf_result = clf.predict(pca_result)
    score = number_to_score(clf_result[0])

    # ファイル書き込み
    write_score_to_xlsx(file_path, 'シート2', index, model_name, score)

    # 結果出力
    print(f'{model_name}: {score}')

def predict_all(file_path):
    model_names = os.listdir('./models')

    for index, model_name in enumerate(model_names):
        predict(file_path, model_name, index)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='スキルシートを自動評価します')
    parser.add_argument('file', help='スキルシート')
    parser.add_argument('-m', '--model_name', help="使用するモデル名")
    args = parser.parse_args()

    if args.model_name is None:
        predict_all(args.file)
    else:
        predict(args.file, args.model_name)
