# 报告结构
report_buff = {
    "http:// credit.chaozhou.gov.cn": {"sql_attack_param": []}}  # 列表里存length


def filter_response_use_length(url: str, attack_kind: str, length: int):
    # 初始化结构表
    if url not in report_buff:
        report_buff[url] = {attack_kind: []}
    if attack_kind not in report_buff[url]:
        report_buff[url] = {attack_kind: []}
    if length not in report_buff[url][attack_kind]:
        report_buff[url][attack_kind].append(length)
        return True
    return False
