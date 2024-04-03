# About grafana_query_tool

grafana_query_tool is a tool that enables the following operations in Grafana WebUI to be performed via CLI.

* Login to Grafana WebUI
* Enter your query in Grafana Explore
* Download query execution results in CSV format

# Requirement

* Environment in which operation was verified
    * OS
        * Linux
            * Ubuntu 20.04
        * Mac OS
            * 14.2.1
        * Not tested on Windows
    * Grafana Version
        * 10.1.0, 10.4.0
* Tool
    * Python3
        * Version tested is 3.10 series
    * Poerty or pip3

# Preparation

## Install Package

Install the packages necessary to run grafana_query_tool in one of the following ways.

### Method 1: Using Poetry

```
poetry install
```

### Method 2: Using pip

```
pip3 install -r requirements.txt
```

## Install Playwright

```
playwright install-deps
```

## Setting up credentials to login to Grafana

Copy ``.env.sample`` as ``.env``.<br>
Modify the following environment variables to match your environment.

```shell:.env
GRAFANA_URL="https://grafana.example.com"
GRAFANA_USERNAME="username"
GRAFANA_PASSWORD="password"
```

Modification example
```shell:.env
GRAFANA_URL="https://grafana-your-site.example.com"
GRAFANA_USERNAME="your-username"
GRAFANA_PASSWORD="your-password"
```

# Usage

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


## An example of Usage
Here is an example of getting ``node_memory_MemFree_bytes`` metrics with ``prometheus`` as the data source.

### Execution command
```
python3 main.py \
prometheus \
'node_memory_MemFree_bytes{instance="hostname-of-node:9100", job="kubernetes-service-endpoints"}' \
"2024-02-05 13:20:00" \
"2024-02-05 13:30:00" \
-o output/result.csv
```

The example above uses the format ``yyyy-mm-dd HH:MM:SS`` as the time period for which to retrieve data. As an alternative, you can also specify relative times such as ``"now"`` or ``"now-1h"``.

### Output result
```
Attempting to login to https://grafana-your-site.example.com
Running a query in explore.
Downloading query results in progress.
Saved results to output/result.csv
```

### Example of CSV file output

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
