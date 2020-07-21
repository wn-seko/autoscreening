import os
import argparse
import glob
import pickle
from xlsx import read_xlsx_to_empty_dataframe, read_xlsx_to_dataframe
from sklearn.decomposition import PCA
from sklearn.linear_model import Ridge

def train(file_dir_path, master_file_path, model_name):
    if model_name is None:
        model_name = 'model'

    file_paths = glob.glob(f'{file_dir_path}/*.xlsx')

    # マスターファイルから列生成
    df = read_xlsx_to_empty_dataframe(master_file_path, 'シート1', skip_rows=2)

    # ファイルを読み込んでデータフレームに変換
    for file_path in file_paths:
        df = df.append(read_xlsx_to_dataframe(file_path, 'シート1', score_sheet_name='シート2', skip_rows=2))

    # スコアデータ分離
    scores = df['score']
    del df['score']

    # 主成分分析
    pca = PCA(n_components=5) # TODO: パラメータチューニング
    pca.fit(df)
    pca_result = pca.transform(df)

    # リッジ回帰
    clf = Ridge(alpha=1.0) # TODO: パラメータチューニング
    clf.fit(pca_result, scores)
    Ridge()

    # モデルを保存
    os.mkdir(f'./models/{model_name}')

    with open(f'./models/{model_name}/pca.pickle', 'wb') as picklefile:
        pickle.dump(pca, picklefile)

    with open(f'./models/{model_name}/clf.pickle', 'wb') as picklefile:
        pickle.dump(clf, picklefile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='既存のスキルシートを元にモデルを作成します')
    parser.add_argument('directory', help='スキルシートが入ったディレクトリ')
    parser.add_argument('master_file_path', help='フォーマットを決めるマスターファイル')
    parser.add_argument('-m', '--model_name', help="保存するモデル名")
    args = parser.parse_args()

    train(args.directory, args.master_file_path, args.model_name)
