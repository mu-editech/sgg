
# Name
**Salary-Graph-Generator**
**（給与情報統合集計基盤）**

# Overview
給与明細のPDFファイルを投入して、各項目についての数値を取得＋蓄積し、集計結果を提示するシステム
S3の特定位置にPDFの給与・賞与明細をPUTすると、自動でデータを取得・蓄積し、グラフで閲覧できるシステム。
今までの給与・賞与の合計、残業時間の推移などがわかる。
PDFの帳票をCSVに変換しBIツールにて可視化するので、振込明細など似たインプットを持つシステムにも応用可能な点がメリット。

### DynamoDBイメージ
<img width="1086" alt="dynamoDB_table" src="https://user-images.githubusercontent.com/58851029/73407089-67b0e880-433b-11ea-9ebd-c79f78d4c1c6.png">

### ダッシュボードイメージ


# Architect
![Salary-Graph-Generator](https://user-images.githubusercontent.com/58851029/73407007-405a1b80-433b-11ea-8464-9ae7e392627c.png)

### 処理フロー
1. S3の特定の場所に給与明細データをアップロードしておく
2. CloudWatch Eventsが定期的に発動し、Fargateをキック
3. 帳票データから数値を抽出し、DynamoDBに格納
4. DynamoDBからS3に出力したデータをQuickSightで閲覧

### 補足
- CloudWatch Eventsでのキックは、今後イベントドリブンな方法に変更予定。
- 

# Requirement
requirements.txt参照。


# Setup
※現在terraformを使った自動構築方法を確立中。

# Licence
Copyright (c) 2020 MU-tech
Released under the [MIT license](https://opensource.org/licenses/mit-license.php)


### Author

[むーてく(MU-tech)](https://github.com/mu-editech)