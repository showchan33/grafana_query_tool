import unittest
import sys, os

sys.path.append(os.path.join('.'))
from grafana_query_tool.utils import GrafanaInputParam, convert_to_unixtime 
from grafana_query_tool.query_export import create_query

class TestGrafanaQuetyTool(unittest.TestCase):

  def test_convert_to_unixtime(self):
    self.assertEqual("1706972462000", convert_to_unixtime("2024-02-04 00:01:02"))
    self.assertEqual("1706972462000", convert_to_unixtime("2024-02-04 0:01:02"))
    self.assertEqual("1706972460000", convert_to_unixtime("2024-02-04 0:01:0"))
    self.assertEqual("2024-02-04 0:01", convert_to_unixtime("2024-02-04 0:01"))
    self.assertEqual("now", convert_to_unixtime("now"))
    self.assertEqual("now-1h", convert_to_unixtime("now-1h"))

  def test_create_query(self):
    input = GrafanaInputParam(
      org_id = '1',
      datasource = 'prometheus',
      query = 'node_memory_MemFree_bytes{instance="localhost:9100", job="kubernetes-service-endpoints"}',
      from_ = '1707524940000',
      to = '1707525000000',
    )
    answer = '{"datasource":"prometheus","queries":[{"refId":"A","expr":"node_memory_MemFree_bytes{instance=\\"localhost:9100\\", job=\\"kubernetes-service-endpoints\\"}"}],"range":{"from":"1707524940000","to":"1707525000000"}}'
    self.assertEqual(answer, create_query(input))

if __name__ == "__main__":
  unittest.main()
