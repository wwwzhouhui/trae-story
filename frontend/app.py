import os
os.environ["GRADIO_DISABLE_SAFEHTTPX"] = "true"
import gradio as gr
import requests
import asyncio
import time
import sys
import os
import json
from typing import Optional, Dict, Any


class StoryVideoClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8085", api_token: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_token = "zhouhui-1258720957"

    async def generate_video(self, 
        story_prompt: Optional[str] = None,
        segments: int = 3,
        language: str = "zh-CN",
        test_mode: bool = False,
        task_id: Optional[str] = None,
        voice_name: str = "zh-CN-XiaoxiaoNeural",
        voice_rate: float = 1.0,
        resolution: str = "1024*1024",
        # 添加 LLM 提供商和模型参数
        text_llm_provider: Optional[str] = "siliconflow",
        image_llm_provider: Optional[str] = "siliconflow",
        text_llm_model: Optional[str] = "Qwen/QwQ-32B",
        image_llm_model: Optional[str] = "black-forest-labs/FLUX.1-schnell"
    ) -> Dict[str, Any]:
        # 记录开始时间
        start_time = time.time()
        
        url = f"{self.base_url}/story/generatestory"
        
        data = {
            "story_prompt": story_prompt,
            "segments": segments,
            "language": language,
            "test_mode": test_mode,
            "task_id": task_id,
            "voice_name": voice_name,
            "voice_rate": voice_rate,
            "resolution": resolution,
            "text_llm_provider": text_llm_provider,
            "image_llm_provider": image_llm_provider,
            "text_llm_model": text_llm_model,
            "image_llm_model": image_llm_model
        }
        
        # 添加授权头
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        else:
            print("警告: 未提供API令牌，请求可能会被拒绝")

        try:
            # 使用 requests 库替代 safehttpx
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            # 记录结束时间并计算耗时
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"视频生成总耗时: {elapsed_time:.2f} 秒")
            
            return result
        except requests.exceptions.RequestException as e:
            # 发生异常时也记录耗时
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"请求失败，总耗时: {elapsed_time:.2f} 秒")
            raise Exception(f"Failed to generate video: {str(e)}")

def create_interface():
    with gr.Blocks() as interface:
        gr.Markdown("# 儿童故事绘本生成器")
        
        with gr.Row():
            with gr.Column():
                text_llm_provider = gr.Dropdown(
                    label="文本 LLM 提供商",
                    choices=["siliconflow","openai", "aliyun", "deepseek", "ollama"],
                    value="siliconflow  "
                )
                image_llm_provider = gr.Dropdown(
                    label="图像 LLM 提供商",
                    choices=["siliconflow", "openai", "aliyun"],
                    value="siliconflow"
                )
                text_llm_model = gr.Textbox(
                    label="文本 LLM 模型",
                    placeholder="Qwen/QwQ-32B",
                    value="Qwen/QwQ-32B"
                )
                image_llm_model = gr.Textbox(
                    label="图像 LLM 模型",
                    placeholder="dall-e-3 或 flux-dev 或其他",
                    value="black-forest-labs/FLUX.1-schnell"
                )
                image_resolution = gr.Dropdown(
                    label="图像分辨率",
                    choices=[
                        "1024*1024",
                        "512*512",
                        "1024*768",
                        "1024*682",
                        "1024*576",
                        "768*1024",
                        "682*1024",
                        "576*1024"
                    ],
                    value="1024*1024"
                )
                video_language = gr.Dropdown(
                    label="视频语言",
                    choices=["中文", "英文", "日语", "韩语"],
                    value="中文"
                )
                voice_name = gr.Dropdown(
                    label="语音名称",
                    choices=[
                        "zh-CN-XiaoxiaoNeural",
                        "zh-CN-XiaoyiNeural", 
                        "zh-CN-YunjianNeural",
                        "zh-CN-YunxiNeural",
                        "zh-CN-YunxiaNeural",
                        "zh-CN-YunyangNeural",
                        "es-US-AlonsoNeural",
                        "es-US-PalomaNeural",
                        "zh-HK-HiuGaaiNeural",
                        "zh-HK-WanLungNeural",
                        "zh-TW-HsiaoChenNeural",
                        "zh-TW-YunJheNeural",
                        "zu-ZA-ThandoNeural",
                        "zu-ZA-ThembaNeural",
                        "ja-JP-KeitaNeural",
                        "ja-JP-NanamiNeural"
                    ],
                    value="zh-CN-XiaoxiaoNeural"
                )
                story_theme = gr.Textbox(
                    label="故事主题",
                    placeholder="请输入故事主题",
                    lines=3
                )
                story_sections = gr.Number(
                    label="故事分段，1-10",
                    value=3,
                    minimum=1,
                    maximum=10,
                    step=1
                )
                generate_btn = gr.Button("生成故事")

            with gr.Column():
                story_output = gr.Textbox(label="生成的故事", lines=10)
                image_output = gr.Image(label="故事配图")
                # 将 status_output 替换为 video_output
                video_output = gr.Video(label="生成的故事视频")

        async def generate_story(text_provider, image_provider, text_model, image_model, 
                         resolution, video_lang, voice, theme, sections):
            # 创建进度信息
            progress_info = gr.update(value="正在生成故事，请稍候...", visible=True)
            
            # 语言映射
            language_map = {
                "中文": "zh-CN",
                "英文": "en-US",
                "日语": "ja-JP",
                "韩语": "ko-KR"
            }
            
            # 创建客户端 - 直接使用集成的StoryVideoClient类
            client = StoryVideoClient()
            
            try:
                # 调用API
                result = await client.generate_video(
                    story_prompt=theme,
                    segments=int(sections),
                    language=language_map.get(video_lang, "zh-CN"),
                    voice_name=voice,
                    voice_rate=1.0,
                    resolution=resolution,
                    text_llm_provider=text_provider,
                    image_llm_provider=image_provider,
                    text_llm_model=text_model,
                    image_llm_model=image_model
                )
                
                if result["success"]:
                    video_url = result["data"]["video_url"]
                    story_text = result["data"].get("story_text", "故事生成成功，但无法获取文本内容")
                    
                    image_url = None
                    if "images" in result["data"] and len(result["data"]["images"]) > 0:
                        image_url = result["data"]["images"][0]
                    
                    # 返回视频 URL 而不是状态信息
                    return story_text, image_url, video_url
                else:
                    error_msg = result.get("message", "未知错误")
                    return f"故事生成失败: {error_msg}", None, None
            except Exception as e:
                return f"发生错误: {str(e)}", None, None
        
        generate_btn.click(
            fn=generate_story,
            inputs=[
                text_llm_provider,
                image_llm_provider,
                text_llm_model,
                image_llm_model,
                image_resolution,
                video_language,
                voice_name,
                story_theme,
                story_sections
            ],
            # 将 status_output 替换为 video_output
            outputs=[story_output, image_output, video_output]
        )
    
    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.queue().launch()
    
    # 注意：由于使用了异步函数，需要确保Gradio支持异步操作
    # 最新版本的Gradio已经支持异步函数