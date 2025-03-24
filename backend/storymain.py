from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.video import router as video_router, TASKS_DIR
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保任务目录存在
if not os.path.exists(TASKS_DIR):
    os.makedirs(TASKS_DIR)

# 挂载静态文件目录要在路由之前
app.mount("/tasks", StaticFiles(directory=TASKS_DIR), name="tasks")

# 包含视频路由
app.include_router(video_router, prefix="")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8085)