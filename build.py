#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
由上游官方 Full 模板自动生成本仓库的两份模板（只用 Python 自带模块）。

用法：
  python build.py                     # 从上游 main 下载原版后生成
  python build.py --upstream 原版.ini  # 用本地已下载的原版生成
  python build.py --pin <提交sha>      # 锁定版改锁到另一个上游提交

生成：
  openclash-aethersailor-full.ini         日常版（规则集跟随上游 @main）
  openclash-aethersailor-full-pinned.ini  锁定版（规则集锁定到 --pin 指定的提交）
"""
import argparse
import os
import re
import sys
import urllib.request

UPSTREAM_URL = ("https://raw.githubusercontent.com/Aethersailor/"
                "Custom_OpenClash_Rules/main/cfg/Custom_Clash_Full.ini")
DEFAULT_PIN = "b64d5ac1828495be49751d123daeffff36df1e51"

AI_GROUPS = ["🤖 ChatGPT", "🤖 Copilot", "🤖 Claude", "🤖 Gemini", "🤖 Grok"]
AI_TARGET = "🤖 国外AI服务"
AUTO_GROUP = "♻️ 自动选择"
SAVER_GROUP = "💰 省流自动"
INFO_GROUP = "ℹ️ 订阅信息"
MANUAL_GROUP = "🚀 手动选择"
LOW_GROUP = "🐢 低倍率节点"
TEST_URL = "https://www.gstatic.com/generate_204"
INTERVAL = "300,,50"

# 信息节点：名字里任何位置出现这些字样就算（机场塞进订阅的流量/到期/官网等提示）
INFO_RE = ("剩余|到期|过期|有效期|官网|网址|重置|套餐|订阅|公告|客服|重要提示|已用"
           "|流量[:：]|(?i:traffic|expire)")
# 倍率 >= 2 的写法：2x / 2.5X / 3倍 / 2ｘ / x2 / ×3 / 倍率:2 / 二倍 / 两倍
# 只认 2~99 倍；x 打头的写法要求 x 前面不是字母数字、x 和数字紧挨着，
# 这样「1x 2号」「Max2」「x25519」都不会被误认成高倍率
HIGH_RATE_RE = (r"(?<![\d.])(?:[2-9]|[1-9]\d)(?:\.\d+)?\s*(?:[xX×ｘＸ]|倍)"
                r"|(?<![A-Za-z\d.])[xX×ｘＸ](?:[2-9]|[1-9]\d)(?:\.\d+)?(?![\d.])"
                r"|倍率[:： ]*(?:[2-9]|[1-9]\d)(?![\d])"
                r"|[二两三四五六七八九十]倍")
NOT_INFO = "^(?!.*(?:%s))" % INFO_RE

SAVER_LINE = ("custom_proxy_group=%s`url-test`%s(?!.*(?:%s)).*`%s`%s"
              % (SAVER_GROUP, NOT_INFO, HIGH_RATE_RE, TEST_URL, INTERVAL))
INFO_LINE = "custom_proxy_group=%s`select`(?:%s)" % (INFO_GROUP, INFO_RE)

HEADER = """
;===== 本文件由 build.py 从上游官方 Full 模板自动生成，请勿手改 =====
"""

PIN_HEADER = """;===== 规则集锁定版：{n} 个远程规则集锁定到固定提交，内容不再变化 =====
;重新锁定：python build.py --pin <提交sha>
"""


def fail(msg):
    sys.exit("生成失败：" + msg)


def is_regex_field(f):
    return not (f.startswith("[]") or f.startswith("http")
                or re.fullmatch(r"\d*(,\d*)*", f))


def guard(f):
    """给一个节点名正则加上“排除信息节点”的前缀。"""
    if f == ".*":
        return NOT_INFO + ".*"
    return NOT_INFO + ".*(?:" + f + ")"


def transform(text):
    lines = text.split("\n")
    out = []
    seen_custom = removed = remapped = guarded = 0
    for line in lines:
        if line.startswith("custom_proxy_group="):
            name = line[len("custom_proxy_group="):].split("`", 1)[0]
            if name in AI_GROUPS:
                removed += 1
                continue
            fields = line.split("`")
            for i in range(2, len(fields)):
                if is_regex_field(fields[i]):
                    fields[i] = guard(fields[i])
                    guarded += 1
            if name == MANUAL_GROUP:
                if "[]" + AUTO_GROUP not in fields:
                    fail("%s 里没找到 []%s，上游可能改了结构" % (MANUAL_GROUP, AUTO_GROUP))
                idx = fields.index("[]" + AUTO_GROUP)
                fields.insert(idx + 1, "[]" + SAVER_GROUP)
            line = "`".join(fields)
            out.append(line)
            if name == AUTO_GROUP:
                out.append(SAVER_LINE)
            if name == LOW_GROUP:
                out.append(INFO_LINE)
            continue
        if line.startswith("ruleset="):
            target = line[len("ruleset="):].split(",", 1)[0]
            if target in AI_GROUPS:
                line = "ruleset=" + AI_TARGET + line[len("ruleset=") + len(target):]
                remapped += 1
        out.append(line)
        if line.strip() == "[custom]" and not seen_custom:
            seen_custom = 1
            out.extend(HEADER.rstrip("\n").split("\n") + [""])
    if not seen_custom:
        fail("上游文件里没找到 [custom]")
    if removed != 5 or remapped != 5:
        fail("AI 组删除 %d 个、规则改指 %d 条，应各为 5，上游可能改了结构" % (removed, remapped))
    return "\n".join(out).rstrip("\n") + "\n", guarded


def pin(text, sha):
    pat = "Aethersailor/Custom_OpenClash_Rules@main/"
    n = sum(1 for l in text.split("\n") if l.startswith("ruleset=") and pat in l)
    body = "\n".join(l.replace(pat, "Aethersailor/Custom_OpenClash_Rules@%s/" % sha)
                     if l.startswith("ruleset=") else l for l in text.split("\n"))
    return PIN_HEADER.format(n=n) + body, n


def check(text):
    groups, types, refs = [], {}, []
    rules = []
    for line in text.split("\n"):
        if line.startswith("custom_proxy_group="):
            f = line[len("custom_proxy_group="):].split("`")
            groups.append(f[0])
            types[f[0]] = f[1]
            refs += [(f[0], x[2:]) for x in f[2:] if x.startswith("[]")]
            for x in f[2:]:
                if is_regex_field(x):
                    re.compile(x)
        elif line.startswith("ruleset="):
            rules.append(line[len("ruleset="):].split(",", 1)[0])
    builtin = {"DIRECT", "REJECT"}
    if len(set(groups)) != len(groups):
        fail("有重名分组")
    for g, r in refs:
        if r not in groups and r not in builtin:
            fail("分组 %s 引用了不存在的 %s" % (g, r))
    for r in rules:
        if r not in groups:
            fail("规则指向了不存在的分组 %s" % r)
    if len(rules) > 64:
        fail("规则 %d 条，超过上限 64" % len(rules))
    for g in (INFO_GROUP, SAVER_GROUP, AUTO_GROUP, MANUAL_GROUP):
        if g not in groups:
            fail("缺少分组 %s，上游可能改了结构" % g)
    if ("[]" + SAVER_GROUP) not in text:
        fail("%s 没被放进 %s" % (SAVER_GROUP, MANUAL_GROUP))
    if INFO_GROUP in rules or any(r == INFO_GROUP for _, r in refs):
        fail("信息组被引用了，它应该不被任何地方调用")
    ut = sum(1 for t in types.values() if t == "url-test")
    return len(groups), ut, len(groups) - ut, len(rules)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--upstream", help="本地上游原版文件；不填就从上游 main 下载")
    ap.add_argument("--pin", default=DEFAULT_PIN, help="锁定版锁到的上游提交 sha")
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    a = ap.parse_args()
    if a.upstream:
        with open(a.upstream, "rb") as fh:
            raw = fh.read()
    else:
        with urllib.request.urlopen(UPSTREAM_URL, timeout=30) as r:
            raw = r.read()
    src = raw.decode("utf-8").replace("\r\n", "\n")
    full, guarded = transform(src)
    pinned, n = pin(full, a.pin)
    stats = check(full)
    check(pinned)
    for fn, data in (("openclash-aethersailor-full.ini", full),
                     ("openclash-aethersailor-full-pinned.ini", pinned)):
        with open(os.path.join(a.out, fn), "wb") as fh:
            fh.write(data.encode("utf-8"))
        print("%s  %d 字节" % (fn, len(data.encode("utf-8"))))
    print("分组 %d 个（url-test %d，select %d），规则 %d 条；加排除的正则 %d 处；锁定 URL %d 行"
          % (stats + (guarded, n)))


if __name__ == "__main__":
    main()
