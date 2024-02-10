from playwright.sync_api import sync_playwright
import argparse

from grafana_query_tool.login import login
from grafana_query_tool.utils import create_grafana_input_param
from grafana_query_tool.query_export import exec_query, export_result
from websession.websession import WebSession

def create_args() -> argparse.Namespace:

  parser = argparse.ArgumentParser(
    description='A tool to run queries in Grafana and download the results'
  )
  parser.add_argument(
    'datasource',
    help='Set the datasource (example: loki)'
  )
  parser.add_argument(
    'query',
    help='Set the query',
  )
  parser.add_argument(
    'from_',
    help='Specify the start time of the data',
  )
  parser.add_argument(
    'to',
    help='Specify the end time of the data',
  )
  parser.add_argument(
    '-i', '--org-id',
    help='Specify the Org ID (default: 1)',
    default='1',
  )
  parser.add_argument(
    '-r', '--record-video',
    action='store_true',
    help='Enable video recording',
  )
  parser.add_argument(
    '-e', '--env-file',
    help='Specify the filename of enviroment variables (default: .env)',
    default='.env',
  )
  parser.add_argument(
    '-o', '--output-filename',
    help='Specify the name of the output csv file',
    default=None,
  )

  return parser.parse_args()

if __name__ == '__main__':

  args = create_args()
  grafana_input_param = create_grafana_input_param(
      args.org_id,
      args.datasource,
      args.query,
      args.from_,
      args.to,
  )

  with sync_playwright() as playwright:

    websession = WebSession(playwright, record_video=args.record_video)

    websession = login(websession, args.env_file)

    websession = exec_query(
      websession,
      grafana_input_param,
      args.env_file,
    )

    websession = export_result(websession, args.output_filename)

    websession.close()

