import subprocess
import re

print("必要なパッケージをインストール中...")
subprocess.run("pip install -r requirements.txt")
print("パッケージのインストールが完了しました")
print("server.propertiesを設定中...")
with open("../server.properties","r") as f:
  config = f.read()
  config = re.sub("enable-rcon=false","enable-rcon=true",config)
  config = re.sub("rcon.port=\d*\n","rcon.port=25575\n",config)
  config = re.sub("broadcast-rcon-to-ops=true","broadcast-rcon-to-ops=false",config)
  config = re.sub("rcon.password=.*\n","rcon.password=lunachat\n",config)
with open("../server.properties","w") as f:
  f.write(config)
print("server.propertiesの設定が完了しました")