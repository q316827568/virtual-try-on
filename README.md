# Virtual Try-On Skill

<div align="center">

👕 **虚拟换装** - AI 驱动的服装试穿技术

[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-Space-yellow)](https://huggingface.co/spaces/WeShopAI/WeShopAI-Virtual-Try-On)
[![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-blue)](LICENSE)

</div>

## 简介

虚拟换装（Virtual Try-On）是一项使用 AI 技术将服装图片合成到人物图像上的技术。本 Skill 提供了多种实现方案，无需本地 GPU 即可实现高质量的虚拟换装效果。

## ⭐ 推荐方案：WeShopAI Virtual Try-On

**实测可用**（2025-04-19 验证），目前最稳定的免费方案。

### 特点

- ✅ 免费使用，无需本地 GPU
- ✅ API 稳定，响应时间约 30-60 秒
- ✅ 不需要 HuggingFace API Token
- ✅ 效果自然，服装贴合度高

### 快速开始

```python
import os
from gradio_client import Client, handle_file

# 设置代理（国内用户）
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7897'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7897'

# 初始化客户端
client = Client("WeShopAI/WeShopAI-Virtual-Try-On", verbose=False)

# 执行虚拟换装
result = client.predict(
    main_image=handle_file("person.jpg"),        # 人物照片
    background_image=handle_file("garment.jpg"), # 服装图片
    api_name="/generate_image"
)

# 保存结果
import shutil
shutil.copy(result['path'], "output.png")
print("换装完成！")
```

### 依赖安装

```bash
pip install gradio_client
```

## 其他方案

| 方案 | 特点 | 状态 |
|------|------|------|
| WeShopAI | 免费、稳定、无需Token | ⭐ 推荐 |
| Kolors Virtual Try-On | 效果好、10K+ likes | ⚠️ 经常硬件不足 |
| IDM-VTON | 开源、可本地部署 | 需 16GB 显存 |
| CatVTON | 轻量级本地方案 | 需 GPU |
| Fashn.ai | 商业级质量 | 付费 |

## 使用场景

- 🛒 **电商试衣**：让用户在线试穿服装
- 👗 **时尚搭配**：探索不同服装搭配效果
- 🎨 **创意设计**：快速生成服装效果图
- 📱 **APP 集成**：集成到购物、社交应用

## 效果示例

| 人物图 | 服装图 | 换装结果 |
|--------|--------|----------|
| 人物照片 | 服装图片 | AI 合成效果 |

## 注意事项

1. **网络要求**：需要访问 HuggingFace（国内用户需代理）
2. **图片建议**：
   - 人物图：正面全身或半身照，背景简洁
   - 服装图：平铺或模特展示图，主体清晰
3. **处理时间**：约 30-60 秒/张
4. **使用限制**：仅供学习研究，请勿用于商业用途

## 故障排除

### 连接超时
```bash
# 检查代理
curl -x http://127.0.0.1:7897 https://huggingface.co
```

### SSL 错误
确保代理支持 HTTPS 流量

### 效果不理想
- 尝试换更清晰的人物/服装图片
- 人物图使用纯色背景效果更好

## 相关资源

- [WeShopAI Space](https://huggingface.co/spaces/WeShopAI/WeShopAI-Virtual-Try-On)
- [Kolors Virtual Try-On](https://huggingface.co/spaces/Kwai-Kolors/Kolors-Virtual-Try-On)
- [IDM-VTON GitHub](https://github.com/yisol/IDM-VTON)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目仅供学习研究使用。生成结果受原始模型许可证约束。

---

**Hermes Agent Skill** - 让 AI 更懂你的需求
