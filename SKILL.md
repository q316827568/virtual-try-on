---
name: virtual-try-on
description: 虚拟换装 - 使用 AI 技术将服装合成到人物图像上，基于 ComfyUI-IDM-VTON
tags:
  - virtual try-on
  - clothing
  - fashion
  - AI image
  - ComfyUI
  - IDM-VTON
triggers:
  - 虚拟换装
  - virtual try on
  - 试穿
  - 换装
  - 衣服合成
  - AI试衣
---

# 虚拟换装 (Virtual Try-On)

使用 ComfyUI-IDM-VTON 实现虚拟换装功能，将服装图片合成到人物图像上。

## 硬件要求

- **GPU**: 至少 16GB 显存
- **存储**: 约 10GB 用于模型文件

## 安装步骤

### 1. 安装 ComfyUI

```bash
# 克隆 ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# 安装依赖
pip install -r requirements.txt
```

### 2. 安装 ComfyUI-IDM-VTON

**方式一：ComfyUI Manager（推荐）**
1. 打开 ComfyUI Manager
2. 搜索 "ComfyUI-IDM-VTON"（作者: TemryL）
3. 点击安装

**方式二：手动安装**
```bash
cd custom_nodes
git clone https://github.com/TemryL/ComfyUI-IDM-VTON.git
cd ComfyUI-IDM-VTON
python install.py
```

模型权重会自动从 HuggingFace 下载到 `models/` 目录。

### 3. 安装依赖节点

