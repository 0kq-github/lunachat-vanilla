import time
import re

class logger:
  def __init__(self):
    pass

  def log_reader(self,log_path:str):
    '''
    ログの読み取り

    Parameters

    ----------
    log_path : str
         latest.logのパス


    yield : str
        最新のログ

        停止した際は"server closed"
    '''

    log_latest = ""
    while True:
      try:
        with open(log_path,"r") as f:
          log = f.read().split("\n")
          if not log[0]:
            continue
          if log[-2] == log_latest:
            continue
          log_latest = log[-2]
          log_stop = re.search("\[Server thread\/INFO\]\: ThreadedAnvilChunkStorage \(.*\)\: All chunks are saved",log_latest)
          if log_stop:
            yield "server closed"
            break
          yield log_latest
      except PermissionError:
        time.sleep(3)
        continue
    
  def log_formatter(self,log:str):
    '''
    ログの整形

    chat join left start stopに対応


    Parameters

    ----------
    log : str
        整形したいログ
    

    return : str | None
        整形したログ


        一致が無い場合None
    '''

    m_join = re.search("\[Render thread\/INFO\]\: .* joined the game",log)
    m_left = re.search("\[Render thread\/INFO\]\: .* left the game",log)
    m_chat = re.search("\[Render thread\/INFO\]\: \[CHAT\] .*",log)
    if m_chat:
      m_chat = re.sub("\ \ +","",m_chat.group())
      return re.sub("\[Render thread\/INFO\]\: \[CHAT\]","",m_chat,1)
    elif "[Server thread/INFO]: Starting minecraft server" in log:
      return "サーバーを起動中..."
    elif "[Server thread/INFO]: Done" in log:
      return "サーバーが起動しました"
    elif "[Server thread/INFO]: Stopping server" in log:
      return "サーバーを停止中..."
    elif log == "server closed":
      return "サーバーが閉鎖されました"
    elif m_join:
      return re.sub("\[Render thread\/INFO\]\: ","",m_join.group())
    elif m_left:
      return re.sub("\[Render thread\/INFO\]\: ","",m_left.group())
    else:
      return None


'''
log_path = "./server/logs/latest.log"
for line in log_reader(log_path):
  print(line)
'''
