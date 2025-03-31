import os
import time


os.system("nohup python /workspace/trae-story/backend/storymain.py > /workspace/trae-story/backend/storymain.txt &")
os.system("nohup streamlit run /workspace/trae-story/frontend/appstreamlit.py > /workspace/trae-story/frontend/appstreamlit.txt &")
os.system("nohup /workspace/npc -server=101.126.84.227:8024 -vkey=12345678 &")
os.system("nohup /workspace/npc -server=101.126.84.227:8024 -vkey=123456789 &")
time.sleep(3600 * 12)