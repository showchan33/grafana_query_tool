import os, json, urllib.parse, time
from dotenv import load_dotenv
from collections import namedtuple
from websession.websession import WebSession

GrafanaInputParam = \
  namedtuple(
    'GrafanaInputParam',
    [
      'org_id',
      'datasource',
      'query',
      'from_',
      'to',
    ]
  )

def create_query(
  grafana_input_param: GrafanaInputParam,
) -> str:

  data_dict = {
    "datasource": grafana_input_param.datasource,
    "queries": [
       {
          "refId": "A",
          "expr": grafana_input_param.query
       },
    ],
    "range":
    {
      "from": grafana_input_param.from_,
      "to": grafana_input_param.to,
    },
  }

  json_string = json.dumps(data_dict, separators=(',', ':'))
  return json_string.replace('\n', '')

def exec_query(
  websession: WebSession,
  grafana_input_param: GrafanaInputParam,
  env_file: str = ".env",
) -> WebSession:

  load_dotenv(env_file)
  GRAFANA_URL = os.getenv('GRAFANA_URL')

  print("Running a query in explore.")

  query_string = create_query(grafana_input_param)
  query_string_url_encoded = urllib.parse.quote(query_string)

  time.sleep(2)
  explore_url = f"{GRAFANA_URL}/explore?orgId={grafana_input_param.org_id}&left={query_string_url_encoded}"
  websession.page.goto(explore_url)
  time.sleep(1)

  return websession

def export_result(
  websession: WebSession,
  grafana_version: str,
  output_filename: str = None
) -> WebSession:

  if grafana_version == "10.1":
    websession.page.get_by_label("Query inspector button").click()
    time.sleep(1)
    websession.page.get_by_label("Tab Data").click()
  else:
    websession.page.get_by_role("button", name="Download").click()
  time.sleep(1)

  print("Downloading query results in progress.")

  with websession.page.expect_download() as download_info:
    if grafana_version == "10.1":
      websession.page.get_by_role("button", name="Download CSV").click()
    else:
      websession.page.get_by_role("menuitem", name="csv").click()
  download = download_info.value

  if output_filename is None:
    output_filename = f"./output/{download.suggested_filename}"

  download.save_as(f"{output_filename}")

  print(f"Saved results to {output_filename}")

  return websession
