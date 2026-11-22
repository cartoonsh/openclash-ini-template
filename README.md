# OpenClash 订阅转换外部模板（59 组）

这是一个给 [subconverter](https://github.com/tindy2013/subconverter) 用的**外部配置模板**（对应 `config=` 参数），供 OpenClash 做订阅转换时调用。

它只定义**策略组和规则**，不包含任何节点、订阅地址、token 或个人信息，因此可以公开托管、给任意订阅复用。

## 文件

`openclash-59groups-inline.ini`

- 59 个策略组
- 99 条内联规则（`GEOSITE` / `GEOIP` / 端口规则），**不使用 `rule-providers` 外链**
- 通过 `exclude_remarks` 自动过滤机场的「流量信息伪节点」（到期时间、剩余流量之类）

Raw 地址：

```
https://raw.githubusercontent.com/cartoonsh/openclash-ini-template/main/openclash-59groups-inline.ini
```

## 策略组

| 分类 | 组名 |
|---|---|
| 手动 / 自动 | 🚀 手动选择、♻️ 自动选择 |
| 地区 | 🇭🇰 香港、🇺🇸 美国、🇯🇵 日本、🇸🇬 新加坡、🇼🇸 台湾、🇰🇷 韩国、🇬🇧 英国、🇫🇷 法国、🇩🇪 德国、🇳🇱 荷兰、🇷🇺 俄罗斯、🌐 其他地区 |
| 通讯社交 | 📨 Telegram、🎧 Discord、📞 Talkatone、💬 即时通讯、🌐 社交媒体 |
| AI | 🤖 ChatGPT、Copilot、Claude、Gemini、Grok、国外 AI、国内 AI |
| 流媒体 | 📹 YouTube、🎥 Netflix、Disney+、HBO、PrimeVideo、AppleTV+、Emby、🎻 Spotify、📺 Bahamut、🎶 TikTok |
| 开发 / 服务 | 🚀 GitHub、📦 容器服务、💻 开发者服务、📚 学术资源、📢 谷歌FCM、🇬 谷歌服务、🍎 苹果服务、Ⓜ️ 微软服务、💾 OneDrive、💳 PayPal |
| 游戏 / 下载 | 🎮 游戏平台、🎮 Steam、⏬ PT 站点、🚀 测速工具 |
| 其他 | 📰 新闻资讯、🛒 国外电商、🪙 加密货币、🌎 国外媒体、🌍 国外域名、🔀 非标端口、🎯 全球直连、🐟 漏网之鱼 |

其中 `🔀 非标端口` 用 `DST-PORT` 把 1-79、81-442、444-65535 三段单独分流，方便处理 BT、游戏等非 80/443 流量。

## 怎么用

1. 复制上面的 Raw 地址
2. 打开 OpenClash → 配置订阅 → 添加或编辑订阅
3. 「订阅转换」保持开启
4. 「模板」填这个 Raw 地址（若界面是下拉框，选「自定义」后填写）
5. 保存并应用

之后每次订阅更新，转换站都会按这个模板同步生成配置，不需要手动转换。

## 注意

- 仓库必须**公开**，因为拉取模板的是转换站（在境外）；本文件不含任何个人订阅信息。
- 模板只决定分组和规则。节点是内联 `proxies:` 还是走 `proxy-providers`，由转换器决定，模板控制不了。
- 如果订阅本身的节点入口不可达，换任何模板都连不上，需要检查机场侧。
- 地区组按常见地区预置：如果你的订阅没有某地区节点，对应组会是空的，建议删掉该行，避免面板里出现点了没内容的选项。
- 规则使用 `GEOSITE` / `GEOIP`，需要 mihomo（Meta）内核支持。

## 修改

直接编辑 `openclash-59groups-inline.ini` 并提交，Raw 地址不变，OpenClash 下次更新订阅时自动生效。
