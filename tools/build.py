# -*- coding: utf-8 -*-
"""由 tools/curriculum.py 生成全套学习包文件。运行：python tools/build.py"""
import csv
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from curriculum import CURRICULUM, SETTINGS, RULES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def w(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("written:", path)


def w_csv(path, rows):
    buf = io.StringIO(newline="")
    writer = csv.writer(buf)
    writer.writerows(rows)
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8-sig", newline="") as f:
        f.write(buf.getvalue())
    print("written:", path)


def slug(lesson):
    return "%02d-%s" % (lesson["id"], lesson["title"].replace("：", "-").replace(" ", ""))


# ---------------------------------------------------------------- 数据文件
w("curriculum.json", json.dumps(
    {"settings": SETTINGS, "rules": RULES, "lessons": CURRICULUM},
    ensure_ascii=False, indent=2) + "\n")


# ---------------------------------------------------------------- 逐讲教案
for L in CURRICULUM:
    lines = []
    a = lines.append
    a("# 第 %d 讲 %s" % (L["id"], L["title"]))
    a("")
    a("| 项目 | 内容 |")
    a("| --- | --- |")
    a("| 周次 | %s |" % L["week"])
    a("| 单元 | %s |" % L["unit"])
    a("| 本周目标 | %s |" % L["goal"])
    a("| 达标标准 | %s |" % L["standard"])
    a("| 建议安排 | 每周 2 次，每次 20 分钟；第 1 次看讲解与例题，第 2 次做练习与打卡 |")
    a("")
    a("## 1. 情境引入（讲给孩子听）")
    a("")
    a(L["story"])
    a("")
    a("## 2. 方法口诀")
    a("")
    a("> **%s**" % L["slogan"])
    a("")
    for i, m in enumerate(L["method"], 1):
        a("%d. %s" % (i, m))
    a("")
    a("## 3. 例题（家长带着读，先让孩子说思路）")
    a("")
    for i, e in enumerate(L["examples"], 1):
        a("**例 %d** %s" % (i, e["q"]))
        a("")
        for s in e["steps"]:
            a("- %s" % s)
        a("")
        a("**答：%s**" % e["answer"])
        a("")
    a("## 4. 课堂练习（5 题，独立完成）")
    a("")
    a("| # | 题目 | 选项 | 正确答案 | 解析 |")
    a("| --- | --- | --- | --- | --- |")
    for i, e in enumerate(L["exercises"], 1):
        a("| %d | %s | %s | %s | %s |" % (
            i, e["q"], " / ".join(e["options"]),
            e["options"][e["answer"]], e["why"]))
    a("")
    a("## 5. 易错提醒")
    a("")
    a(L["mistake"])
    a("")
    a("## 6. 家长陪伴提示（只提问，不讲公式）")
    a("")
    for i, p in enumerate(L["parent"], 1):
        a("%d. %s" % (i, p))
    a("")
    a("## 7. 达标与记录")
    a("")
    a("- 达标：%s" % RULES["pass"])
    a("- 需订正：%s" % RULES["review"])
    a("- 需复学：%s" % RULES["redo"])
    a("- 记录：在 `progress/学习计划与进度表.csv` 填本讲得分、自评星级与错题数；在网页「打卡」页保存进度。")
    a("")
    a("## 8. 卡通讲解视频分镜脚本")
    a("")
    a("画面统一为「%s」风格的 %s 与 %s。画面不出现具体算式，算式与讲解词由网页动画课堂和本教案承载，避免字幕出错。" % (
        SETTINGS["place"], SETTINGS["hero"], SETTINGS["partner"]))
    a("")
    a("| 时间 | 画面 | 台词 |")
    a("| --- | --- | --- |")
    for s in L["scenes"]:
        a("| %s | %s | %s |" % (s["t"], s["pic"], s["line"]))
    a("")
    a("## 9. 网页动画课堂台词（逐帧）")
    a("")
    for i, s in enumerate(L["anim"], 1):
        a("%d. %s" % (i, s))
    a("")
    w("lessons/%s.md" % slug(L), "\n".join(lines) + "\n")


# ---------------------------------------------------------------- README
readme = []
r = readme.append
r("# %s" % SETTINGS["title"])
r("")
r("面向 %s。16 周、16 讲，每周 2 次、每次 20 分钟。每讲包含：教案、卡通讲解（网页动画课堂，可叠加 MP4 短片）、3 道例题、5 道练习与解析、达标标准、进度记录与家长反馈。" % SETTINGS["audience"])
r("")
r("**起始日期：待填。** 下表用相对周次，不预设日历日期；确定开课日期后填入 `progress/学习计划与进度表.csv` 的「起始日期」列。")
r("")
r("## 1. 目录结构与用法")
r("")
r("| 路径 | 内容 |")
r("| --- | --- |")
r("| `README.md` | 16 周计划、达标规则、进度与反馈办法 |")
r("| `curriculum.json` | 全部课程数据，改内容改这里再运行 `python tools/build.py` |")
r("| `lessons/` | 16 份逐讲教案（含例题、练习、解析、分镜脚本、家长提示） |")
r("| `site/index.html` | 学习中心：卡通动画讲解、练习判分、错题本、打卡积分、家长周反馈 |")
r("| `videos/` | 卡通讲解 MP4 短片与分镜说明 |")
r("| `progress/` | 学习计划与进度表、家长反馈记录、填写说明 |")
r("| `.github/ISSUE_TEMPLATE/` | 进度打卡、周反馈、错题求助三类 Issue 模板 |")
r("| `tools/` | 课程数据与生成脚本 |")
r("")
r("**最快开始**：双击打开 `site/index.html`（无需联网、无需安装）。进度保存在浏览器本地，可导出 JSON 备份。")
r("")
r("**在线版**：https://jyotikujur002-collab.github.io/grade2-math-olympiad/ （GitHub Pages，免登录，手机/平板可开）。仓库：https://github.com/jyotikujur002-collab/grade2-math-olympiad （公开）。在线版与本地版的进度各自存在本机浏览器，不互通；换设备用网页里的「导出进度 / 导入进度」。")
r("")
r("## 2. 16 周学习计划（详细）")
r("")
r("| 周次 | 讲次 | 主题 | 单元 | 本周目标 | 达标标准 | 教案 |")
r("| --- | --- | --- | --- | --- | --- | --- |")
for L in CURRICULUM:
    r("| %s | 第 %d 讲 | %s | %s | %s | %s | [教案](lessons/%s.md) |" % (
        L["week"], L["id"], L["title"], L["unit"], L["goal"], L["standard"], slug(L)))
r("")
r("### 每周固定节奏")
r("")
r("| 时段 | 做什么 | 时长 | 产出 |")
r("| --- | --- | --- | --- |")
r("| 第 1 次 | 看卡通讲解（动画课堂 + 单元 MP4 短片）→ 读情境 → 一起说口诀 | 8 分钟 | 能复述口诀 |")
r("| 第 1 次 | 3 道例题，家长只提问不代算 | 12 分钟 | 能说出思路 |")
r("| 第 2 次 | 独立完成 5 道练习，网页自动判分并记错题 | 10 分钟 | 练习得分 |")
r("| 第 2 次 | 订正错题 → 自评星级 → 打卡领积分 | 6 分钟 | 进度表一行 |")
r("| 周末 | 家长填一次周反馈，按规则决定是否复学 | 4 分钟 | 周反馈一条 |")
r("")
r("## 3. 达标、积分与徽章")
r("")
r("| 情况 | 处理 |")
r("| --- | --- |")
r("| 达标 | %s |" % RULES["pass"])
r("| 做对 3 题 | %s |" % RULES["review"])
r("| 做对 ≤2 题 | %s |" % RULES["redo"])
r("")
r("积分规则：")
r("")
for p in RULES["points"]:
    r("- %s" % p)
r("")
r("徽章：")
r("")
for b in RULES["badges"]:
    r("- %s" % b)
r("")
r("> 连续 2 周未达标，不要往下推进；把该讲的例题重讲一遍，并换一组同类型口头题，确认方法真的会用了再继续。")
r("")
r("## 4. 进度管理（三处同步，任选其一也能跑通）")
r("")
r("1. **网页自动**：练习判分、打卡、积分、错题本、周反馈全部存在浏览器 `localStorage`，首页「导出进度」生成 JSON，换设备时「导入进度」还原。")
r("2. **表格人工**：`progress/学习计划与进度表.csv` 每讲一行，填完成状态、得分、星级、错题数、达标状态；`progress/家长反馈记录.csv` 每周一行。")
r("3. **GitHub 协作**：用 `.github/ISSUE_TEMPLATE/` 里的三类模板开 Issue；建议建一个 Projects 看板，列设为 `待学 / 学习中 / 已达标 / 需复学`，每讲一张卡片，讲完拖动。")
r("")
r("进度状态取值统一为：`待学`、`学习中`、`已达标`、`需复学`。")
r("")
r("## 5. 反馈机制")
r("")
r("| 层级 | 谁填 | 什么时候 | 内容 |")
r("| --- | --- | --- | --- |")
r("| 课后自评 | 孩子 | 每讲练习后 | 三星：我懂了 / 有点难 / 没听懂；点星星即记录 |")
r("| 错题本 | 网页自动 + 孩子订正 | 每讲练习后 | 错题干、正确答案、是否已订正 |")
r("| 家长周反馈 | 家长 | 每周末 | 卡在哪一题、最有成就感的一题、下周调整 |")
r("| 单元复盘 | 家长 | 第 4/8/12/16 周末 | 4 讲达标情况、是否需要补讲、徽章是否解锁 |")
r("| 求助 Issue | 家长 | 随时 | 贴错题、孩子当时的想法，便于针对性讲解 |")
r("")
r("反馈如何改变计划：")
r("")
r("- 家长反馈「卡在某一类题」→ 下一周第 1 次课用 5 分钟重看该讲动画课堂，不新增内容。")
r("- 连续 3 周全部达标且自评三星 → 可把每周 2 次压缩为 1 次，腾出时间做本讲的「变式题」（把例题数字换掉重做）。")
r("- 自评连续 2 次「没听懂」→ 暂停新讲，回到该单元第 1 讲重学。")
r("")
r("## 6. 卡通讲解说明")
r("")
r("- **动画课堂**：网页内置 SVG 卡通角色（%s、%s），每讲 4-5 帧逐句讲解，可播放 / 暂停 / 上一句 / 重播。算式与讲解词由课程数据驱动，内容可控。" % (SETTINGS["hero"], SETTINGS["partner"]))
r("- **MP4 短片**：本次视频生成调用未获授权，`videos/` 下暂无 mp4 文件。网页会按 `unitN-opening.mp4` 自动尝试读取，找不到即回退到动画课堂，学习流程不受影响；分镜脚本与生成提示词已齐备，补齐文件后即可播放。")
r("- **分镜脚本**：16 讲全部分镜写在各讲教案第 8 节，并汇总在 `videos/README.md`，可按同一模板继续生成其余讲次的 MP4。")
r("- 设计原则：AI 生成的视频画面不承载具体算式与数字，避免出现错字错数；知识点、算式、解析一律以教案和网页动画课堂为准。")
r("")
r("## 7. 内容维护")
r("")
r("```bash")
r("python tools/build.py   # 改完 tools/curriculum.py 后重新生成教案、网页、进度表")
r("```")
r("")
r("## 8. 复核提示")
r("")
r("- 题目与答案已逐题核对，但用于正式教学、对外分享或评价性表述前，请家长/任课老师再复核一遍。")
r("- 计划起始日期、孩子实际年级与已学内容（是否学过表内除法）需按实际情况确认后填写。")
r("- 视频文件为生成式内容，画面细节与教学无关，使用前请预览确认适合儿童观看。")
r("")
w("README.md", "\n".join(readme) + "\n")


# ---------------------------------------------------------------- 进度表
rows = [["周次", "讲次", "主题", "单元", "起始日期(待填)", "第1次完成", "第2次完成",
         "练习得分(0-5)", "自评星级(1-3)", "错题数", "达标状态", "家长反馈要点", "复盘日期"]]
for L in CURRICULUM:
    rows.append([L["week"], "第 %d 讲" % L["id"], L["title"], L["unit"],
                 "待填", "未", "未", "", "", "", "待学", "", ""])
w_csv("progress/学习计划与进度表.csv", rows)

rows2 = [["周次", "日期(待填)", "本周完成的讲次", "卡住的题目", "最有成就感的一题",
          "孩子状态(懂了/有点难/没听懂)", "下周调整", "家长签字"]]
for L in CURRICULUM:
    rows2.append([L["week"], "待填", "第 %d 讲" % L["id"], "", "", "", "", ""])
w_csv("progress/家长反馈记录.csv", rows2)

w("progress/使用说明.md", "\n".join([
    "# 进度与反馈填写说明",
    "",
    "1. `学习计划与进度表.csv` 每讲一行。状态只用四个词：待学 / 学习中 / 已达标 / 需复学。",
    "2. 练习得分填 0-5；达标线 4 分。3 分订正后可标达标，2 分及以下标需复学。",
    "3. 自评星级由孩子在网页里点星星，家长把数字抄进表；1=没听懂，2=有点难，3=我懂了。",
    "4. `家长反馈记录.csv` 每周一行，三个必填：卡住的题目、最有成就感的一题、下周调整。",
    "5. 起始日期按实际开课日填写，本套材料不预设日历日期。",
    "6. 换设备或清空浏览器数据前，先在网页首页点「导出进度」保存 JSON。",
    "7. 两份 CSV 用 Excel / WPS 打开即可（已带 UTF-8 BOM）。",
    "",
]) + "\n")


# ---------------------------------------------------------------- 视频说明
v = []
v.append("# 卡通讲解视频说明")
v.append("")
v.append("主角：%s、%s；场景：%s。风格：明亮、圆润、低龄向 2D 卡通。" % (
    SETTINGS["hero"], SETTINGS["partner"], SETTINGS["place"]))
v.append("")
v.append("## 短片状态")
v.append("")
v.append("**本次未生成 MP4。** 视频生成调用未获授权，因此没有产生视频文件。网页在找不到 mp4 时会自动回退到内置动画课堂，学习流程不受影响。")
v.append("")
v.append("如需补齐：按下表命名把 5 秒短片放进本目录，网页会自动读取，无需改代码。16 讲分镜脚本与生成提示词见下文。")
v.append("")
v.append("| 计划文件名 | 对应单元 | 覆盖讲次 | 建议时长 | 当前状态 |")
v.append("| --- | --- | --- | --- | --- |")
unit_names = ["第一单元 计算巧算", "第二单元 规律与图形", "第三单元 应用题", "第四单元 逻辑与综合"]
for i, u in enumerate(unit_names, 1):
    ids = [L["id"] for L in CURRICULUM if L["unit"] == u]
    v.append("| `unit%d-opening.mp4` | %s | 第 %d-%d 讲 | 5 秒 | 待生成 |" % (
        i, u, min(ids), max(ids)))
v.append("")
v.append("> 视频文件为二进制，不在 GitHub 仓库的文本推送内容里。本地放在本目录即可被网页读取；如需在 GitHub Pages 上播放，请手动 `git add videos/*.mp4` 后提交，或作为 Release 附件上传并改网页里的视频路径。")
v.append("")
v.append("## 16 讲分镜脚本（可直接用于补生成其余讲次）")
v.append("")
for L in CURRICULUM:
    v.append("### 第 %d 讲 %s（%s）" % (L["id"], L["title"], L["unit"]))
    v.append("")
    v.append("| 时间 | 画面 | 台词 |")
    v.append("| --- | --- | --- |")
    for s in L["scenes"]:
        v.append("| %s | %s | %s |" % (s["t"], s["pic"], s["line"]))
    v.append("")
    v.append("配套动画课堂台词：%s" % " ／ ".join(L["anim"]))
    v.append("")
v.append("## 可复用生成提示词模板")
v.append("")
v.append("```text")
v.append("明亮低龄向 2D 卡通动画，16:9。圆润的小狐狸和方块小机器人在彩色数学森林里，")
v.append("柔和描边、扁平色块、缓慢运镜，角色动作简单可爱。画面不出现任何文字、数字或字幕。")
v.append("镜头内容：<把上表某一行的「画面」粘贴到这里>。时长 5 秒。")
v.append("```")
v.append("")
v.append("要求画面不出现文字与数字，是避免生成式视频把算式画错；具体算式与讲解由教案、网页动画课堂和家长口述承担。")
v.append("")
w("videos/README.md", "\n".join(v) + "\n")


# ---------------------------------------------------------------- Issue 模板
w(".github/ISSUE_TEMPLATE/progress-checkin.md", """---
name: 讲次进度打卡
about: 完成一讲后记录得分与达标状态
title: "[进度] 第 __ 讲"
labels: progress
---

- 讲次：第 __ 讲《______》
- 完成日期：待填
- 练习得分：__ / 5
- 自评星级：1 / 2 / 3（1=没听懂，2=有点难，3=我懂了）
- 错题数：__
- 达标状态：待学 / 学习中 / 已达标 / 需复学
- 孩子能复述的口诀：______

<!-- 达标线：4 分。3 分订正后达标，2 分及以下需复学。 -->
""")

w(".github/ISSUE_TEMPLATE/weekly-feedback.md", """---
name: 家长周反馈
about: 每周末填一次，用来调整下一周计划
title: "[周反馈] 第 __ 周"
labels: feedback
---

- 周次：第 __ 周
- 本周完成讲次：第 __ 讲
- 卡住的题目：______（写题号 + 孩子当时的想法）
- 最有成就感的一题：______
- 孩子状态：懂了 / 有点难 / 没听懂
- 下周调整：继续新讲 / 订正错题 / 重看动画 / 暂停复学

<!-- 调整规则：连续 2 周未达标不推进新讲；连续 3 周全达标可压缩为每周 1 次。 -->
""")

w(".github/ISSUE_TEMPLATE/wrong-question.md", """---
name: 错题求助
about: 一道题讲不通时，把孩子的想法记下来
title: "[错题] 第 __ 讲 第 __ 题"
labels: question
---

- 讲次 / 题号：第 __ 讲 第 __ 题
- 原题：______
- 孩子选的答案 / 写的算式：______
- 孩子当时的想法（原话）：______
- 家长已尝试的讲法：______

<!-- 优先记录「孩子怎么想的」，比只记正确答案更有助于下次讲清。 -->
""")

w(".gitignore", "__pycache__/\n*.pyc\n.DS_Store\n")


# ---------------------------------------------------------------- 网页学习中心
HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>二年级奥数·数学森林闯关</title>
<style>
:root{
  --bg:#f5f8fc; --card:#ffffff; --ink:#20304a; --muted:#6c7f99; --line:#e3eaf3;
  --orange:#ff7a59; --blue:#3b82f6; --green:#2bb673; --yellow:#ffc53d; --purple:#8b6cf0;
  --shadow:0 3px 14px rgba(32,48,74,.07);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"PingFang SC","Microsoft YaHei","Noto Sans CJK SC",system-ui,sans-serif;
  font-size:15px;line-height:1.7}
header{background:linear-gradient(120deg,#fff7f2,#eef5ff);border-bottom:1px solid var(--line);
  padding:18px 22px;position:sticky;top:0;z-index:20}
.hwrap{max-width:1180px;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;gap:14px}
h1{font-size:20px;margin:0;font-weight:800;letter-spacing:.5px}
.hsub{font-size:12px;color:var(--muted);margin-top:2px}
.stats{margin-left:auto;display:flex;gap:10px;flex-wrap:wrap}
.stat{background:#fff;border:1px solid var(--line);border-radius:12px;padding:6px 13px;text-align:center;min-width:78px}
.stat b{display:block;font-size:18px;line-height:1.2;color:var(--orange)}
.stat span{font-size:11px;color:var(--muted)}
.tools{display:flex;gap:8px;margin-left:auto}
button{font:inherit;cursor:pointer;border-radius:10px;border:1px solid var(--line);
  background:#fff;color:var(--ink);padding:6px 13px;transition:.15s}
button:hover{border-color:var(--blue);color:var(--blue)}
button.primary{background:var(--orange);border-color:var(--orange);color:#fff;font-weight:700}
button.primary:hover{filter:brightness(1.05);color:#fff}
button:disabled{opacity:.45;cursor:not-allowed}
main{max-width:1180px;margin:20px auto;padding:0 22px;display:grid;grid-template-columns:270px 1fr;gap:20px;align-items:start}
@media(max-width:860px){main{grid-template-columns:1fr}.tools{margin-left:0}.stats{margin-left:0}}
.panel{background:var(--card);border:1px solid var(--line);border-radius:16px;box-shadow:var(--shadow)}
.side{padding:14px;position:sticky;top:100px}
.side h2{font-size:13px;color:var(--muted);margin:14px 0 8px;font-weight:600;letter-spacing:1px}
.side h2:first-child{margin-top:0}
.lesson-btn{display:block;width:100%;text-align:left;border:1px solid transparent;background:transparent;
  padding:7px 10px;border-radius:10px;margin-bottom:2px;font-size:13.5px}
.lesson-btn:hover{background:#f2f7ff;border-color:#dce9ff;color:var(--ink)}
.lesson-btn.active{background:#eaf2ff;border-color:#cfe0ff;color:#1d4ed8;font-weight:700}
.lesson-btn .tick{float:right;color:var(--green);font-weight:800}
.bar{height:9px;border-radius:9px;background:#eaf0f8;overflow:hidden;margin:6px 0 10px}
.bar>i{display:block;height:100%;background:linear-gradient(90deg,var(--orange),var(--yellow));transition:.3s}
.content{padding:20px}
.crumb{font-size:12px;color:var(--muted);margin-bottom:4px}
.content h2{font-size:24px;margin:2px 0 6px}
.goal{background:#fff8f2;border-left:4px solid var(--orange);padding:9px 13px;border-radius:8px;
  font-size:14px;margin:12px 0 16px}
.slogan{display:inline-block;background:#fff5d6;border:1px dashed #f0c14b;color:#8a5a00;
  padding:5px 14px;border-radius:20px;font-weight:800;margin-bottom:14px}
h3{font-size:16px;margin:22px 0 10px;padding-left:10px;border-left:4px solid var(--blue)}
.stage{position:relative;background:linear-gradient(180deg,#eaf6ff,#f9ffef);
  border:1px solid #dbeaf7;border-radius:16px;overflow:hidden}
.stage svg{display:block;width:100%;height:auto}
.bubble{position:absolute;left:14%;top:9%;width:72%;min-height:66px;background:#fff;
  border:2px solid #ffd7c7;border-radius:16px;padding:10px 14px;font-size:15px;font-weight:600;
  box-shadow:0 4px 12px rgba(255,122,89,.14);display:flex;align-items:center}
.bubble:after{content:"";position:absolute;left:42px;bottom:-11px;border:6px solid transparent;
  border-top-color:#fff}
.board{position:absolute;right:5%;bottom:34%;background:#fffdf3;border:2px solid #f2dfa5;
  border-radius:10px;padding:6px 12px;font-size:13px;font-weight:700;color:#8a6b00;max-width:40%;
  box-shadow:0 3px 8px rgba(0,0,0,.05)}
.ctrl{display:flex;gap:8px;flex-wrap:wrap;align-items:center;padding:10px 14px;background:#fff;
  border-top:1px solid var(--line)}
.stepinfo{font-size:12px;color:var(--muted);margin-left:auto}
.video-box{margin-top:12px;background:#f8fbff;border:1px dashed #cddcf0;border-radius:12px;padding:12px}
.video-box video{width:100%;max-height:330px;border-radius:10px;background:#000}
.vfallback{font-size:13px;color:var(--muted);display:none}
.story{font-size:14.5px;background:#f7fbff;border-radius:10px;padding:12px 15px}
.method li{margin-bottom:4px}
details{border:1px solid var(--line);border-radius:10px;padding:9px 13px;margin-bottom:8px;background:#fcfdff}
summary{cursor:pointer;font-weight:700;font-size:14px}
details .body{padding:8px 2px 2px;font-size:14px;color:#40506a}
details .body em{font-style:normal;color:var(--green);font-weight:800}
.q{border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin-bottom:10px;background:#fff}
.q .qt{font-weight:700;margin-bottom:8px}
.opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px}
.opt{border:1px solid var(--line);border-radius:9px;padding:7px 10px;font-size:14px;text-align:left;background:#fbfdff}
.opt:hover{border-color:var(--blue)}
.opt.sel{background:#e8f1ff;border-color:var(--blue);font-weight:700}
.opt.right{background:#e6f8ee;border-color:var(--green);color:#16794a;font-weight:700}
.opt.wrong{background:#ffeded;border-color:#e5484d;color:#b42318}
.res{font-size:13.5px;margin-top:9px;padding:8px 11px;border-radius:8px;display:none}
.res.ok{background:#e9f9f0;color:#16794a;display:block}
.res.no{background:#fff0f0;color:#b42318;display:block}
.submitrow{display:flex;gap:10px;align-items:center;margin:12px 0}
.score{font-weight:800;color:var(--orange);font-size:16px}
.checkin{background:linear-gradient(120deg,#fff8ec,#f0f7ff);border:1px solid #ffe2bd;
  border-radius:14px;padding:14px 16px;margin-top:18px}
.stars{font-size:26px;letter-spacing:6px;cursor:pointer;user-select:none;color:#d8dfe9}
.stars .on{color:var(--yellow)}
textarea{width:100%;min-height:76px;border:1px solid var(--line);border-radius:10px;padding:9px 11px;
  font:inherit;font-size:14px;resize:vertical;background:#fff}
.saved{font-size:12px;color:var(--green);margin-left:8px}
.wronglist{font-size:13.5px}
.wrongitem{border-bottom:1px dashed var(--line);padding:7px 0}
.wrongitem.done{color:var(--muted);text-decoration:line-through}
.tag{display:inline-block;font-size:11px;background:#eef4ff;color:#3b5fa8;border-radius:6px;padding:1px 7px;margin-right:6px}
.notice{font-size:12.5px;color:var(--muted);margin-top:8px}
footer{text-align:center;font-size:12px;color:var(--muted);padding:26px}
</style>
</head>
<body>
<header>
  <div class="hwrap">
    <div>
      <h1>🦊 二年级奥数 · 数学森林闯关</h1>
      <div class="hsub">16 讲 · 每周 2 次 · 每次 20 分钟 ｜ 动画讲解 + 例题 + 练习 + 打卡 + 周反馈</div>
    </div>
    <div class="stats">
      <div class="stat"><b id="sDone">0</b><span>已达标讲次</span></div>
      <div class="stat"><b id="sPct">0%</b><span>总进度</span></div>
      <div class="stat"><b id="sPoints">0</b><span>积分</span></div>
      <div class="stat"><b id="sWrong">0</b><span>待订正错题</span></div>
    </div>
    <div class="tools">
      <button onclick="exportState()">导出进度</button>
      <button onclick="document.getElementById('importFile').click()">导入进度</button>
      <button onclick="showReport()">家长周报</button>
      <input id="importFile" type="file" accept="application/json" hidden onchange="importState(this)">
    </div>
  </div>
</header>

<main>
  <aside class="panel side">
    <h2>总进度</h2>
    <div class="bar"><i id="barFill" style="width:0%"></i></div>
    <div id="navList"></div>
    <h2>单元徽章</h2>
    <div id="badges" style="font-size:12.5px;color:var(--muted);line-height:2"></div>
  </aside>

  <section class="panel content" id="detail"></section>
</main>

<div id="reportModal" style="display:none;position:fixed;inset:0;background:rgba(20,35,60,.45);z-index:40;padding:24px;overflow:auto">
  <div class="panel" style="max-width:720px;margin:30px auto;padding:20px">
    <h2 style="font-size:19px;margin:0 0 12px">家长周报（可复制）</h2>
    <textarea id="reportText" style="min-height:330px"></textarea>
    <div style="margin-top:12px;display:flex;gap:8px">
      <button class="primary" onclick="copyReport()">复制全文</button>
      <button onclick="document.getElementById('reportModal').style.display='none'">关闭</button>
    </div>
  </div>
</div>

<footer>数据保存在本机浏览器，换设备请先导出进度。题目与答案用于正式教学前请人工复核。</footer>

<script id="curriculum-data" type="application/json">__CURRICULUM_JSON__</script>
<script>
const DATA = JSON.parse(document.getElementById('curriculum-data').textContent);
const LESSONS = DATA.lessons, RULES = DATA.rules, SET = DATA.settings;
const KEY = 'g2math_state_v1';
let state = load();
let cur = 1, animIdx = 0, timer = null, selections = {};

function load(){
  try{ const s = JSON.parse(localStorage.getItem(KEY)); if(s && s.rec) return s; }catch(e){}
  return {rec:{}, points:0, wrong:[], feedback:{}};
}
function save(){ localStorage.setItem(KEY, JSON.stringify(state)); }
function rec(id){ if(!state.rec[id]) state.rec[id] = {done:false,score:null,stars:0,anim:false,examples:false,date:''}; return state.rec[id]; }
function today(){ const d=new Date(); return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'); }

function buildNav(){
  const units = [...new Set(LESSONS.map(l=>l.unit))];
  let html = '';
  units.forEach(u=>{
    html += '<h2>'+u+'</h2>';
    LESSONS.filter(l=>l.unit===u).forEach(l=>{
      html += '<button class="lesson-btn'+(l.id===cur?' active':'')+'" onclick="openLesson('+l.id+')">'
        +'第'+l.id+'讲 '+l.title+(rec(l.id).done?'<span class="tick">✓</span>':'')+'</button>';
    });
  });
  document.getElementById('navList').innerHTML = html;
  const names=['计算小能手','火眼金睛','解题侦探','坚持之星'];
  document.getElementById('badges').innerHTML = units.map((u,i)=>{
    const ids=LESSONS.filter(l=>l.unit===u).map(l=>l.id);
    const ok=ids.every(id=>rec(id).done);
    return '<div>'+(ok?'🏅 ':'🔒 ')+names[i]+'：'+(ok?'已解锁（'+ids.length+' 讲全部达标）':'待解锁 '+ids.filter(id=>!rec(id).done).length+' 讲')+'</div>';
  }).join('');
}
function refreshStats(){
  const done = LESSONS.filter(l=>rec(l.id).done).length;
  document.getElementById('sDone').textContent = done;
  document.getElementById('sPct').textContent = Math.round(done/LESSONS.length*100)+'%';
  document.getElementById('barFill').style.width = (done/LESSONS.length*100)+'%';
  document.getElementById('sPoints').textContent = state.points;
  document.getElementById('sWrong').textContent = state.wrong.filter(w=>!w.fixed).length;
}
function openLesson(id){
  stopAnim(); cur=id; animIdx=0; selections={};
  buildNav(); refreshStats(); render();
  window.scrollTo({top:0,behavior:'smooth'});
}

const FOX = `<g class="char" transform="translate(66,96)">
  <ellipse cx="34" cy="86" rx="34" ry="8" fill="#dbe9d5" opacity=".7"/>
  <path d="M8 72 Q-18 58 -8 38 Q8 46 18 62 Z" fill="#ff9a4d" stroke="#e2762c" stroke-width="2"/>
  <path d="M12 70 Q-6 58 0 44" stroke="#fff0d6" stroke-width="5" fill="none" stroke-linecap="round"/>
  <polygon points="12,26 22,2 36,22" fill="#ff9a4d" stroke="#e2762c" stroke-width="2"/>
  <polygon points="48,22 62,2 66,28" fill="#ff9a4d" stroke="#e2762c" stroke-width="2"/>
  <circle cx="39" cy="42" r="30" fill="#ffb066" stroke="#e2762c" stroke-width="2"/>
  <path d="M16 48 Q39 76 62 48 Q52 66 39 66 Q26 66 16 48Z" fill="#fff4e4"/>
  <circle cx="29" cy="38" r="3.6" fill="#3b2a20"/><circle cx="50" cy="38" r="3.6" fill="#3b2a20"/>
  <ellipse cx="39" cy="52" rx="5" ry="3.6" fill="#3b2a20"/>
  <circle cx="21" cy="48" r="4" fill="#ff8d8d" opacity=".55"/><circle cx="57" cy="48" r="4" fill="#ff8d8d" opacity=".55"/>
  <rect x="14" y="68" width="50" height="20" rx="9" fill="#5b8def"/>
  <circle cx="39" cy="78" r="6" fill="#ffd76a"/>
</g>`;
const ROBOT = `<g class="char" transform="translate(510,98)">
  <ellipse cx="42" cy="86" rx="34" ry="8" fill="#dbe9d5" opacity=".7"/>
  <line x1="42" y1="6" x2="42" y2="20" stroke="#7a8ba5" stroke-width="3"/>
  <circle cx="42" cy="5" r="5" fill="#ff7a59"/>
  <rect x="10" y="20" width="64" height="48" rx="12" fill="#9fd8ff" stroke="#4a90d9" stroke-width="2"/>
  <rect x="20" y="32" width="42" height="22" rx="7" fill="#f7fdff"/>
  <circle cx="33" cy="43" r="4" fill="#2b4a6b"/><circle cx="51" cy="43" r="4" fill="#2b4a6b"/>
  <path d="M32 56 Q42 62 52 56" stroke="#2b4a6b" stroke-width="2" fill="none" stroke-linecap="round"/>
  <rect x="18" y="70" width="48" height="20" rx="6" fill="#7fb2e8" stroke="#4a90d9" stroke-width="2"/>
  <rect x="2" y="72" width="12" height="16" rx="5" fill="#7fb2e8"/><rect x="70" y="72" width="12" height="16" rx="5" fill="#7fb2e8"/>
</g>`;

function stageSVG(){
  return `<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg">
    <rect width="680" height="220" fill="none"/>
    <path d="M0 176 Q90 150 180 176 T360 176 T540 176 T680 176 L680 220 L0 220Z" fill="#dff0d8"/>
    <circle cx="120" cy="34" r="16" fill="#fff" opacity=".75"/><circle cx="140" cy="30" r="20" fill="#fff" opacity=".75"/>
    <circle cx="580" cy="26" r="14" fill="#fff" opacity=".7"/>
    <path d="M250 176 l0 -54 M250 122 l-26 -18 M250 138 l28 -20" stroke="#8fb37a" stroke-width="6" stroke-linecap="round"/>
    <circle cx="250" cy="110" r="26" fill="#9ed48a"/><circle cx="226" cy="124" r="17" fill="#8cc879"/>
    <path d="M430 176 l0 -46" stroke="#a08263" stroke-width="8" stroke-linecap="round"/>
    <circle cx="430" cy="112" r="24" fill="#7fc26a"/><circle cx="410" cy="126" r="15" fill="#6fb35c"/>
    ${FOX}${ROBOT}
    <g fill="#f6c86a"><circle cx="330" cy="168" r="5"/><circle cx="352" cy="172" r="4"/><circle cx="310" cy="174" r="3"/></g>
  </svg>`;
}

function render(){
  const L = LESSONS.find(x=>x.id===cur);
  const r = rec(cur);
  const unitIdx = [...new Set(LESSONS.map(x=>x.unit))].indexOf(L.unit)+1;
  let h = '';
  h += '<div class="crumb">'+L.unit+' ｜ '+L.week+' ｜ 达标：'+L.standard+'</div>';
  h += '<h2>第 '+L.id+' 讲 · '+L.title+'</h2>';
  h += '<div class="slogan">口诀：'+L.slogan+'</div>';
  h += '<div class="goal"><b>本周目标：</b>'+L.goal+'</div>';

  h += '<h3>① 卡通动画课堂</h3>';
  h += '<div class="stage">'+stageSVG()
     + '<div class="bubble" id="bubble">点「播放」开始，'+SET.hero+'和'+SET.partner+'一块儿讲给你听。</div>'
     + '<div class="board" id="board">'+L.slogan+'</div>'
     + '<div class="ctrl">'
     + '<button class="primary" id="playBtn" onclick="toggleAnim()">▶ 播放</button>'
     + '<button onclick="prevStep()">上一句</button><button onclick="nextStep()">下一句</button>'
     + '<button onclick="replayAnim()">重播</button>'
     + '<span class="stepinfo" id="stepInfo">第 0 / '+L.anim.length+' 句</span>'
     + '</div></div>';
  h += '<div class="video-box"><b style="font-size:13px">🎬 单元卡通短片（MP4）</b>'
     + '<div style="margin:8px 0"><video id="lessonVideo" controls preload="metadata" src="../videos/unit'+unitIdx+'-opening.mp4" onerror="videoFallback()"></video></div>'
     + '<div class="vfallback" id="vfallback">本单元 MP4 未放在 videos/ 目录，或当前环境不支持播放；不影响学习，上面的动画课堂已包含完整逐句讲解。</div>'
     + '<div class="notice">视频画面不含算式，知识点以动画课堂与教案为准。</div></div>';

  h += '<h3>② 情境故事</h3><div class="story">'+L.story+'</div>';
  h += '<h3>③ 方法步骤</h3><ol class="method">'+L.method.map(m=>'<li>'+m+'</li>').join('')+'</ol>';

  h += '<h3>④ 例题（先自己想，再点开看思路）</h3>';
  L.examples.forEach((e,i)=>{
    h += '<details><summary>例 '+(i+1)+'　'+e.q+'</summary><div class="body">'
      + e.steps.map(s=>'<div>· '+s+'</div>').join('')
      + '<div style="margin-top:6px"><em>答：'+e.answer+'</em></div></div></details>';
  });
  h += '<button onclick="markExamples()">'+ (r.examples?'✓ 已看懂例题':'看懂例题 +2 分') +'</button>';

  h += '<h3>⑤ 课堂练习（5 题，点选后提交）</h3>';
  L.exercises.forEach((e,i)=>{
    h += '<div class="q" id="q'+i+'"><div class="qt">'+(i+1)+'. '+e.q+'</div><div class="opts">'
      + e.options.map((o,j)=>'<button class="opt" id="o'+i+'_'+j+'" onclick="pick('+i+','+j+')">'+String.fromCharCode(65+j)+'. '+o+'</button>').join('')
      + '</div><div class="res" id="res'+i+'"></div></div>';
  });
  h += '<div class="submitrow"><button class="primary" onclick="submitQuiz()">提交并判分</button>'
     + '<span class="score" id="scoreText">'+(r.score!==null?'上次得分：'+r.score+' / 5':'')+'</span></div>';

  h += '<div class="checkin"><h3 style="margin:0 0 8px;border:none;padding:0">⑥ 自评、打卡与家长反馈</h3>'
     + '<div>今天的课：<span class="stars" id="stars">'
     + [1,2,3].map(n=>'<span class="'+(r.stars>=n?'on':'')+'" onclick="setStars('+n+')">★</span>').join('')
     + '</span> <span style="font-size:12px;color:var(--muted)">1=没听懂　2=有点难　3=我懂了</span></div>'
     + '<div style="margin:10px 0"><button class="primary" onclick="checkIn()">'+(r.done?'✓ 已达标（点此更新记录）':'完成打卡')+'</button>'
     + ' <span style="font-size:12px;color:var(--muted)">'+RULES.pass+'</span></div>'
     + '<div style="font-size:13px;font-weight:700;margin:12px 0 6px">家长本周反馈</div>'
     + '<textarea id="fb" placeholder="卡在哪一题？最有成就感的是哪一题？下周怎么调整？">'+esc(state.feedback[cur]||'')+'</textarea>'
     + '<div style="margin-top:8px"><button onclick="saveFeedback()">保存反馈 +5 分</button><span class="saved" id="fbSaved"></span></div>'
     + '</div>';

  h += '<h3>⑦ 易错提醒</h3><div class="story" style="background:#fff8f2">'+L.mistake+'</div>';
  h += '<h3>⑧ 家长提问（只问，不代算）</h3><ol class="method">'+L.parent.map(p=>'<li>'+p+'</li>').join('')+'</ol>';
  h += '<h3>⑨ 错题本</h3><div class="wronglist" id="wrongList"></div>';
  h += '<div style="margin-top:22px;display:flex;gap:10px">'
     + '<button onclick="openLesson(Math.max(1,cur-1))">← 上一讲</button>'
     + '<button onclick="openLesson(Math.min(LESSONS.length,cur+1))">下一讲 →</button></div>';
  document.getElementById('detail').innerHTML = h;
  renderWrong();
  if(location.hostname.indexOf('github.io')>-1){
    videoFallback('在线版暂不含 MP4 短片；上面的动画课堂已包含本讲完整逐句讲解，直接点「播放」即可。');
  }
}

function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function videoFallback(msg){ const v=document.getElementById('lessonVideo'); if(v) v.style.display='none';
  const f=document.getElementById('vfallback'); if(f){ if(msg) f.textContent=msg; f.style.display='block'; } }

function showStep(){
  const L=LESSONS.find(x=>x.id===cur);
  if(animIdx<0) animIdx=0; if(animIdx>=L.anim.length) animIdx=L.anim.length-1;
  document.getElementById('bubble').textContent = L.anim[animIdx];
  document.getElementById('stepInfo').textContent = '第 '+(animIdx+1)+' / '+L.anim.length+' 句';
  document.getElementById('board').textContent = L.slogan;
}
function toggleAnim(){ if(timer) stopAnim(); else startAnim(); }
function startAnim(){
  const L=LESSONS.find(x=>x.id===cur);
  if(animIdx>=L.anim.length-1) animIdx=0;
  document.getElementById('playBtn').textContent='⏸ 暂停';
  showStep();
  timer=setInterval(()=>{
    if(animIdx>=L.anim.length-1){ stopAnim(); grantAnim(); return; }
    animIdx++; showStep();
  },3200);
}
function stopAnim(){ if(timer){clearInterval(timer);timer=null;}
  const b=document.getElementById('playBtn'); if(b) b.textContent='▶ 播放'; }
function nextStep(){ stopAnim(); const L=LESSONS.find(x=>x.id===cur);
  if(animIdx<L.anim.length-1) animIdx++; showStep(); if(animIdx===L.anim.length-1) grantAnim(); }
function prevStep(){ stopAnim(); if(animIdx>0) animIdx--; showStep(); }
function replayAnim(){ stopAnim(); animIdx=0; showStep(); startAnim(); }
function grantAnim(){ const r=rec(cur); if(!r.anim){ r.anim=true; state.points+=2; save(); refreshStats(); } }
function markExamples(){ const r=rec(cur); if(r.examples) return;
  r.examples=true; state.points+=2; save(); render(); refreshStats(); }

function pick(i,j){
  selections[i]=j;
  const L=LESSONS.find(x=>x.id===cur);
  L.exercises[i].options.forEach((_,k)=>{
    const el=document.getElementById('o'+i+'_'+k); if(el) el.className='opt'+(k===j?' sel':'');
  });
}
function submitQuiz(){
  const L=LESSONS.find(x=>x.id===cur);
  if(Object.keys(selections).length<L.exercises.length){ alert('还有题目没选，做完 5 题再提交。'); return; }
  let right=0;
  L.exercises.forEach((e,i)=>{
    const ok = selections[i]===e.answer;
    if(ok) right++;
    e.options.forEach((_,k)=>{
      const el=document.getElementById('o'+i+'_'+k); if(!el) return;
      el.className='opt'+(k===e.answer?' right':(k===selections[i]?' wrong':''));
    });
    const res=document.getElementById('res'+i);
    res.className='res '+(ok?'ok':'no');
    res.innerHTML=(ok?'✓ 答对了　':'✗ 正确答案是 '+String.fromCharCode(65+e.answer)+'. '+e.options[e.answer]+'　')+esc(e.why);
    if(!ok){
      const key=cur+'-'+i;
      if(!state.wrong.some(w=>w.key===key)) state.wrong.push({key:key,lesson:cur,q:e.q,right:e.options[e.answer],fixed:false});
    }else{
      const key=cur+'-'+i;
      state.wrong.filter(w=>w.key===key).forEach(w=>w.fixed=true);
    }
  });
  const r=rec(cur);
  if(r.score===null){ state.points += right*2; }
  r.score=right;
  const pass = right>=4;
  if(pass && !r.done){} // 打卡仍由孩子/家长确认
  save(); refreshStats(); renderWrong();
  document.getElementById('scoreText').textContent='本次得分：'+right+' / 5';
  let msg = right>=4 ? '达标！可以打卡啦。' : (right===3 ? '订正错题，隔一天再做一遍。' : '先重看动画课堂和例题，本讲顺延一周。');
  setTimeout(()=>alert('做对 '+right+' 题。'+msg),120);
}
function renderWrong(){
  const list=state.wrong.filter(w=>w.lesson===cur);
  const el=document.getElementById('wrongList'); if(!el) return;
  if(!list.length){ el.innerHTML='<span style="color:var(--muted)">本讲还没有错题。</span>'; return; }
  el.innerHTML=list.map(w=>'<div class="wrongitem'+(w.fixed?' done':'')+'">'
    +'<span class="tag">第 '+w.lesson+' 讲</span>'+esc(w.q)+'　正确答案：'+esc(w.right)
    +(w.fixed?'　✓ 已订正':'　<button style="padding:2px 9px;font-size:12px" onclick="fixWrong(\''+w.key+'\')">标记已订正</button>')
    +'</div>').join('');
}
function fixWrong(key){ const w=state.wrong.find(x=>x.key===key); if(w){w.fixed=true;save();renderWrong();refreshStats();} }
function setStars(n){ const r=rec(cur);
  if(r.stars<3 && n===3) state.points+=3;
  r.stars=n; save(); render(); }
function checkIn(){
  const r=rec(cur);
  if(r.score===null){ alert('先完成 5 道练习再打卡。'); return; }
  const pass=r.score>=4;
  r.done=pass; r.date=today(); save();
  buildNav(); refreshStats(); render();
  alert(pass?'第 '+cur+' 讲已达标 ✓':'得分 '+r.score+' 分，记为「需复学」：订正错题或重看讲解后再打卡。');
}
function saveFeedback(){
  const t=document.getElementById('fb').value.trim();
  const had=!!state.feedback[cur];
  state.feedback[cur]=t;
  if(t && !had) state.points+=5;
  save(); refreshStats();
  document.getElementById('fbSaved').textContent='已保存 '+today();
}

function showReport(){
  const done=LESSONS.filter(l=>rec(l.id).done).length;
  const lines=['二年级奥数 · 学习周报（生成日期 '+today()+'）','',
    '总进度：'+done+' / '+LESSONS.length+' 讲达标；积分 '+state.points+'；待订正错题 '+state.wrong.filter(w=>!w.fixed).length+' 道','',
    '—— 逐讲记录 ——'];
  LESSONS.forEach(l=>{
    const r=rec(l.id);
    lines.push(l.week+' 第'+l.id+'讲 '+l.title+'：'+(r.score===null?'未做':'得分 '+r.score+'/5')
      +'；'+(r.done?'已达标':'未达标')+'；自评 '+r.stars+' 星'+(r.date?'；打卡 '+r.date:''));
  });
  lines.push('','—— 家长反馈 ——');
  LESSONS.forEach(l=>{ if(state.feedback[l.id]) lines.push('第'+l.id+'讲：'+state.feedback[l.id]); });
  if(!Object.values(state.feedback).some(x=>x)) lines.push('（尚未填写）');
  lines.push('','—— 待订正错题 ——');
  const ws=state.wrong.filter(w=>!w.fixed);
  if(ws.length) ws.forEach(w=>lines.push('第'+w.lesson+'讲：'+w.q+'　正确答案 '+w.right));
  else lines.push('（无）');
  lines.push('','—— 下周建议 ——');
  const need=LESSONS.filter(l=>!rec(l.id).done);
  const bad=LESSONS.filter(l=>rec(l.id).score!==null && rec(l.id).score<=2);
  if(bad.length) lines.push('有 '+bad.length+' 讲需复学：第 '+bad.map(l=>l.id).join('、')+' 讲；暂不推进新讲。');
  else if(need.length) lines.push('继续第 '+need[0].id+' 讲《'+need[0].title+'》；家长反馈里「卡住的题」先在开课前 5 分钟重讲。');
  else lines.push('16 讲全部达标，可做变式练习（把例题数字换掉重做）。');
  document.getElementById('reportText').value=lines.join('\n');
  document.getElementById('reportModal').style.display='block';
}
function copyReport(){ const t=document.getElementById('reportText'); t.select();
  try{document.execCommand('copy');alert('已复制，可直接粘贴到周反馈 Issue 或微信。');}catch(e){alert('请手动选中文本复制。');} }
function exportState(){
  const blob=new Blob([JSON.stringify(state,null,2)],{type:'application/json'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob);
  a.download='grade2-math-progress-'+today()+'.json'; a.click(); URL.revokeObjectURL(a.href);
}
function importState(input){
  const f=input.files[0]; if(!f) return;
  const reader=new FileReader();
  reader.onload=e=>{ try{ const s=JSON.parse(e.target.result);
      if(!s.rec) throw new Error('格式不对'); state=s; save(); buildNav(); refreshStats(); render(); alert('进度已导入。');
    }catch(err){ alert('导入失败：'+err.message); } };
  reader.readAsText(f); input.value='';
}

buildNav(); refreshStats(); render();
</script>
</body>
</html>
"""

payload = json.dumps({"settings": SETTINGS, "rules": RULES, "lessons": CURRICULUM},
                     ensure_ascii=False).replace("</", "<\\/")
w("site/index.html", HTML.replace("__CURRICULUM_JSON__", payload))

# Pages 站点根：自动跳转到学习中心，便于使用短链接
w("index.html", """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url=site/">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>二年级奥数 · 数学森林闯关</title>
<style>body{margin:0;padding:64px 20px;text-align:center;background:#f5f8fc;color:#20304a;
font-family:"PingFang SC","Microsoft YaHei",system-ui,sans-serif;line-height:1.8}
h1{font-size:22px;margin:0 0 10px}a{color:#ff7a59;font-weight:700}</style>
</head>
<body>
<h1>二年级奥数 · 数学森林闯关</h1>
<p>正在进入学习中心……</p>
<p><a href="site/">如果没有自动跳转，点这里进入</a></p>
</body>
</html>
""")

print("done. lessons=%d" % len(CURRICULUM))
