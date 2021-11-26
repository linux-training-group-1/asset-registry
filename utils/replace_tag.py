import sys
import re
file_name = sys.argv[1]
new_tag = sys.argv[2]

f = open(file_name, 'r')
file_data = f.read()
f.close()

new_data = re.sub('/asset-app:.*', new_tag, file_data, flags=re.M)

f = open(file_name, 'w')
f.write(new_data)
f.close()
