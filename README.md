# ReverseGeocode
クリックした場所の緯度経度から住所を調べます(逆ジオコーディング)。住所を調べる処理はプラウザのJavaScriptのみで行っており、サーバ上で処理は行っていません。なお、クリックした地点に最も近い代表点の住所を返すため、実際の住所と異なる場合があります。

## 利用データについて
デジタル庁の
- [レジストリカタログの 日本 町字マスター データセット mt_town_all.csv](https://catalog.registries.digital.go.jp/rc/dataset/ba-o1-000000_g2-000003)
- [全国　町字マスター位置参照拡張　データセット mt_town_pos_all.csv](https://catalog.registries.digital.go.jp/rc/dataset/ba000004) 

2025/7/21時点のデータを加工して利用しています。

- 加工済みデータの[ダウンロード](https://ksasao.github.io/ReverseGeocode/merged.csv)　(約47MB)

データのライセンスは、[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja) です。
