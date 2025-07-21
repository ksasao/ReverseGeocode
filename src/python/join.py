import csv

def merge_csv_files():
    """
    mt_town_all.csvとmt_town_pos_all.csvを
    lg_code,machiaza_idをキーとして結合し、merged.csvを作成する
    """
    
    # ファイル名
    town_file = "mt_town_all.csv"
    pos_file = "mt_town_pos_all.csv"
    output_file = "merged.csv"
    
    # 出力ファイルのヘッダ（指定された順序）
    output_header = [
        'lg_code', 'machiaza_id', 'rep_lat', 'rep_lon', 'machiaza_type',
        'pref', 'pref_kana', 'county', 'county_kana', 
        'city', 'city_kana', 'ward', 'ward_kana',
        'oaza_cho', 'oaza_cho_kana', 'chome', 'chome_kana',
        'koaza', 'koaza_kana'
    ]
    
    try:
        # 位置情報ファイル（mt_town_pos_all.csv）を辞書に読み込み
        print(f"位置情報ファイル '{pos_file}' を読み込み中...")
        pos_data = {}
        with open(pos_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row['lg_code'], row['machiaza_id'])
                pos_data[key] = row
        
        print(f"位置情報データ: {len(pos_data):,}件")
        
        # 町字ファイル（mt_town_all.csv）を読み込んで結合処理
        print(f"町字ファイル '{town_file}' を読み込み、結合処理中...")
        merged_count = 0
        skipped_count = 0
        
        with open(town_file, 'r', encoding='utf-8') as town_f, \
             open(output_file, 'w', encoding='utf-8', newline='') as output_f:
            
            town_reader = csv.DictReader(town_f)
            writer = csv.DictWriter(output_f, fieldnames=output_header)
            
            # ヘッダを書き込み
            writer.writeheader()
            
            for town_row in town_reader:
                key = (town_row['lg_code'], town_row['machiaza_id'])
                
                # 位置情報データに対応するキーがあるかチェック
                if key in pos_data:
                    pos_row = pos_data[key]
                    
                    # 結合されたデータを作成
                    merged_row = {
                        'lg_code': town_row['lg_code'],
                        'machiaza_id': town_row['machiaza_id'],
                        'rep_lat': pos_row['rep_lat'],
                        'rep_lon': pos_row['rep_lon'],
                        'machiaza_type': town_row['machiaza_type'],
                        'pref': town_row['pref'],
                        'pref_kana': town_row['pref_kana'],
                        'county': town_row['county'],
                        'county_kana': town_row['county_kana'],
                        'city': town_row['city'],
                        'city_kana': town_row['city_kana'],
                        'ward': town_row['ward'],
                        'ward_kana': town_row['ward_kana'],
                        'oaza_cho': town_row['oaza_cho'],
                        'oaza_cho_kana': town_row['oaza_cho_kana'],
                        'chome': town_row['chome'],
                        'chome_kana': town_row['chome_kana'],
                        'koaza': town_row['koaza'],
                        'koaza_kana': town_row['koaza_kana']
                    }
                    
                    writer.writerow(merged_row)
                    merged_count += 1
                    
                    if merged_count % 10000 == 0:
                        print(f"  処理済み: {merged_count:,}件")
                else:
                    skipped_count += 1
        
        print(f"\n結合完了！")
        print(f"出力ファイル: {output_file}")
        print(f"結合された行数: {merged_count:,}件")
        print(f"スキップされた行数: {skipped_count:,}件")
        
        # 結果の確認
        import os
        file_size = os.path.getsize(output_file)
        print(f"ファイルサイズ: {file_size:,} バイト")
        
    except FileNotFoundError as e:
        print(f"ファイルが見つかりません: {e}")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

def check_merged_file(filename="merged.csv", lines=10):
    """
    結合されたCSVファイルの先頭数行を確認する
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            print(f"\n=== {filename} の先頭{lines}行 ===")
            for i, row in enumerate(reader):
                if i >= lines:
                    break
                if i == 0:
                    print(f"ヘッダ: {','.join(row)}")
                else:
                    # 主要な列のみ表示（見やすくするため）
                    key_data = f"{row[0]},{row[1]} -> lat:{row[2]}, lon:{row[3]}, {row[5]}{row[13]}{row[16]}{row[17]}"
                    print(f"{i:2d}: {key_data}")
    except FileNotFoundError:
        print(f"ファイル '{filename}' が見つかりません。")
    except Exception as e:
        print(f"ファイル確認エラー: {str(e)}")

# メイン実行部分
if __name__ == "__main__":
    merge_csv_files()
    
    # 結果を確認
    print("\n" + "="*60)
    check_merged_file()