from datetime import datetime
import time
from grafana_query_tool.query_export import GrafanaInputParam

def convert_to_unixtime(
  time_string: str
) -> str:
  datetime_format = "%Y-%m-%d %H:%M:%S"
  
  try:
    dt_object = datetime.strptime(time_string, datetime_format)
    unix_time = int(time.mktime(dt_object.timetuple())) * 1000
    return str(unix_time)
  except ValueError:
    # If not in the specified format, returns as string
    return time_string

def create_grafana_input_param(
  org_id: str,
  datasource: str,
  query: str,
  from_: str,
  to: str,
) -> GrafanaInputParam:
  
  return GrafanaInputParam(
    org_id = org_id,
    datasource = datasource,
    query = query,
    from_ = convert_to_unixtime(from_),
    to = convert_to_unixtime(to),
  )
