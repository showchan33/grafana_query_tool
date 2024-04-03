# grafana_query_toolの概要

grafana_query_toolは、GrafanaにおけるWebUIでの以下の操作をコマンドラインで実行可能にするツールです。

* GrafanaのWebUIにログイン
* Exploreでクエリを入力
* クエリの実行結果をCSV形式でダウンロード

# 必要条件

* 動作確認環境
    * OS
        * Linux
            * Ubuntu 20.04
        * Mac OS
            * 14.2.1
        * ※Windowsでの動作は未確認
    * Grafanaのバージョン
        * 10.1.0, 10.4.0
* ツール
    * Python3
        * 動作確認バージョンは3.10系
    * Poerty または pip3

# 事前準備

## パッケージのインストール

以下のいずれかの方法で、grafana_query_toolを動かすのに必要なパッケージをインストールします。

### 方法1: Poetryを利用

```
poetry install
```

### 方法2: pipを利用

```
pip3 install -r requirements.txt
```

## Playwrightのインストール

```
playwright install-deps
```

## Grafanaにログインするための認証情報の設定

``.env.sample``を``.env``という名前でコピーします。<br>
以下の環境変数を、お使いの環境に合わせてに変更します。

```shell:.env
GRAFANA_URL="https://grafana.example.com"
GRAFANA_USERNAME="username"
GRAFANA_PASSWORD="password"
```
↓ 変更例
```shell:.env
GRAFANA_URL="https://grafana-your-site.example.com"
GRAFANA_USERNAME="your-username"
GRAFANA_PASSWORD="your-password"
```

# 使い方

```
$ python main.py -h
usage: main.py [-h] [-i ORG_ID] [-r] [-e ENV_FILE] [-o OUTPUT_FILENAME] [-g {10.1,10.4}] datasource query from_ to

A tool to run queries in Grafana and download the results

positional arguments:
  datasource            Set the datasource (example: prometheus, loki)
  query                 Set the query
  from_                 Specify the start time of the data
  to                    Specify the end time of the data

options:
  -h, --help            show this help message and exit
  -i ORG_ID, --org-id ORG_ID
                        Specify the Org ID (default: 1)
  -r, --record-video    Enable video recording
  -e ENV_FILE, --env-file ENV_FILE
                        Specify the filename of enviroment variables (default: .env)
  -o OUTPUT_FILENAME, --output-filename OUTPUT_FILENAME
                        Specify the name of the output csv file
  -g {10.1,10.4}, --grafana-version {10.1,10.4}
                        Specify the version of Grafana to query. Default is 10.4
```


## 利用例
データソースに``prometheus``を指定して、``node_memory_MemFree_bytes``のメトリクスを取得する例です。

### 実行コマンド
```
python3 main.py \
prometheus \
'node_memory_MemFree_bytes{instance="hostname-of-node:9100", job="kubernetes-service-endpoints"}' \
"2024-02-05 13:20:00" \
"2024-02-05 13:30:00" \
-o output/result.csv
```

上の例ではデータを取得する期間として``yyyy-mm-dd HH:MM:SS``のフォーマットを使っていますが、``"now"``や``"now-1h"``のような相対的な時間も指定できます。

### 出力結果
```
Attempting to login to https://grafana-your-site.example.com
Running a query in explore.
Downloading query results in progress.
Saved results to output/result.csv
```

### CSVファイルの出力例

```result.csv
"Time","node_memory_MemFree_bytes{app_kubernetes_io_component=""metrics"", app_kubernetes_io_instance=""prometheus"", app_kubernetes_io_managed_by=""Helm"", app_kubernetes_io_name=""prometheus-node-exporter"", app_kubernetes_io_part_of=""prometheus-node-exporter"", app_kubernetes_io_version=""1.6.0"", helm_sh_chart=""prometheus-node-exporter-4.22.0"", instance=""hostname-of-node:9100"", job=""kubernetes-service-endpoints"", namespace=""prometheus"", node=""node01"", service=""prometheus-prometheus-node-exporter""}"
1707538170000,985042944
1707538185000,1067003904
1707538200000,1067003904
1707538215000,1067003904
1707538230000,1067003904
1707538245000,976990208
1707538260000,976990208
1707538275000,976990208
...
```

# Author
showchan33

# License
"grafana_query_tool" is under [GPL license](https://www.gnu.org/licenses/licenses.en.html).
