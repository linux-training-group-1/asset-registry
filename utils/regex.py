import re

text = "        - name: appdeploy\nimage: dock-reg-0001.ml/asset-app:0.1.0\nimagePullPolicy: Always"
t = re.sub('/asset-app:.*', '/'+'asset-app:0.4.5', text, flags=re.M)
print(t)
