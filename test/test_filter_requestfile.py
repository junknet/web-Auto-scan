import os
import re
import os
base_lib = '/home/junknet/Desktop/web安全检测/http_log/'
files = os.listdir(base_lib)
files = filter(lambda x: x.endswith('request.txt'), files)

post_urls = []
get_urls = []
post_re = re.compile(r'POST (.+?) HTTP/1.1')
get_re = re.compile(r'GET (.+?) HTTP/1.1')
for file in files:
    with open(base_lib+file) as f:
        line = f.readline()
        if post_re.findall(line) and line not in post_urls:
            post_urls.append(line)
            os.system('cp {} {}'.format(
                base_lib+file, base_lib+'post_request/'+file))
        if get_re.findall(line) and line not in get_urls:
            get_urls.append(line)
            os.system('cp {} {}'.format(
                base_lib+file, base_lib+'get_request/'+file))
