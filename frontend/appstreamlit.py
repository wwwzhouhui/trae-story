import os
import streamlit as st
import requests
import asyncio
import time
from typing import Optional, Dict, Any

class StoryVideoClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8001", api_token: str = None):
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
        text_llm_provider: Optional[str] = "siliconflow",
        image_llm_provider: Optional[str] = "siliconflow",
        text_llm_model: Optional[str] = "Qwen/QwQ-32B",
        image_llm_model: Optional[str] = "black-forest-labs/FLUX.1-schnell"
    ) -> Dict[str, Any]:
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
        
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        else:
            st.warning("警告: 未提供API令牌，请求可能会被拒绝")

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            st.info(f"视频生成总耗时: {elapsed_time:.2f} 秒")
            
            return result
        except requests.exceptions.RequestException as e:
            end_time = time.time()
            elapsed_time = end_time - start_time
            st.error(f"请求失败，总耗时: {elapsed_time:.2f} 秒")
            raise Exception(f"Failed to generate video: {str(e)}")

def display_output():
    with st.container():
        if st.session_state.image_url:
            st.image(st.session_state.image_url, caption="故事配图")
            
        if st.session_state.video_url:
            st.video(st.session_state.video_url)
        st.text_area("生成的故事", value=st.session_state.story_text, height=200)

def main():
    # 在文件开头添加新的状态变量
    if "need_update" not in st.session_state:
        st.session_state.need_update = False

    st.set_page_config(page_title="儿童故事绘本生成器", layout="wide")
    st.title("儿童故事绘本生成器")

    # 创建两列布局
    col1, col2 = st.columns(2)

    with col1:
        text_llm_provider = st.selectbox(
            "文本 LLM 提供商",
            options=["siliconflow", "openai", "aliyun", "deepseek", "ollama"],
            index=0
        )
        
        image_llm_provider = st.selectbox(
            "图像 LLM 提供商",
            options=["siliconflow", "openai", "aliyun"],
            index=0
        )
        
        text_llm_model = st.text_input(
            "文本 LLM 模型",
            value="Qwen/QwQ-32B",
            placeholder="Qwen/QwQ-32B"
        )
        
        image_llm_model = st.text_input(
            "图像 LLM 模型",
            value="black-forest-labs/FLUX.1-schnell",
            placeholder="dall-e-3 或 flux-dev 或其他"
        )
        
        image_resolution = st.selectbox(
            "图像分辨率",
            options=[
                "1024*1024", "512*512", "1024*768", "1024*682",
                "1024*576", "768*1024", "682*1024", "576*1024"
            ],
            index=0
        )
        
        video_language = st.selectbox(
            "视频语言",
            options=["中文", "英文", "日语", "韩语"],
            index=0
        )
        
        voice_name = st.selectbox(
            "语音名称",
            options=[
                "zh-CN-XiaoxiaoNeural", "zh-CN-XiaoyiNeural", 
                "zh-CN-YunjianNeural", "zh-CN-YunxiNeural",
                "zh-CN-YunxiaNeural", "zh-CN-YunyangNeural",
                "es-US-AlonsoNeural", "es-US-PalomaNeural",
                "zh-HK-HiuGaaiNeural", "zh-HK-WanLungNeural",
                "zh-TW-HsiaoChenNeural", "zh-TW-YunJheNeural",
                "zu-ZA-ThandoNeural", "zu-ZA-ThembaNeural",
                "ja-JP-KeitaNeural", "ja-JP-NanamiNeural"
            ],
            index=0
        )
        
        story_theme = st.text_area(
            "故事主题",
            placeholder="请输入故事主题",
            height=100
        )
        
        story_sections = st.number_input(
            "故事分段，1-10",
            min_value=1,
            max_value=10,
            value=3,
            step=1
        )

    with col2:

        if "image_url" not in st.session_state:
            st.session_state.image_url = None
        if "video_url" not in st.session_state:
            st.session_state.video_url = None
        if "story_text" not in st.session_state:
            st.session_state.story_text = ""

        # 初始显示输出区域
        display_output()

    with col1:
        if st.button("生成故事"):
            language_map = {
                "中文": "zh-CN",
                "英文": "en-US",
                "日语": "ja-JP",
                "韩语": "ko-KR"
            }
    
            client = StoryVideoClient()
            
            try:
                with st.spinner("正在生成故事，请稍候..."):
                    # 由于 streamlit 不直接支持 async/await，我们使用同步方式调用
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    result = loop.run_until_complete(client.generate_video(
                        story_prompt=story_theme,
                        segments=int(story_sections),
                        language=language_map.get(video_language, "zh-CN"),
                        voice_name=voice_name,
                        voice_rate=1.0,
                        resolution=image_resolution,
                        text_llm_provider=text_llm_provider,
                        image_llm_provider=image_llm_provider,
                        text_llm_model=text_llm_model,
                        image_llm_model=image_llm_model
                    ))
                    
                    # 修改结果处理部分
                    if result["success"]:
                        st.session_state.video_url = result["data"]["video_url"]
                        st.session_state.story_text = result["data"].get("story_text", "故事生成成功，但无法获取文本内容")
                        
                        if "images" in result["data"] and len(result["data"]["images"]) > 0:
                            st.session_state.image_url = result["data"]["images"][0]
                        
                        # 生成成功后立即更新显示
                        with col2:
                            display_output()
                        st.success("故事生成成功！")
                        # 删除 st.rerun() 这一行
                    else:
                        st.error(f"故事生成失败: {result.get('message', '未知错误')}")
            except Exception as e:
                st.error(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()