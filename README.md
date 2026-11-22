# OpenClash 订阅转换外部模板（59 组）

这是一个给 [subconverter](https://github.com/tindy2013/subconverter) 用的**外部配置模板**（对应 `config=` 参数），供 OpenClash 做订阅转换时调用。

它只定义**策略组和规则**，不含节点、订阅地址、token 或任何个人信息，因此可以公开托管、给任意订阅复用。

## 这个文件包含什么、不包含什么

| 内容 | 是否包含 | 说明 |
|---|---|---|
| 策略组定义（59 组） | 包含 | 组名、类型（`select` / `url-test`）、测速地址与间隔 |
| 节点名匹配正则 | 包含 | 例如 `港|HK|Hong Kong`，用于把节点自动归入地区组 |
| 分流规则（99 条） | 包含 | `GEOSITE` / `GEOIP` / `DST-PORT` 等，全部内联，无 `rule-providers` |
| 伪节点过滤规则 | 包含 | `exclude_remarks`，剔除「到期 / 剩余 / 官网」这类流量信息节点 |
| 节点（服务器、端口、密码） | **不包含** | 由转换器在转换时从订阅地址注入 |
| 订阅地址 / token | **不包含** | 属于请求参数，不写进模板 |
| DNS 设置 | **不包含** | 由 OpenClash 在生成运行配置时注入 |

### 为什么不含节点

这不是刻意删掉的，而是**文件类型决定的**。

subconverter 的外部配置（`config=` 指向的 ini）只是「配方」：描述怎么分组、怎么分流。节点数据是「食材」，转换时从你填在订阅地址里的那条链接实时取。在 ini 里写 `proxies:` 也不会生效，因为它不是完整配置。

### 与其他配置文件的区别

| 文件 | 含节点 | 含分组 / 规则 | 用途 | 能否公开 |
|---|---|---|---|---|
| 本文件（subconverter ini） | 否 | 是 | 转换时的模板 | 可以 |
| 完整 Clash YAML | 是（`proxies:`） | 是 | 直接给 mihomo 运行 | 不可以（含节点密码） |
| proxy-provider YAML | 否（远程引用） | 否 | 只提供节点列表 | 视情况 |
| 机场原始订阅 | 是 | 部分 | 待转换的原料 | 不可以（含 token） |

所以「其他文件都含节点」是因为它们分别是成品和原料；本文件是配方，按机制就用不到节点。反过来，本文件包含的是订阅里没有的东西——组定义、地区匹配正则、分流规则、伪节点过滤，这些是通用的，换任何订阅都能复用。

如果你需要「含节点」的成品，那是另一份文件（完整 Clash YAML），只能本地使用，**不能公开**。

## 文件

`openclash-59groups-inline.ini`

- 59 个策略组
- 99 条内联规则（`GEOSITE` / `GEOIP` / 端口规则），不使用 `rule-providers` 外链
- 通过 `exclude_remarks` 自动过滤机场的「流量信息伪节点」

推荐使用的 Raw 地址（jsDelivr，境外转换站和国内都能访问）：

```
https://cdn.jsdelivr.net/gh/cartoonsh/openclash-ini-template@main/openclash-59groups-inline.ini
```

GitHub 原始地址（`raw.githubusercontent.com`）实测部分转换站拉不到，不建议填这个。

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

1. 复制上面的 jsDelivr 地址
2. 打开 OpenClash → 配置订阅 → 添加或编辑订阅
3. 「订阅转换」保持开启
4. 「模板」填这个地址（若界面是下拉框，选「自定义」后填写）
5. 保存并应用

之后每次订阅更新，转换站都会按这个模板同步生成配置，不需要手动转换。

## 注意

- 仓库必须**公开**，因为拉取模板的是转换站（在境外）。
- 模板只决定分组和规则。节点是内联 `proxies:` 还是走 `proxy-providers`，由转换器决定，模板控制不了。
- 如果订阅本身的节点入口不可达，换任何模板都连不上，需要检查机场侧。
- 地区组按常见地区预置：如果你的订阅没有某地区节点，对应组会是空的，建议删掉该行，避免面板里出现点了没内容的选项。
- 规则使用 `GEOSITE` / `GEOIP`，需要 mihomo（Meta）内核支持。

## 修改

直接编辑 `openclash-59groups-inline.ini` 并提交，地址不变，OpenClash 下次更新订阅时自动生效（jsDelivr 有几分钟缓存）。

修改时注意两点，否则规则会变空：

- `enable_rule_generator=true` 必须保留
- 所有 `ruleset=` 行要写在 `custom_proxy_group=` 之前
