
import sys
sys.path.append('../src/')
from scan.parse_request import RequestParse


qwe = RequestParse("../request_log/25-request.txt")
print(qwe.meta())
