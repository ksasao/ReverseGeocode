import zipfile
import os
from pathlib import Path

def extract_and_merge_csv_files():
    """
    mt_town_pos_all.csv.zipから複数のzipファイルを解凍し、
    含まれるCSVファイルをすべて結合してmt_town_pos_all.csvを作成する
    （テキストとして直接結合、各CSVの先頭行（ヘッダ）はスキップ）
    """
    
    # メインのzipファイル名
    main_zip_file = "mt_town_pos_all.csv.zip"
    output_csv_file = "mt_town_pos_all.csv"
    
    # 一時的な解凍ディレクトリ
    temp_dir = "temp_extracted"
    
    try:
        # メインのzipファイルを解凍
        print(f"メインzipファイル '{main_zip_file}' を解凍中...")
        with zipfile.ZipFile(main_zip_file, 'r') as main_zip:
            main_zip.extractall(temp_dir)
        
        # 解凍されたzipファイルのリストを取得（ソート済み）
        zip_files = sorted(list(Path(temp_dir).glob("*.zip")))
        print(f"見つかったzipファイル数: {len(zip_files)}")
        
        # 出力ファイルを開く
        with open(output_csv_file, 'w', encoding='utf-8', newline='') as output_file:
            first_file = True
            total_lines = 0
            
            # 各zipファイルを処理
            for zip_file in zip_files:
                print(f"処理中: {zip_file.name}")
                
                # zipファイルを解凍
                with zipfile.ZipFile(zip_file, 'r') as sub_zip:
                    # zipファイル内のCSVファイルを探す
                    csv_files = [f for f in sub_zip.namelist() if f.endswith('.csv')]
                    
                    for csv_file in csv_files:
                        # CSVファイルを読み込み
                        with sub_zip.open(csv_file) as csv_content:
                            try:
                                # UTF-8で読み込みを試す
                                content = csv_content.read().decode('utf-8')
                            except UnicodeDecodeError:
                                # UTF-8で読めない場合はShift-JISを試す
                                csv_content.seek(0)
                                content = csv_content.read().decode('shift-jis')
                            
                            # 行に分割
                            lines = content.strip().split('\n')
                            
                            if lines:
                                # 最初のファイルの場合はヘッダも含めて書き込み
                                if first_file:
                                    for line in lines:
                                        output_file.write(line + '\n')
                                    total_lines += len(lines)
                                    first_file = False
                                    print(f"  - {csv_file}: {len(lines)}行（ヘッダ含む）を書き込み")
                                else:
                                    # 2番目以降のファイルはヘッダ（先頭行）をスキップ
                                    data_lines = lines[1:]  # 先頭行をスキップ
                                    for line in data_lines:
                                        output_file.write(line + '\n')
                                    total_lines += len(data_lines)
                                    print(f"  - {csv_file}: {len(data_lines)}行（ヘッダスキップ）を書き込み")
        
        print(f"\n結合完了！")
        print(f"出力ファイル: {output_csv_file}")
        print(f"総行数: {total_lines:,}行（ヘッダ含む）")
        
        # ファイルサイズを表示
        file_size = os.path.getsize(output_csv_file)
        print(f"ファイルサイズ: {file_size:,} バイト")
    
    except FileNotFoundError:
        print(f"エラー: '{main_zip_file}' が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
    
    finally:
        # 一時ディレクトリをクリーンアップ
        if os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)
            print(f"\n一時ディレクトリ '{temp_dir}' を削除しました。")

# 先頭の数行を確認する関数（オプション）
def check_output_file(filename="mt_town_pos_all.csv", lines=10):
    """
    出力されたCSVファイルの先頭数行を確認する
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            print(f"\n=== {filename} の先頭{lines}行 ===")
            for i, line in enumerate(f):
                if i >= lines:
                    break
                print(f"{i+1:2d}: {line.rstrip()}")
    except FileNotFoundError:
        print(f"ファイル '{filename}' が見つかりません。")

# メイン実行部分
if __name__ == "__main__":
    extract_and_merge_csv_files()
    
    # 結果を確認（オプション）
    print("\n" + "="*50)
    check_output_file()