import sys

file_name = sys.argv[1]
old_tag = sys.argv[2]
new_tag = sys.argv[3]

f = open(file_name, 'r')
file_data = f.read()
f.close()

new_data = file_data.replace(old_tag, new_tag)

f = open(file_name, 'w')
f.write(new_data)
f.close()
