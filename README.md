# OpenClash 订阅转换模板（Aethersailor Full · 60 组）

给 [subconverter](https://github.com/tindy2013/subconverter) 用的**外部配置模板**（对应转换接口的 `config=` 参数），供 OpenClash 做订阅转换时调用。

只定义**策略组**和**分流规则**，不含节点、订阅地址或 token，因此可以公开托管，给任意机场的任意订阅复用。

**两份文件，按需选一个**：

| 版本 | 地址 | 说明 |
|---|---|---|
| 跟随上游（推荐） | `https://cdn.jsdelivr.net/gh/cartoonsh/openclash-ini-template@heads/main/openclash-aethersailor-full.ini` | 远程规则集跟着上游更新 |
| 规则锁定版 | `https://cdn.jsdelivr.net/gh/cartoonsh/openclash-ini-template@heads/main/openclash-aethersailor-full-pinned.ini` | 规则集固定到某个上游提交，内容不再变化 |

两份只差 6 行规则集 URL（锁定版另有 7 行说明注释），业务逻辑完全一样。拿不定就用第一个。

---

## 一、30 秒用法

1. 复制上面那行 jsDelivr 地址
2. OpenClash → 配置订阅 → 编辑（或新增）订阅
3. 「订阅转换」保持开启
4. 「模板名称」选 **自定义**（Custom Template）
5. 在「自定义模板地址」里粘贴地址
6. 保存 → 应用 → 更新订阅

之后每次订阅更新都会按这个模板重新生成配置，不需要手动转换。

---

## 二、这个文件是什么

**Aethersailor 官方 `Custom_Clash_Full.ini` 的自动化衍生版**，由同目录的 `build.py` 生成，相对官方有四处调整。

已在 OpenClash + mihomo 内核上实机验证：60 组正常加载，63 条规则生效，两个新增组工作正常。

| 项目 | 值 |
|---|---|
| 上游来源 | [Aethersailor/Custom_OpenClash_Rules](https://github.com/Aethersailor/Custom_OpenClash_Rules) 的 `Custom_Clash_Full.ini` |
| 策略组 | 60 个 |
| 规则行 | 63 条 `ruleset=`（官方上限 64） |
| 转换输出 | 63 条规则 + 6 个 rule-providers |
| 文件大小 | 41,420 字节（锁定版 42,191 字节） |

### 相对官方的四处调整

1. **合并国外 AI 组**：官方把 ChatGPT / Copilot / Claude / Gemini / Grok 各拆一个组，这里并入 `🤖 国外AI服务`，5 条对应规则（`openai`、`bing`、`anthropic`、`google-gemini`、`xai`）一并改指。`🤖 国内AI服务` 不动。
2. **提示节点单独成组**：机场塞进订阅的套餐信息节点（`剩余流量：…`、`套餐到期：…`、`[重要提示]…`）收进 `ℹ️ 订阅信息`，不再删除——删了面板里就看不到流量和到期时间。
3. **其余分组排除这些节点**：其余 55 处按名字挑节点的正则统一加上「名字里不含提示关键词」的前缀，避免 `香港-剩余IP优化` 进香港组、`到期日…` 里的「日」命中日本组。
4. **新增 `💰 省流自动`**：`url-test` 组，只在**倍率低于 2x** 的节点里挑最快的（名字没写倍率按 1x 算），放在 `🚀 手动选择` 里紧跟 `♻️ 自动选择`。

### 包含 / 不包含

| 内容 | 是否包含 |
|---|---|
| 60 个策略组定义（类型、测速地址、间隔） | 包含 |
| 节点名匹配正则（如 `港\|HK\|Hong Kong`） | 包含 |
| 63 条分流规则 | 包含 |
| 节点（服务器、端口、密码） | **不包含** |
| 订阅地址 / token | **不包含** |
| DNS 设置 | **不包含** |

不含节点不是刻意删的，是文件类型决定的：subconverter 的 `config=` 只是一份「配方」，节点由转换器从你填的订阅地址实时取。也正因为如此，它可以公开。

---

## 三、60 个策略组

| 分类 | 组名（与模板逐字一致，可直接在面板里搜） |
|---|---|
| 手动 / 自动 | 🚀 手动选择、♻️ 自动选择、💰 省流自动 |
| 信息 | ℹ️ 订阅信息（不被任何规则引用，只用来显示） |
| 地区（15） | 🇭🇰 香港节点、🇺🇸 美国节点、🇯🇵 日本节点、🇸🇬 新加坡节点、🇼🇸 台湾节点、🇰🇷 韩国节点、🇨🇦 加拿大节点、🇬🇧 英国节点、🇫🇷 法国节点、🇩🇪 德国节点、🇳🇱 荷兰节点、🇹🇷 土耳其节点、🇷🇺 俄罗斯节点、🌐 其他地区、🏠 家宽节点 |
| 倍率 | 🐢 低倍率节点 |
| 通讯社交 | 📨 Telegram、🎧 Discord、📞 Talkatone、📹 Zoom、💬 即时通讯、🌐 社交媒体 |
| AI | 🤖 国外AI服务、🤖 国内AI服务 |
| 流媒体 | 📹 YouTube、🎥 Netflix、🎥 DisneyPlus、🎥 HBO、🎥 PrimeVideo、🎥 AppleTV+、🎥 Emby、🎻 Spotify、📺 Bahamut、🎶 TikTok |
| 开发 / 云服务 | 🚀 GitHub、📦 容器服务、💻 开发者服务、📚 学术资源、📢 谷歌FCM、🇬 谷歌服务、🍎 苹果服务、Ⓜ️ 微软服务、💾 OneDrive、💳 PayPal |
| 游戏 / 下载 | 🎮 游戏平台、🎮 Steam、⏬ PT站点、🚀 测速工具 |
| 其他 | 📰 新闻资讯、🛒 国外电商、🪙 加密货币、🌎 国外媒体、🌍 国外域名、🔀 非标端口、🎯 全球直连、🐟 漏网之鱼 |

几点说明：

- **18 个 `url-test`、42 个 `select`**。`url-test` 是 `♻️ 自动选择`、`💰 省流自动`、15 个地区/家宽组、`🐢 低倍率节点`；其余自己点。
- **`🚀 手动选择`** 末尾带全部节点（提示节点除外），地区正则一个都没匹配上时也不至于无处可选。
- **`📦 容器服务`**：GEOSITE `docker` + `category-container`，覆盖 Docker Hub、ghcr.io、Kubernetes 等镜像仓库。
- **`💻 开发者服务`**：GEOSITE `category-dev`，覆盖 GitHub、GitLab、Stack Overflow、npm、PyPI 等。
- **`🔀 非标端口`**：用 `DST-PORT` 把 1-79、81-442、444-65535 三段单独处理，方便 BT、游戏。
- **`🐢 低倍率节点`** 只匹配 `0.x` 小数倍率，`2x` 不会命中。
- **`🇼🇸 台湾节点`** 用的是萨摩亚国旗（上游如此）。

想让某个业务省流：在该业务组选 `🚀 手动选择`，再到 `🚀 手动选择` 里选 `💰 省流自动`。

---

## 四、分流规则

63 条 `ruleset=` 的构成：

| 类型 | 条数 | 说明 |
|---|---|---|
| `[]GEOSITE` | 49 | 引用 mihomo 内置 geosite，如 `telegram`、`netflix`、`category-ai-!cn` |
| `[]GEOIP` | 7 | 内置 geoip，含 `private`、`cn` 兜底 |
| `clash-domain:` 远程规则集 | 2 | `Custom_Direct_Domain.mrs`、`Custom_Proxy_Domain.mrs` |
| `clash-classic:` 远程规则集 | 4 | 自定义直连 IP、代理 IP、Steam CDN、非标端口 |
| `[]FINAL` | 1 | 兜底，指向 `🐟 漏网之鱼` |

6 个远程规则集在默认模式下保留为 `rule-providers`，由 mihomo 按 `interval` 自行刷新（1800 / 28800 秒），不占规则行数。

> ⚠️ **不要用 `expand=true`。** subconverter 不解析 `.mrs` 二进制，展开模式下两个 `clash-domain` 规则集会产出 0 条，等于上千条自定义直连域名**静默消失**，而且不报错。OpenClash 默认不带这个参数，别手动加。

---

## 五、已知限制

1. **必须用支持 `config=` 参数的转换后端。** OpenClash 默认的 `api.asailor.org`、`api.wcc.best` 都支持；只支持 `template=` 的后端不行。
2. **需要 mihomo（Meta）内核**，因为用了 `GEOSITE` / `GEOIP`。
3. **转换站要能访问 jsDelivr。** 部分转换站拉 `raw.githubusercontent.com` 会得到空内容或旧内容，不建议换成 raw 地址。
4. **仓库必须公开**，因为拉取模板的是境外转换站。
5. **63 条规则接近 64 条上限。** 官方注明兼容 `max_allowed_rulesets=64`，本模板留了 1 条余量，别再加远程规则集。
6. **提示节点按关键词认，会误判。** 真节点名字里带「剩余」「官网」「订阅」这类字样会被当成提示节点，只能看不能用；机场用了关键词表以外的说法则认不出来。要调整就改 `build.py` 里的 `INFO_RE`。
7. **省流组只看节点名里的倍率。** 名字不写倍率按 1x 算；机场只在网站上标倍率时分辨不出来。
8. **机场入口挂了，模板救不了。** 全部节点指向同一个不可达入口时，任何模板都无解。
9. **`clash_meta -t` 不能证明规则集能拉到。** 它不下载 `rule-providers`，URL 写错也能通过。要看运行日志里有没有 `[Provider] … pull error`。
10. **空组不会让配置加载失败。** 带 `use:` + `filter:` 的组即使筛选结果为 0，mihomo 也能启动，只是点进去是空的——这是静默的，不报错。反过来，既没有 `proxies:` 也没有 `use:` 的组会让 mihomo 直接拒载。

---

## 六、跟随上游 / 自己改

**跟上游**：上游更新后，在本目录跑：

```
python build.py
```

脚本只用 Python 自带模块，从上游下载原版、做完四处调整、生成两份文件，并在写文件前校验：AI 组确实删掉、规则确实改指、每个 `[]组名` 引用都有定义、规则不超过 64 条、两个新组都在且信息组未被引用、每个正则都能编译。任何一项不对就报「生成失败」且不写文件。

- 已下载好原版：`python build.py --upstream 原版.ini`
- 锁定版换提交：`python build.py --pin <提交sha> --pin-date <日期>`

**自己改**：不要直接改两份 ini，下次重跑会被覆盖。改 `build.py` 再重新生成。

改的时候注意：

- `enable_rule_generator=true` 必须保留（删了会得到 `rules: ~`，规则全空）
- `ruleset=` 之间的**先后顺序**会影响分流结果（先命中先赢），但 `ruleset=` 与 `custom_proxy_group=` 谁在前无所谓

jsDelivr 对分支地址最长缓存 12 小时，急用时用浏览器打开下面地址清缓存（返回 `"status": "finished"` 即可）：

```
https://purge.jsdelivr.net/gh/cartoonsh/openclash-ini-template@heads/main/openclash-aethersailor-full.ini
```

### 6 个远程规则集

| 文件 | 内容 | 刷新间隔 |
|---|---|---|
| `Custom_Direct_Domain.mrs` | 自定义直连域名 | 1800 秒 |
| `Custom_Direct_Classical_IP.yaml` | 自定义直连 IP | 28800 秒 |
| `Custom_Proxy_Domain.mrs` | 自定义代理域名 | 28800 秒 |
| `Custom_Proxy_Classical_IP.yaml` | 自定义代理 IP | 28800 秒 |
| `Steam_CDN_Classical.yaml` | Steam 下载 CDN | 28800 秒 |
| `Custom_Port_Direct.yaml` | 80/443 之外的端口 | 28800 秒 |

它们是 mihomo 在本地运行时自己拉的，不是转换器写进配置。拉取失败不会让服务挂掉：有缓存就继续用上一次的文件，没缓存则该规则集为空。

---

## 七、隐私

- 本文件不含订阅地址、token、节点 IP、节点密码。
- 文件名和仓库名不含机场名。
- ⚠️ **但订阅地址会交给转换站。** OpenClash 开启「订阅转换」后，会把订阅的完整地址（含 token）发给转换后端（默认 `api.asailor.org`），由它拉节点、套模板。这与用哪个模板无关。在意的话可以自建 subconverter，把转换后端换成本地地址。

---

## 致谢

- 模板与规则：[Aethersailor/Custom_OpenClash_Rules](https://github.com/Aethersailor/Custom_OpenClash_Rules)（基于 ACL4SSR 模板魔改）
- 转换器：[tindy2013/subconverter](https://github.com/tindy2013/subconverter)
- 规则集分发：[jsDelivr](https://www.jsdelivr.com/)
