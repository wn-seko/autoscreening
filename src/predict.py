import os
import argparse
import glob
import pickle
from score import number_to_score
from xlsx import read_xlsx_to_dataframe, write_score_to_xlsx

def predict_core(file_path, model_name, index=0):
    # ファイルを読み込んでデータフレームに変換
    df = read_xlsx_to_dataframe(file_path, 'シート1', skip_rows=1)

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
    write_score_to_xlsx(file_path, 'シート3', index, model_name, score)

    # 結果出力
    print(f'{model_name}: {score}')

def predict_all(file_path):
    model_names = os.listdir('./models')

    for index, model_name in enumerate(model_names):
        predict_core(file_path, model_name, index)

def predict_file(file_path, model_name = None):
    if args.model_name is None:
        predict_all(file_path)
    else:
        predict_core(file_path, args.model_name)

def predict_dir(file_dir_path, model_name = None):
    file_paths = glob.glob(f'{file_dir_path}/*.xlsx')

    for file_path in file_paths:
        print(f'process: {file_path}')
        predict_file(file_path, model_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='スキルシートを自動評価します')
    parser.add_argument('path', help='スキルシート')
    parser.add_argument('-m', '--model_name', help="使用するモデル名")
    args = parser.parse_args()

    if os.path.isdir(args.path):
        predict_dir(args.path, args.model_name)
    else:
        predict_file(args.path, args.model_name)
