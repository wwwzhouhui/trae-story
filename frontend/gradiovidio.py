import gradio as gr

def generate_video():
    # 假设这是从后端返回的远程视频 URL
    remote_video_url = "https://dify-1258720957.cos.ap-nanjing.myqcloud.com/videos/video20250318005720.mp4"
    return remote_video_url

with gr.Blocks() as demo:
    gr.Markdown("# 视频生成示例")
    
    with gr.Row():
        generate_btn = gr.Button("生成视频")
        video_output = gr.Video(label="生成的视频")
    
    def on_generate():
        # 调用生成函数并返回视频 URL
        return generate_video()
    
    generate_btn.click(on_generate, outputs=video_output)

demo.launch()