from pyokaka import okaka
from log import logger as mclog
import re
from mcrcon import MCRcon
import datetime
import config


version = "0.1"

def lprint(*text:str):
  """
  [現在時刻] text
  の形式でprint
  """
  text = [v for v in map(lambda x:str(x),text)]
  datime_now = datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
  print(f"[{datime_now}] {' '.join(text)}")


def main(path):
  try:
    for line in mclog().log_reader(path):
      line = re.sub("\[\d\d\:\d\d\:\d\d\]\ \[Server\ thread/INFO\]\:\ ","",line)
      player_name = re.search("(?<=\<)[^(\<\>)]*?(?=\>\ )",line)
      if not player_name:
        continue
      else:
        player_name = player_name.group()
        player_chat = re.sub(f"<{player_name}> ","",line)
      kana = okaka.convert(player_chat)
      with MCRcon(config.RCON_IP,config.RCON_PASSWORD,config.RCON_PORT) as mcr:
        mcr.command('tellraw @a [{"text":"["},{"text":"lunachat","color":"gold"},{"text":"] <'+player_name+'> '+kana+'","color":"white"}]')
      lprint(f"<{player_name}> {kana}")
  
  except KeyboardInterrupt:
    with MCRcon(config.RCON_IP,config.RCON_PASSWORD,config.RCON_PORT) as mcr:
      mcr.command('tellraw @a [{"text":"["},{"text":"lunachat","color":"gold"},{"text":"] lunachat vanilla v'+version+' を終了中...","color":"white"}]')
    lprint(f"lunachat vanilla v{version} を終了中...")
    exit()

if __name__ == "__main__":
  try:
    with MCRcon(config.RCON_IP,config.RCON_PASSWORD,config.RCON_PORT) as mcr:
      mcr.command('tellraw @a [{"text":"["},{"text":"lunachat","color":"gold"},{"text":"] lunachat vanilla v'+version+' by 0kq","color":"white"}]')
      mcr.command('tellraw @a [{"text":"["},{"text":"lunachat","color":"gold"},{"text":"] lunachat vanilla v'+version+' が起動しました","color":"white"}]')
  except Exception as e:
    lprint("rconの接続に失敗しました。",e)
    exit()
  lprint(f"lunachat vanilla v{version} by 0kq")
  lprint(f"lunachat vanilla v{version} を起動中...")
  main(config.LOG_PATH)