- [ComfyUI Segment Anything](https://github.com/storyicon/comfyui_segment_anything) - 用于生成图像蒙版
- [ComfyUI ControlNet Auxiliary Preprocessors](https://github.com/Fannovel16/comfyui_controlnet_aux) - 用于 DensePose 姿态估计

## 使用方法

### 准备图片

1. **人物图 (Garment)**: 穿着需要保留部分的人物照片
2. **服装图 ( cloth)**: 要换上的服装图片

### 运行工作流

1. 启动 ComfyUI
2. 加载 `workflow.json` 工作流文件
3. 输入人物图和服装图
4. 点击 "Queue Prompt" 开始生成

### Python 脚本方式

```python
from PIL import Image
import torch
from diffusers import StableDiffusionInpaintPipeline

# 加载模型
pipe = StableDiffusionInpipeline.from_pretrained(
    "yisol/IDM-VTON",
    torch_dtype=torch.float16
).to("cuda")

# 准备输入
person_image = Image.open("person.jpg")
cloth_image = Image.open("cloth.jpg")

# 生成
result = pipe(
    prompt="a person wearing the cloth",
    image=person_image,
    mask_image=mask,
    num_inference_steps=30
).images[0]

result.save("result.jpg")
```

## 工作流节点说明

| 节点 | 功能 |
|------|------|
| Load Image | 加载人物图和服装图 |
| SAM (Segment Anything) | 生成人物蒙版 |
| DensePose Preprocessor | 提取身体姿态信息 |
| IDM-VTON | 核心换装模型 |
| VAE Decode | 解码生成图像 |

## 常见问题

### Q: 显存不足怎么办？
A: 需要至少 16GB 显存。可尝试降低分辨率或使用量化模型。

### Q: 生成效果不好？
A: 尝试：
- 调整人物和服装图的分辨率（建议 512x768 或 768x1024）
- 使用纯色背景的人物图
- 确保服装图清晰、主体突出

### Q: 如何获取更好的结果？
A:
- 使用高清的人物和服装图片
- 人物图最好是正面的全身照
- 服装图最好是平整拍摄的正面图

## 相关资源

- [IDM-VTON 原始项目](https://github.com/yisol/IDM-VTON)
- [HuggingFace 模型](https://huggingface.co/yisol/IDM-VTON)
- [ComfyUI-IDM-VTON](https://github.com/TemryL/ComfyUI-IDM-VTON)

## 无GPU方案

### 方案1: WeShopAI Virtual Try-On（⭐ 推荐首选）

**实测可用**（2025-04-19 验证），510+ likes，通过 gradio_client 调用。

**特点**：
- 免费使用，无需本地 GPU
- API 稳定，响应时间约 30-60 秒
- 不需要 HuggingFace API Token
- 目前可用性最高的免费方案

**使用方式**：

```python
import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7897'  # 需要代理
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7897'

from gradio_client import Client, handle_file

client = Client("WeShopAI/WeShopAI-Virtual-Try-On", verbose=False)

# main_image = 人物图, background_image = 服装图
result = client.predict(
    main_image=handle_file("/path/to/person.jpg"),
    background_image=handle_file("/path/to/garment.jpg"),
    api_name="/generate_image"
)

# 保存结果
import shutil
shutil.copy(result['path'], "/path/to/output.png")
```

**注意事项**：
- 需要设置代理访问 HuggingFace
- 网络不稳定时可能需要重试
- 输入参数：`main_image` 是人物图，`background_image` 是服装图

### 方案2: Kolors Virtual Try-On API

快手开源的虚拟换装模型，通过 HuggingFace Space 提供免费 API，无需本地 GPU。

**特点**：
- 10,040+ likes，效果优秀
- 免费使用，有速率限制
- 处理时间约 40-60 秒/张（实测约55秒）
- 输出格式：WebP
- ⚠️ 经常显示硬件不足

**API 调用方式**：

```python
import requests
import json
import time
import sseclient
from PIL import Image
import io

BASE_URL = "https://kwai-kolors-kolors-virtual-try-on.hf.space"

def virtual_tryon(person_image: bytes, garment_image: bytes, seed: int = 0, random_seed: bool = True) -> dict:
    """
    执行虚拟试衣
    
    Args:
        person_image: 人物图片的字节数据
        garment_image: 服装图片的字节数据
        seed: 随机种子
        random_seed: 是否使用随机种子
        
    Returns:
        dict: 包含结果图片 URL 和处理信息
    """
    
    # 1. 上传图片
    upload_url = f"{BASE_URL}/upload"
    resp = requests.post(upload_url, files={'files': ('person.png', person_image, 'image/png')}, timeout=60)
    person_path = resp.json()[0]
    
    resp = requests.post(upload_url, files={'files': ('garment.png', garment_image, 'image/png')}, timeout=60)
    garment_path = resp.json()[0]
    
    # 2. 加入处理队列
    session_hash = f"session_{int(time.time() * 1000)}"
    event_id = f"event_{int(time.time() * 1000)}"
    
    queue_data = {
        "data": [
            {"path": person_path, "meta": {"_type": "gradio.FileData"}},
            {"path": garment_path, "meta": {"_type": "gradio.FileData"}},
            seed,
            random_seed
        ],
        "session_hash": session_hash,
        "event_id": event_id,
        "fn_index": 2,  # 主函数索引
        "trigger": "click",
        "component": 26  # Button 组件
    }
    
    resp = requests.post(f"{BASE_URL}/queue/join", json=queue_data, timeout=30)
    
    # 3. 通过 SSE 等待结果
    sse_url = f"{BASE_URL}/queue/data?session_hash={session_hash}"
    resp = requests.get(sse_url, stream=True, timeout=300)
    client = sseclient.SSEClient(resp)
    
    for event in client.events():
        data = json.loads(event.data)
        msg = data.get('msg', '')
        
        if msg == 'process_completed':
            output = data.get('output', {})
            result_data = output.get('data', [])
            if len(result_data) >= 3:
                return {
                    "success": True,
                    "image_url": result_data[0].get('url'),
                    "seed_used": result_data[1],
                    "message": result_data[2],
                    "duration": output.get('duration')
                }
        elif msg == 'error':
            return {"success": False, "message": data.get('error')}
    
    return {"success": False, "message": "Timeout"}

# 使用示例
with open("person.jpg", "rb") as f:
    person = f.read()
with open("garment.jpg", "rb") as f:
    garment = f.read()

result = virtual_tryon(person, garment)
if result['success']:
    # 下载结果
    resp = requests.get(result['image_url'], timeout=60)
    with open("output.webp", "wb") as f:
        f.write(resp.content)
```

**依赖安装**：
```bash
pip install requests sseclient-py pillow
```

**注意事项**：
- 网络需能访问 `*.hf.space` 域名（中国用户需代理，hf-mirror.com 无法替代 Gradio Space）
- 高峰期可能需要排队等待
- 图片建议尺寸：768×1024
- 代理设置示例：`export http_proxy=http://127.0.0.1:7897 https_proxy=http://127.0.0.1:7897`

### 方案3: Google Colab

使用 IlyaTsibulin/colab-tryon 在云端运行：

```bash
git clone https://github.com/IlyaTsibulin/colab-tryon.git
cd colab-tryon
```

### 方案4: CatVTON（轻量级本地）

需要 GPU，但显存要求较低：

```bash
git clone https://github.com/Pratyush-Basu/virtual-tryon-catvton.git
cd virtual-tryon-catvton
pip install torch torchvision diffusers transformers accelerate
python app.py --person person.jpg --cloth cloth.jpg
```

### 方案5: 在线服务

- [Kolors Virtual Try-On Demo](https://huggingface.co/spaces/Kwai-Kolors/Kolors-Virtual-Try-On) - 免费，高峰期经常硬件不足
- [WeShopAI Virtual Try-On](https://huggingface.co/spaces/WeShopAI/WeShopAI-Virtual-Try-On) - **⭐ 推荐**，实测稳定可用
- [IDM-VTON Demo](https://huggingface.co/spaces/yisol/IDM-VTON) - 免费
- [CatVTON](https://huggingface.co/spaces/zhengchong/CatVTON) - 经常无硬件资源
- [Fashn.ai](https://www.fashn.ai) - 免费试用，商业级质量
- [Replicate](https://replicate.com) - 付费 API

## 常见错误与解决方案

### 1. HuggingFace Space 硬件不足

```
Runtime error: Scheduling failure: not enough hardware capacity
```

**原因**：免费 GPU 资源有限，高峰期经常不可用

**解决**：
- 等待低峰期（北京时间凌晨）使用
- 或使用 Fashn.ai 等商业服务
- 或升级 HuggingFace Pro 账户

### 2. API 调用 413 错误

```
{"error": "request entity too large"}
```

**原因**：图片文件超过 API 限制

**解决**：压缩图片
```python
from PIL import Image

def compress_image(input_path, output_path, max_size=1024, quality=85):
    img = Image.open(input_path)
    if max(img.size) > max_size:
        ratio = max_size / max(img.size)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)
    img.save(output_path, quality=quality, optimize=True)
```

### 3. SSL 证书验证失败

```
SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
httpcore.ConnectError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol
```

**原因**：代理环境导致 SSL 验证问题（常见于 Clash 等代理工具）

**解决方案**：

```python
# 方案1：设置代理环境变量（推荐）
import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7897'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7897'

# 方案2：禁用 urllib3 警告
import urllib3
urllib3.disable_warnings()

# 方案3：为 httpx 单独配置（gradio_client 使用 httpx）
import httpx
httpx._config._DEFAULT_TIMEOUT_CONFIG = httpx.Timeout(120.0)

# 方案4：重试逻辑（最实用）
import time
for attempt in range(5):
    try:
        client = Client("WeShopAI/WeShopAI-Virtual-Try-On", verbose=False)
        result = client.predict(...)
        break
    except Exception:
        time.sleep(2)

# 方案5：切换代理模式
# Clash: 规则模式 → 全局模式，或更换代理节点
```

**实测有效的组合**：
```python
import os
import urllib3
urllib3.disable_warnings()

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7897'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7897'

from gradio_client import Client, handle_file

client = Client("WeShopAI/WeShopAI-Virtual-Try-On", verbose=False)
result = client.predict(
    main_image=handle_file(garment_img),
    background_image=handle_file(person_img),
    api_name="/generate_image"
)
```

### 4. 浏览器访问超时

**原因**：HuggingFace Space 加载慢，需要下载模型

**解决**：
- 增加超时时间到 120-180 秒
- 或直接使用 API 方式调用

### CPU 推理（不推荐）

本地 CPU 推理极慢（几小时/张），建议使用上述云端方案。

## 注意事项

- 仅供学习和研究使用
- 遵守原始项目的 CC BY-NC-SA 4.0 许可证
- 生成结果仅限个人使用，不要用于商业目的

## 实战经验

## 国内加速说明

**⚠️ 无国内镜像方案**：HuggingFace Gradio Space 的 API 无法通过 hf-mirror.com 加速，必须使用代理访问。

**视觉模型性价比对比**（2025-04-19 实测）：

| 模型 | 输入价格 | 输出价格 | 性价比 |
|------|---------|---------|--------|
| qwen-vl-plus | 0.0008元/千tokens | 0.0008元/千tokens | ⭐⭐⭐⭐⭐ 最便宜 |
| doubao-vision | 0.003元/千tokens | 0.006元/千tokens | ⭐⭐⭐⭐ |
| hunyuan-vision | 0.008元/千tokens | 0.008元/千tokens | ⭐⭐⭐ |
| qwen-vl-max | 0.02元/千tokens | 0.02元/千tokens | ⭐⭐ 最强但贵 |

**API 响应速度对比**（2025-04-19 实测）：
| API | 响应时间 | 处理时间 | 推荐度 |
|-----|---------|---------|--------|
| WeShopAI | ~1.3s | 30-60s | ⭐⭐⭐ 推荐 |
| IDM-VTON | ~1.5s | 40-60s | ⭐⭐ |
| Kolors | ~6s | 40-60s | ⭐ |

**处理时间主要消耗在模型推理**（30-60秒），网络传输占比较小，优化代理对整体速度提升有限。

### 多角度服装合并（推荐）
当有多张不同角度的服装照片时，先合并再换装效果更好：

**命令行方式**：
```bash
python ~/.hermes/skills/image-processing/virtual-try-on/scripts/combine_garments.py \
  img1.jpg img2.jpg -o combined.png
```

**代码方式**：
from PIL import Image

def combine_garment_images(img_paths, output_path, direction='horizontal'):
    """合并多张服装图片"""
    images = [Image.open(p) for p in img_paths]
    
    if direction == 'horizontal':
        # 并排拼接
        target_height = min(img.height for img in images)
        resized = []
        total_width = 0
        for img in images:
            ratio = target_height / img.height
            new_w = int(img.width * ratio)
            resized.append(img.resize((new_w, target_height), Image.LANCZOS))
            total_width += new_w
        combined = Image.new('RGB', (total_width, target_height))
        x = 0
        for img in resized:
            combined.paste(img, (x, 0))
            x += img.width
    
    combined.save(output_path, quality=95)
    return output_path

# 使用示例
combine_garment_images(
    ["/path/to/garment_angle1.jpg", "/path/to/garment_angle2.jpg"],
    "/path/to/garment_combined.png"
)
```

### 参数说明（易混淆）⚠️ 实测修正
WeShopAI 的参数名称与实际功能**相反**：
- `main_image`: **服装图片** - 要穿的服装
- `background_image`: **人物照片** - 需要换装的人

**实测验证**（2025-04-19）：要让图一的人穿上图二的白色连衣裙，需要：
- main_image = 图二（服装）
- background_image = 图一（人物）

### 网络不稳定处理
HuggingFace Space 连接可能超时或断开，建议添加重试逻辑：

```python
import time

for attempt in range(3):
    try:
        client = Client("WeShopAI/WeShopAI-Virtual-Try-On", verbose=False)
        result = client.predict(
            main_image=handle_file(person_img),
            background_image=handle_file(garment_img),
            api_name="/generate_image"
        )
        break
    except Exception as e:
        print(f"尝试 {attempt+1}/3 失败")
        if attempt < 2:
            time.sleep(5)
```

### 代理配置（国内用户）
```python
import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7897'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7897'
```