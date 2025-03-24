from fastapi import APIRouter, HTTPException, Query, Header, Depends, Request
from fastapi.staticfiles import StaticFiles
from loguru import logger
from services.video import generate_video, create_video_with_scenes, generate_voice
from schemas.video import VideoGenerateRequest, VideoGenerateResponse, StoryScene
import os
import json
from utils.utils import extract_id
import configparser
from starlette.requests import Request as StarletteRequest

router = APIRouter()

# 读取配置文件中的API密钥
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')
config.read(config_path)

try:
    # 尝试读取配置文件
    if not config.read(config_path, encoding='utf-8'):
        raise FileNotFoundError(f"配置文件未找到: {config_path}")
except Exception as e:
    logger.error(f"读取配置文件失败: {str(e)}")
    raise

def verify_auth_token(authorization: str = Header(None)):
    """验证 Authorization Header 中的 Bearer Token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization Scheme")
    
    # 从配置文件读取有效token列表
    try:
        valid_tokens = json.loads(config.get('auth', 'valid_tokens'))
        if token not in valid_tokens:
            raise HTTPException(status_code=403, detail="Invalid or Expired Token")
    except (configparser.NoSectionError, configparser.NoOptionError):
        logger.error("配置文件中缺少auth部分或valid_tokens选项")
        raise HTTPException(status_code=500, detail="Server configuration error")
    
    return token

# 添加静态文件目录配置
TASKS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tasks')
if not os.path.exists(TASKS_DIR):
    os.makedirs(TASKS_DIR)

@router.post("/story/generatestory")
async def generate_video_endpoint(
    request: VideoGenerateRequest,
    req: Request,
    auth_token: str = Depends(verify_auth_token)
):
    """生成视频"""
    try:
        #video_file = await generate_video(request)
        video_file = "f:/work/code/AIcode/story/src/backend/tasks/1742821862/video20250324211114.mp4"
        logger.info(f"Video generated successfully: {video_file}")
        task_id = extract_id(video_file)
        video_filename = os.path.basename(video_file)
        
        # 读取story.json文件
        story_json_path = os.path.join(os.path.dirname(video_file), 'story.json')
        with open(story_json_path, 'r', encoding='utf-8') as f:
            story_data = json.load(f)
        
        # 提取所有场景的文本并拼接
        story_text = '\n'.join(scene['text'] for scene in story_data['scenes'])
        # 收集所有场景的图片URL
        images = [scene['url'] for scene in story_data['scenes']]
        
        # 修改 URL 构建方式
        host = req.headers.get("host", "localhost:8085")
        scheme = req.headers.get("x-forwarded-proto", "http")
        base_url = f"{scheme}://{host}"
        video_url = f"{base_url}/tasks/{task_id}/{video_filename}"
        
        logger.info(f"Video URL: {video_url}")
        logger.info(f"Story Text: {story_text}")
        logger.info(f"Images: {images}")
        return VideoGenerateResponse(
            success=True,
            data={
                "video_url": video_url,
                "story_text": story_text,  # 使用从story.json中提取的文本
                "images": images  # 使用从story.json中提取的图片URL列表
            }
        )
    except Exception as e:
        logger.error(f"Failed to generate video: {str(e)}")
        return VideoGenerateResponse(
            success=False,
            message=str(e)
        )


