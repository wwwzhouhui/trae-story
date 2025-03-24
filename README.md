# trae-story
使用trae生成的项目

## 项目说明

本项目可以输入一个故事主题，在输入分镜头的数量，使用大语言模型、文生图模型等生成故事视频，视频中包含大模型生成的图片、故事内容，以及音频和字幕信息。

项目后端技术栈为 python + fastapi 框架，前端为 streamlit实现。

## 界面截图

  <video controls>   <source src='https://dify-1258720957.cos.ap-nanjing.myqcloud.com/videos/video20250318005720.mp4' type='video/mp4'>{filename}</video>

![image-20250324232230796](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250324232230796.png)

![image-20250324232246273](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250324232246273.png)

![image-20250324232305143](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250324232305143.png)

## 使用说明

### 下载本项目

```
https://github.com/wwwzhouhui/trae-story
```

### 启动项目

本地电脑上安装python 运行环境，建议python3.12+

后端服务

```shell
pip install -r requirements.txt
cd backend
python storymain.py
```

启动完成后

![image-20250324231832369](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250324231832369.png)

后端启动后使用一个8085端口的服务，对外提供API接口服务。

前端服务

```shell
cd frontend
streamlit run appstreamlit.py  

```

![image-20250324232005472](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250324232005472.png)

### 验证及测试

浏览器输入网址（本地测试）http://localhost:8501/

填写：文本 LLM 提供商、图像 LLM 提供商、文本 LLM 模型、图像 LLM 模型、图像分辨率、视频语言、语音名称、故事主题、故事分段，1-10

其中模型和模型供应商、语言等程序我们从下拉选择中选择。目前我主要用硅基流动提供的模型测试，所以可以选择硅基的相关模型

对用户来说只需要输入 故事主题、故事分段数量其他值都可以默认填写

![image-20250324215120195](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250324215120195.png.png)

填写后点击"生成故事"按钮 等待后端处理.点击完成后右边大概需要5-6分钟时间（这个时间取决分境数量，数量越多 生成的时间越长）

![image-20250324215315450](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250324215315450.png.png.png)

最上方生成一张配图。

![image-20250324215354801](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250324215354801.png.png)

中间生成儿童故事绘本视频合成

![image-20250324215427918](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250324215427918.png.png)

最下方生成故事内容。
