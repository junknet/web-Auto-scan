from scan.output import report_print
from scan.filter import filter_response_use_length

len_check = ["sql_attack_param", "brute_attack_load"]


def check_response(url, attack_kind, request_body, response: str):
    if attack_kind in len_check:
        if filter_response_use_length(url, attack_kind, response.__len__()):
            report_print(url, attack_kind, request_body)
    if attack_kind == "xss_attack_param":
        if "<script>alert('XSS')</script>" in response:
            report_print(url, attack_kind, request_body)
