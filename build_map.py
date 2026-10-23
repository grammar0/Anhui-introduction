# -*- coding: utf-8 -*-
"""生成单文件、可嵌入的「安徽十六城」互动地图 HTML。"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GEO = json.loads((ROOT / "anhui-geo.json").read_text(encoding="utf-8"))
OUTLINE = json.loads((ROOT / "anhui-outline.json").read_text(encoding="utf-8"))

LAT0 = math.radians(32.0)
W, H, PAD = 760, 980, 30

REGION_COLORS = {
    "皖北": "#c3a05f",
    "江淮": "#6f9785",
    "皖南": "#7794ae",
}

# 每个城市一种略有差异的同色系填充，避免整块色块显得呆板
CITY_FILLS = {
    "huaibei": "#c6a363", "bozhou": "#c19b58", "suzhou": "#cba86a",
    "bengbu": "#bd9652", "fuyang": "#c8a563", "huainan": "#c09a57",
    "hefei": "#6d9986", "chuzhou": "#729d8a", "luan": "#68917f", "anqing": "#76a08d",
    "huangshan": "#7694af", "chizhou": "#7c9ab4", "xuancheng": "#7190ab",
    "tongling": "#809db7", "wuhu": "#7492ad", "maanshan": "#7896b0",
}

CITIES = [
    {
        "id": "huaibei", "name": "淮北市", "short": "淮北", "en": "HUAIBEI", "region": "皖北",
        "area": "2,741", "pop": "194.4", "tagline": "运河故里，能源之城",
        "desc": "因煤而兴的皖北城市，隋唐大运河曾在此流淌。相山森林公园、南湖湿地与临涣古镇的茶馆，构成一幅刚柔并济的皖北生活图景。",
        "tags": ["煤城", "大运河", "口子酒"],
        "spots": ["相山公园", "南湖湿地", "临涣古镇", "隋唐大运河遗址"],
    },
    {
        "id": "bozhou", "name": "亳州市", "short": "亳州", "en": "BOZHOU", "region": "皖北",
        "area": "8,374", "pop": "496.0", "tagline": "药都酒乡，曹魏故里",
        "desc": "商汤故都，曹操、华佗故里，国家历史文化名城。花戏楼的砖雕木雕精美绝伦，曹操运兵道在地下蜿蜒；作为“中华药都”，中药材香气弥漫全城。",
        "tags": ["历史文化名城", "中药材", "古井贡酒"],
        "spots": ["花戏楼", "曹操运兵道", "华祖庵", "古井酒文化博览园"],
    },
    {
        "id": "suzhou", "name": "宿州市", "short": "宿州", "en": "SUZHOU", "region": "皖北",
        "area": "9,939", "pop": "526.9", "tagline": "楚汉故地，奇石梨乡",
        "desc": "皖北门户，九州通衢。楚汉相争的垓下故事、虞姬墓的传说在此流传；灵璧奇石、砀山梨园与皇藏峪的青山，让平原地带多了几分奇趣。",
        "tags": ["皖北门户", "灵璧奇石", "砀山梨"],
        "spots": ["皇藏峪", "虞姬墓", "灵璧奇石文化园", "砀山梨园"],
    },
    {
        "id": "bengbu", "name": "蚌埠市", "short": "蚌埠", "en": "BENGBU", "region": "皖北",
        "area": "5,952", "pop": "326.7", "tagline": "淮上明珠，铁路枢纽",
        "desc": "淮河穿城而过，古称“珠城”，是皖北重要的交通枢纽和工业城市。双墩遗址、禹会诸侯的传说与龙子湖的波光，让这座火车拉来的城市兼有远古回响与市井烟火。",
        "tags": ["淮河文化", "交通枢纽", "珠城"],
        "spots": ["龙子湖", "张公山公园", "涂山", "蚌埠市博物馆"],
    },
    {
        "id": "fuyang", "name": "阜阳市", "short": "阜阳", "en": "FUYANG", "region": "皖北",
        "area": "10,118", "pop": "808.4", "tagline": "管仲故里，颍淮粮仓",
        "desc": "皖北人口大市，淮河最大支流颍河穿境而过。这里孕育了管仲、鲍叔牙，颍州西湖曾与杭州西湖齐名；八里河与万亩良田铺展成平原上的舒展画卷。",
        "tags": ["人口大市", "管仲", "颍州西湖"],
        "spots": ["颍州西湖", "八里河", "阜阳生态乐园", "管仲故里"],
    },
    {
        "id": "huainan", "name": "淮南市", "short": "淮南", "en": "HUAINAN", "region": "皖北",
        "area": "5,533", "pop": "301.6", "tagline": "八公山下，豆腐故里",
        "desc": "八公山下，淮河之滨，楚风汉韵在此沉淀。这里是豆腐的发源地，也是淝水之战的古战场；寿县古城墙与安丰塘至今仍讲述着千年故事。",
        "tags": ["能源之都", "楚汉文化", "寿县古城"],
        "spots": ["八公山", "寿县古城", "安丰塘", "焦岗湖"],
    },
    {
        "id": "hefei", "name": "合肥市", "short": "合肥", "en": "HEFEI", "region": "江淮",
        "area": "11,445", "pop": "985.3", "tagline": "庐州古韵，科创之城",
        "desc": "古称庐州，安徽省会，环巢湖而建。全国重要的科教基地和综合性国家科学中心，量子信息、新能源汽车等产业在此集聚。城市气质一半是包公故里的厚重，一半是科创之城的锐气。",
        "tags": ["省会", "科教名城", "环巢湖"],
        "spots": ["包公园", "三河古镇", "巢湖姥山岛", "安徽博物院"],
    },
    {
        "id": "chuzhou", "name": "滁州市", "short": "滁州", "en": "CHUZHOU", "region": "江淮",
        "area": "13,516", "pop": "405.5", "tagline": "醉翁之意，改革之源",
        "desc": "皖东门户，南京都市圈重要成员。欧阳修在此写下《醉翁亭记》，小岗村按下中国农村改革的第一枚红手印；琅琊山的林壑与明皇陵的石刻相映成趣。",
        "tags": ["南京都市圈", "醉翁亭", "小岗村"],
        "spots": ["琅琊山", "醉翁亭", "明皇陵", "小岗村"],
    },
    {
        "id": "luan", "name": "六安市", "short": "六安", "en": "LU'AN", "region": "江淮",
        "area": "15,451", "pop": "434.3", "tagline": "大别门户，将军故里",
        "desc": "大别山北麓的门户，红色老区与生态绿城。天堂寨的飞瀑、万佛湖的碧水、白马尖的云海，构成皖西最动人的山水长卷；六安瓜片清香悠长。",
        "tags": ["红色老区", "大别山", "六安瓜片"],
        "spots": ["天堂寨", "万佛湖", "白马尖", "皖西大裂谷"],
    },
    {
        "id": "anqing", "name": "安庆市", "short": "安庆", "en": "ANQING", "region": "江淮",
        "area": "13,590", "pop": "411.5", "tagline": "黄梅故里，桐城文章",
        "desc": "曾为安徽省会，国家历史文化名城。黄梅戏在此婉转传唱，桐城派文章甲天下；天柱山擎起皖西南的脊梁，振风塔守望着长江。",
        "tags": ["历史文化名城", "黄梅戏", "天柱山"],
        "spots": ["天柱山", "迎江寺振风塔", "菱湖", "桐城文庙"],
    },
    {
        "id": "huangshan", "name": "黄山市", "short": "黄山", "en": "HUANGSHAN", "region": "皖南",
        "area": "9,807", "pop": "131.7", "tagline": "徽州故里，天下黄山",
        "desc": "古称徽州，徽商故里、徽文化核心区。黄山集世界文化与自然双遗产于一身，宏村、西递的白墙黛瓦倒映在新安江的山水间。",
        "tags": ["徽文化", "世界遗产", "徽商"],
        "spots": ["黄山", "宏村", "西递", "屯溪老街"],
    },
    {
        "id": "chizhou", "name": "池州市", "short": "池州", "en": "CHIZHOU", "region": "皖南",
        "area": "8,392", "pop": "132.3", "tagline": "千载诗人地，九华佛国",
        "desc": "依九华山而居，临长江而卧，素有“千载诗人地”之称。李白、杜牧、苏轼都曾在此留下诗篇；杏花村的酒旗、牯牛降的原始森林与平天湖的月色，皆是江南意韵。",
        "tags": ["九华山", "生态绿城", "杏花村"],
        "spots": ["九华山", "杏花村", "牯牛降", "平天湖"],
    },
    {
        "id": "xuancheng", "name": "宣城市", "short": "宣城", "en": "XUANCHENG", "region": "皖南",
        "area": "12,313", "pop": "248.7", "tagline": "宣纸之乡，诗画皖南",
        "desc": "皖南山水与徽文化交汇之地，文房四宝中的宣纸、宣笔皆出于此。敬亭山、桃花潭、查济古村与龙川胡氏宗祠，串起一条诗画江南的线索。",
        "tags": ["文房四宝", "徽文化", "敬亭山"],
        "spots": ["敬亭山", "龙川", "桃花潭", "查济古村"],
    },
    {
        "id": "tongling", "name": "铜陵市", "short": "铜陵", "en": "TONGLING", "region": "皖南",
        "area": "3,008", "pop": "130.1", "tagline": "古铜都，皖江门户",
        "desc": "采冶铜的历史绵延三千年，被誉为“中国古铜都”。天井湖嵌在城中，大通古镇临江而居，工业遗产与山水洲城在这里交织。",
        "tags": ["铜工业", "古铜都", "长江"],
        "spots": ["天井湖", "大通古镇", "铜官山", "浮山"],
    },
    {
        "id": "wuhu", "name": "芜湖市", "short": "芜湖", "en": "WUHU", "region": "皖南",
        "area": "6,026", "pop": "375.6", "tagline": "江东名邑，长江明珠",
        "desc": "位于长江之滨，古称鸠兹，是安徽融入长三角的桥头堡。奇瑞汽车、机器人产业和港口经济让这座“江东名邑”充满活力，方特乐园与鸠兹古镇则添了几分轻快。",
        "tags": ["省域副中心", "港口城市", "方特"],
        "spots": ["鸠兹古镇", "芜湖方特", "镜湖", "天门山"],
    },
    {
        "id": "maanshan", "name": "马鞍山市", "short": "马鞍山", "en": "MA'ANSHAN", "region": "皖南",
        "area": "4,049", "pop": "219.1", "tagline": "诗城钢城，长江采石",
        "desc": "长江东岸的钢铁之城，也是李白笔下的“天门中断楚江开”。采石矶、太白楼与濮塘竹海，让工业城市的硬朗线条里透出诗意。",
        "tags": ["钢铁基地", "李白", "采石矶"],
        "spots": ["采石矶", "太白楼", "濮塘", "褒禅山"],
    },
]

NAME_TO_ID = {c["name"]: c["id"] for c in CITIES}
SHORT = {c["name"]: c["short"] for c in CITIES}

# 手工微调拥挤区域的标注位置（单位：SVG 用户坐标）
LABEL_OFFSET = {
    "马鞍山市": (26, 8),
    "芜湖市": (8, 18),
    "铜陵市": (-14, 6),
    "淮北市": (-32, -6),
    "宿州市": (24, -14),
    "淮南市": (-20, -8),
    "蚌埠市": (14, -14),
    "滁州市": (20, -16),
    "池州市": (22, 10),
}


def project(lon, lat):
    return lon * math.cos(LAT0), -lat


def collect_points():
    pts = []
    for feature in GEO["features"]:
        geom = feature["geometry"]
        polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        for poly in polys:
            for ring in poly:
                pts.extend(project(lon, lat) for lon, lat in ring)
    return pts


PTS = collect_points()
MINX, MAXX = min(p[0] for p in PTS), max(p[0] for p in PTS)
MINY, MAXY = min(p[1] for p in PTS), max(p[1] for p in PTS)
SCALE = min((W - 2 * PAD) / (MAXX - MINX), (H - 2 * PAD) / (MAXY - MINY))
OX = PAD + ((W - 2 * PAD) - (MAXX - MINX) * SCALE) / 2
OY = PAD + ((H - 2 * PAD) - (MAXY - MINY) * SCALE) / 2


def screen(lon, lat):
    x, y = project(lon, lat)
    return OX + (x - MINX) * SCALE, OY + (y - MINY) * SCALE


def ring_to_path(ring):
    parts = []
    for i, (lon, lat) in enumerate(ring):
        x, y = screen(lon, lat)
        parts.append(("M" if i == 0 else "L") + f"{x:.2f} {y:.2f}")
    return "".join(parts) + "Z"


def geometry_to_path(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    return "".join(ring_to_path(ring) for poly in polys for ring in poly)


def build_city_paths():
    out = []
    for feature in GEO["features"]:
        name = feature["properties"]["name"]
        cid = NAME_TO_ID[name]
        city = next(c for c in CITIES if c["id"] == cid)
        fill = CITY_FILLS[cid]
        label = f'{name}，{city["tagline"]}。点击查看城市介绍。'
        out.append(
            f'<path class="city" data-city="{cid}" d="{geometry_to_path(feature["geometry"])}" '
            f'fill="{fill}" tabindex="0" role="button" aria-label="{label}">'
            f'<title>{name} · 点击查看介绍</title></path>'
        )
    return "\n          ".join(out)


def build_labels():
    out = []
    for feature in GEO["features"]:
        name = feature["properties"]["name"]
        cid = NAME_TO_ID[name]
        lon, lat = feature["properties"]["centroid"]
        x, y = screen(lon, lat)
        dx, dy = LABEL_OFFSET.get(name, (0, 0))
        out.append(
            f'<text class="city-label" data-city="{cid}" x="{x + dx:.1f}" y="{y + dy:.1f}" '
            f'text-anchor="middle">{SHORT[name]}</text>'
        )
    return "\n          ".join(out)


def build_outline():
    return "".join(geometry_to_path(f["geometry"]) for f in OUTLINE["features"])


def build_index():
    groups = []
    for region in ("皖北", "江淮", "皖南"):
        items = []
        for c in CITIES:
            if c["region"] != region:
                continue
            items.append(
                f'<button type="button" class="city-item" data-city="{c["id"]}" '
                f'style="--dot:{CITY_FILLS[c["id"]]}">'
                f'<span class="city-dot"></span>'
                f'<span class="city-cn">{c["short"]}</span>'
                f'<span class="city-en">{c["en"]}</span>'
                f'</button>'
            )
        groups.append(
            f'<section class="index-group" aria-label="{region}城市">'
            f'<p class="group-label" style="--dot:{REGION_COLORS[region]}">'
            f'<span class="group-bar"></span>{region}<em>{len(items)}</em></p>'
            f'<div class="city-list">{"".join(items)}</div>'
            f'</section>'
        )
    return "\n        ".join(groups)


DATA_JSON = json.dumps(
    {c["id"]: {k: v for k, v in c.items() if k != "id"} for c in CITIES},
    ensure_ascii=False,
    separators=(",", ":"),
)
REGION_JSON = json.dumps(REGION_COLORS, ensure_ascii=False, separators=(",", ":"))

HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="description" content="安徽省十六市互动地图：点击任一城市区域，查看城市简介、面积、人口与城市名片。">
<title>安徽十六城 · 互动地图</title>
<style>
  :root{
    --paper:#f3eee2;
    --paper-2:#fbf8f0;
    --ink:#1f2c27;
    --muted:#6b746c;
    --line:rgba(31,44,39,.13);
    --line-strong:rgba(31,44,39,.24);
    --accent:#b34a32;
    --gold:#a97c32;
    --north:#c3a05f;
    --central:#6f9785;
    --south:#7794ae;
    --shadow:0 18px 50px rgba(37,45,38,.12);
    --serif:"Noto Serif SC","Songti SC","STSong","SimSun",serif;
    --sans:"Noto Sans SC","PingFang SC","Microsoft YaHei","Segoe UI",sans-serif;
  }
  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{
    margin:0;
    color:var(--ink);
    background:
      radial-gradient(1100px 620px at 8% -8%, #fffdf7 0%, rgba(255,253,247,0) 60%),
      radial-gradient(900px 700px at 105% 108%, #e5dcc9 0%, rgba(229,220,201,0) 58%),
      var(--paper);
    font-family:var(--sans);
    -webkit-font-smoothing:antialiased;
    min-height:100vh;
  }
  body::before{
    content:"";
    position:fixed;
    inset:0;
    pointer-events:none;
    z-index:0;
    opacity:.35;
    background-image:radial-gradient(rgba(78,88,74,.18) .7px, transparent .7px);
    background-size:18px 18px;
    mask-image:linear-gradient(to bottom, rgba(0,0,0,.65), transparent 70%);
  }
  body.modal-open{overflow:hidden}
  .page{
    position:relative;
    z-index:1;
    width:min(1180px, calc(100% - 48px));
    margin:0 auto;
    padding:42px 0 30px;
  }

  /* ---------- 页头 ---------- */
  .masthead{
    display:grid;
    grid-template-columns:1fr auto;
    grid-template-areas:"brand legend" "lede legend";
    align-items:end;
    gap:10px 28px;
    padding-bottom:28px;
    border-bottom:1px solid var(--line-strong);
  }
  .brand{grid-area:brand;display:flex;align-items:center;gap:18px}
  .seal{
    width:64px;height:64px;flex:0 0 auto;
    display:grid;place-items:center;
    background:var(--accent);
    color:#fff7ea;
    border-radius:6px;
    box-shadow:inset 0 0 0 2px rgba(255,247,234,.55), 0 8px 18px rgba(179,74,50,.22);
    transform:rotate(-2deg);
  }
  .seal span{
    font-family:var(--serif);
    font-size:38px;
    line-height:1;
    font-weight:700;
    transform:translateY(-1px);
  }
  .kicker{
    margin:0 0 4px;
    font-size:10px;
    letter-spacing:.28em;
    font-weight:700;
    color:var(--gold);
    text-transform:uppercase;
  }
  h1{
    margin:0;
    font-family:var(--serif);
    font-weight:700;
    font-size:clamp(38px,5vw,58px);
    letter-spacing:.04em;
    line-height:1.05;
  }
  .lede{
    grid-area:lede;
    margin:0;
    max-width:600px;
    color:var(--muted);
    font-size:14px;
    line-height:1.8;
    letter-spacing:.04em;
  }
  .legend{
    grid-area:legend;
    display:flex;
    flex-wrap:wrap;
    justify-content:flex-end;
    gap:8px 18px;
    padding-bottom:8px;
    font-size:12px;
    color:#4e5a51;
  }
  .legend span{display:inline-flex;align-items:center;gap:7px;white-space:nowrap}
  .legend i{
    width:10px;height:10px;border-radius:3px;
    background:var(--c);
    box-shadow:inset 0 0 0 1px rgba(31,44,39,.14);
  }

  /* ---------- 主区域 ---------- */
  .atlas{
    display:grid;
    grid-template-columns:minmax(0,1fr) 338px;
    gap:26px;
    align-items:start;
    padding-top:28px;
  }
  .map-card,
  .index-card{
    background:rgba(251,248,240,.86);
    border:1px solid rgba(31,44,39,.12);
    border-radius:20px;
    box-shadow:var(--shadow);
    backdrop-filter:blur(8px);
  }
  .map-card{overflow:hidden}
  .card-head{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:14px;
    padding:19px 24px 16px;
    border-bottom:1px solid var(--line);
  }
  .card-head h2{
    margin:0;
    font-family:var(--serif);
    font-size:17px;
    letter-spacing:.08em;
    font-weight:700;
  }
  .head-hint{
    display:inline-flex;align-items:center;gap:7px;
    color:var(--muted);font-size:11px;letter-spacing:.08em;white-space:nowrap;
  }
  .head-hint i{
    width:6px;height:6px;border-radius:50%;
    background:var(--accent);
    box-shadow:0 0 0 4px rgba(179,74,50,.12);
  }
  .map-shell{
    position:relative;
    margin:18px;
    padding:2px;
    border-radius:16px;
    border:1px solid rgba(31,44,39,.09);
    background-color:#f8f4e9;
    background-image:
      radial-gradient(rgba(78,88,74,.16) .8px, transparent .8px),
      radial-gradient(120% 80% at 50% 0%, rgba(255,255,255,.9), rgba(255,255,255,0) 62%);
    background-size:20px 20px, 100% 100%;
    overflow:hidden;
  }
  .map-shell::before,
  .map-shell::after{
    content:"";
    position:absolute;
    width:24px;height:24px;
    border-color:rgba(169,124,50,.55);
    border-style:solid;
    z-index:2;
    pointer-events:none;
  }
  .map-shell::before{top:10px;left:10px;border-width:1px 0 0 1px}
  .map-shell::after{bottom:10px;right:10px;border-width:0 1px 1px 0}
  .map-shell svg{display:block;width:100%;height:auto;position:relative;z-index:1}
  .map-note{
    position:absolute;
    right:16px;bottom:13px;
    z-index:2;
    font-size:9px;
    letter-spacing:.14em;
    color:rgba(31,44,39,.4);
    pointer-events:none;
  }
  .north-mark{
    position:absolute;
    top:18px;right:18px;
    z-index:2;
    display:flex;flex-direction:column;align-items:center;gap:3px;
    color:rgba(31,44,39,.48);
    font-size:9px;letter-spacing:.16em;
    pointer-events:none;
  }
  .north-mark svg{width:22px;height:26px;display:block}

  /* ---------- 地图 ---------- */
  .city{
    stroke:#faf6ea;
    stroke-width:1.35;
    stroke-linejoin:round;
    cursor:pointer;
    transition:filter .18s ease, opacity .18s ease, stroke .18s ease;
    outline:none;
  }
  .city:hover,
  .city:focus-visible{filter:brightness(1.07) saturate(1.08)}
  .city:focus-visible{stroke:#fffdf6;stroke-width:2.4}
  .map-cities.has-selection .city:not(.is-active){opacity:.42}
  .city.is-active{
    stroke:#fffaf0;
    stroke-width:2.6;
    filter:brightness(1.05) drop-shadow(0 0 7px rgba(43,63,53,.28));
  }
  .province-line{
    fill:none;
    stroke:#26342d;
    stroke-width:2.1;
    stroke-linejoin:round;
    stroke-linecap:round;
    pointer-events:none;
  }
  .city-label{
    font-family:var(--serif);
    font-size:15px;
    font-weight:700;
    fill:#24312b;
    letter-spacing:.08em;
    paint-order:stroke;
    stroke:#faf6ea;
    stroke-width:3.4px;
    stroke-linejoin:round;
    pointer-events:none;
    transition:fill .18s ease, opacity .18s ease;
  }
  .map-labels.has-selection .city-label{opacity:.38}
  .map-labels.has-selection .city-label.is-active{opacity:1;fill:var(--accent)}
  .city-label.is-active{fill:var(--accent)}
  .map-labels.is-hidden{display:none}
  .map-cities.is-filtered .city:not(.is-active){opacity:.32}

  /* ---------- 底部信息 ---------- */
  .card-foot{
    display:flex;
    align-items:center;
    gap:26px;
    padding:0 24px 20px;
    color:var(--muted);
    font-size:11px;
    letter-spacing:.05em;
  }
  .card-foot b{
    color:var(--ink);
    font-family:var(--serif);
    font-size:15px;
    font-weight:700;
    margin-right:3px;
  }
  .foot-tip{margin-left:auto;color:rgba(31,44,39,.42)}

  /* ---------- 城市索引 ---------- */
  .index-card{
    padding:22px 20px 18px;
    position:sticky;
    top:20px;
  }
  .index-head{
    display:flex;align-items:baseline;justify-content:space-between;
    gap:10px;
    padding-bottom:12px;
    border-bottom:1px solid var(--line);
  }
  .index-head h2{
    margin:0;
    font-family:var(--serif);
    font-size:21px;
    letter-spacing:.1em;
  }
  .index-head span{
    font-size:9px;letter-spacing:.2em;color:var(--gold);font-weight:700;
  }
  .index-sub{
    margin:11px 0 14px;
    color:var(--muted);
    font-size:11px;
    line-height:1.65;
    letter-spacing:.04em;
  }
  .index-groups{
    display:grid;
    gap:14px;
  }
  .index-group{min-width:0}
  .group-label{
    display:flex;
    align-items:center;
    gap:7px;
    margin:0 0 6px;
    color:#59655c;
    font-size:9px;
    font-weight:700;
    letter-spacing:.18em;
  }
  .group-bar{
    width:13px;height:2px;
    background:var(--dot);
    border-radius:999px;
  }
  .group-label em{
    margin-left:auto;
    color:#a1a99e;
    font-style:normal;
    font-size:8px;
    letter-spacing:.08em;
  }
  .city-list{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:4px;
  }
  .city-item{
    appearance:none;
    display:grid;
    grid-template-columns:7px 1fr;
    grid-template-rows:auto auto;
    column-gap:7px;
    align-items:center;
    padding:7px 7px;
    border:1px solid transparent;
    border-radius:8px;
    background:transparent;
    color:var(--ink);
    text-align:left;
    cursor:pointer;
    transition:background .16s ease, border-color .16s ease, transform .16s ease;
    font-family:var(--sans);
  }
  .city-item:hover,
  .city-item:focus-visible{
    background:rgba(255,253,246,.9);
    border-color:rgba(31,44,39,.12);
    transform:translateY(-1px);
    outline:none;
  }
  .city-item.is-active{
    background:#fffdf6;
    border-color:rgba(179,74,50,.35);
    box-shadow:inset 3px 0 0 var(--accent);
  }
  .city-dot{
    grid-row:1 / span 2;
    width:8px;height:8px;border-radius:50%;
    background:var(--dot);
    box-shadow:inset 0 0 0 1px rgba(31,44,39,.12);
  }
  .city-cn{font-size:13px;font-weight:600;letter-spacing:.06em;line-height:1.35}
  .city-en{font-size:8px;letter-spacing:.12em;color:#91998f;line-height:1.2}
  .index-foot{
    margin-top:14px;
    padding-top:13px;
    border-top:1px dashed var(--line-strong);
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:8px;
    color:var(--muted);
    font-size:9px;
    letter-spacing:.08em;
  }
  .index-foot p{margin:0;color:var(--gold);font-weight:700;letter-spacing:.16em}

  /* ---------- 页脚 ---------- */
  .page-foot{
    display:flex;
    flex-wrap:wrap;
    justify-content:space-between;
    gap:8px 24px;
    padding-top:22px;
    margin-top:26px;
    border-top:1px solid var(--line);
    color:rgba(31,44,39,.44);
    font-size:9px;
    letter-spacing:.12em;
  }

  /* ---------- 弹窗 ---------- */
  .modal{
    position:fixed;
    inset:0;
    z-index:100;
    display:grid;
    place-items:center;
    padding:24px;
    visibility:hidden;
    opacity:0;
    transition:opacity .22s ease, visibility .22s ease;
  }
  .modal.is-open{visibility:visible;opacity:1}
  .modal-backdrop{
    position:absolute;
    inset:0;
    background:rgba(24,34,29,.48);
    backdrop-filter:blur(5px);
    -webkit-backdrop-filter:blur(5px);
  }
  .sheet{
    --region-color:var(--central);
    position:relative;
    width:min(640px, 100%);
    max-height:min(86vh, 820px);
    overflow:auto;
    padding:34px 40px 26px;
    background:
      radial-gradient(120% 90% at 100% 0%, rgba(255,255,255,.92), rgba(255,255,255,0) 58%),
      var(--paper-2);
    border:1px solid rgba(31,44,39,.14);
    border-radius:22px;
    box-shadow:0 34px 90px rgba(17,25,20,.32);
    transform:translateY(16px) scale(.985);
    transition:transform .28s cubic-bezier(.2,.8,.25,1);
    scrollbar-width:thin;
  }
  .modal.is-open .sheet{transform:none}
  .sheet::before{
    content:"";
    position:absolute;
    left:0;top:0;
    width:100%;height:4px;
    background:linear-gradient(90deg, var(--region-color), rgba(255,255,255,0));
  }
  .sheet-close{
    position:absolute;
    top:16px;right:16px;
    z-index:3;
    width:34px;height:34px;
    display:grid;place-items:center;
    border:1px solid rgba(31,44,39,.16);
    border-radius:50%;
    background:rgba(255,253,246,.8);
    color:#4d5a51;
    cursor:pointer;
    transition:background .16s ease, transform .16s ease, color .16s ease;
  }
  .sheet-close:hover,
  .sheet-close:focus-visible{background:#fff;color:var(--accent);transform:rotate(90deg);outline:none}
  .sheet-close svg{width:15px;height:15px}
  .sheet-head{
    position:relative;
    display:flex;
    align-items:flex-start;
    gap:14px;
    padding-right:40px;
  }
  .sheet-badge{
    flex:0 0 auto;
    margin-top:8px;
    padding:4px 9px;
    border:1px solid var(--region-color);
    border-radius:999px;
    color:var(--region-color);
    background:rgba(255,255,255,.38);
    font-size:10px;
    font-weight:700;
    letter-spacing:.16em;
    line-height:1.2;
  }
  .sheet-titles h2{
    margin:0;
    font-family:var(--serif);
    font-size:clamp(32px,5vw,46px);
    line-height:1.12;
    letter-spacing:.08em;
  }
  .sheet-titles p{
    margin:5px 0 0;
    color:#97a096;
    font-size:9px;
    letter-spacing:.26em;
    font-weight:700;
  }
  .sheet-glyph{
    position:absolute;
    right:-14px;top:-34px;
    font-family:var(--serif);
    font-size:128px;
    line-height:1;
    color:var(--region-color);
    opacity:.09;
    pointer-events:none;
    user-select:none;
  }
  .sheet-tagline{
    margin:15px 0 20px;
    padding-left:13px;
    border-left:3px solid var(--region-color);
    font-family:var(--serif);
    font-size:17px;
    font-weight:700;
    letter-spacing:.1em;
    color:#3d4a42;
  }
  .sheet-stats{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    border-top:1px solid var(--line);
    border-bottom:1px solid var(--line);
  }
  .sheet-stats > div{
    padding:13px 14px 12px 0;
    min-width:0;
  }
  .sheet-stats > div + div{
    padding-left:16px;
    border-left:1px solid var(--line);
  }
  .sheet-stats span{
    display:block;
    margin-bottom:4px;
    color:var(--muted);
    font-size:9px;
    letter-spacing:.14em;
  }
  .sheet-stats strong{
    font-family:var(--serif);
    font-size:25px;
    font-weight:700;
    line-height:1.1;
    letter-spacing:.02em;
  }
  .sheet-stats em{
    margin-left:3px;
    font-style:normal;
    color:#8b9389;
    font-size:9px;
    letter-spacing:.04em;
  }
  .sheet-desc{
    margin:19px 0 17px;
    color:#4d5a51;
    font-size:13px;
    line-height:1.95;
    letter-spacing:.035em;
    text-align:justify;
  }
  .sheet-tags{
    display:flex;
    flex-wrap:wrap;
    gap:6px;
    margin-bottom:22px;
  }
  .tag{
    padding:5px 10px;
    border:1px solid rgba(31,44,39,.12);
    border-radius:999px;
    background:rgba(255,255,255,.55);
    color:#536057;
    font-size:10px;
    letter-spacing:.06em;
  }
  .sheet-spots h3{
    display:flex;
    align-items:baseline;
    gap:9px;
    margin:0 0 10px;
    font-family:var(--serif);
    font-size:14px;
    letter-spacing:.1em;
  }
  .sheet-spots h3 span{
    color:#a3aa9f;
    font-family:var(--sans);
    font-size:8px;
    letter-spacing:.2em;
  }
  .sheet-spots ul{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:7px 18px;
    margin:0;
    padding:0;
    list-style:none;
  }
  .sheet-spots li{
    display:flex;
    align-items:center;
    gap:8px;
    color:#46534a;
    font-size:12px;
    letter-spacing:.04em;
  }
  .sheet-spots li::before{
    content:"";
    width:5px;height:5px;
    flex:0 0 auto;
    background:var(--region-color);
    transform:rotate(45deg);
  }
  .sheet-source{
    margin:24px 0 0;
    padding-top:12px;
    border-top:1px dashed var(--line-strong);
    color:rgba(31,44,39,.4);
    font-size:9px;
    letter-spacing:.06em;
  }

  @media (max-width:980px){
    .masthead{grid-template-columns:1fr;grid-template-areas:"brand" "lede" "legend"}
    .legend{justify-content:flex-start;padding-top:4px}
    .atlas{grid-template-columns:1fr}
    .index-card{position:static}
    .index-groups{grid-template-columns:repeat(3,1fr);gap:20px}
    .city-list{grid-template-columns:1fr}
  }
  @media (max-width:640px){
    .page{width:min(100% - 28px, 1180px);padding-top:24px}
    .brand{gap:13px}
    .seal{width:52px;height:52px}
    .seal span{font-size:31px}
    h1{font-size:38px}
    .lede{font-size:12.5px}
    .atlas{padding-top:18px;gap:18px}
    .card-head{padding:15px 16px 13px}
    .card-head h2{font-size:15px}
    .head-hint{display:none}
    .map-shell{margin:12px}
    .card-foot{gap:14px;padding:0 16px 16px}
    .foot-tip{display:none}
    .city-list{grid-template-columns:repeat(2,1fr)}
    .index-groups{grid-template-columns:1fr}
    .city-label{display:none}
    .map-note{display:none}
    .modal{padding:0;place-items:end center}
    .sheet{
      width:100%;
      max-height:88vh;
      border-radius:20px 20px 0 0;
      padding:28px 22px 22px;
    }
    .sheet-titles h2{font-size:34px}
    .sheet-glyph{font-size:96px;right:-8px;top:-24px}
    .sheet-stats strong{font-size:21px}
    .sheet-spots ul{grid-template-columns:1fr 1fr;gap:7px 10px}
    .sheet-desc{font-size:12.5px;line-height:1.85}
    .page-foot{font-size:8px}
  }
  @media (max-width:420px){
    .sheet-stats > div{padding-right:8px}
    .sheet-stats > div + div{padding-left:11px}
    .sheet-stats strong{font-size:19px}
  }
  @media (prefers-reduced-motion:reduce){
    *,*::before,*::after{scroll-behavior:auto !important;transition:none !important;animation:none !important}
  }
</style>
</head>
<body>
<div class="page">
  <header class="masthead">
    <div class="brand">
      <div class="seal" aria-hidden="true"><span>皖</span></div>
      <div>
        <p class="kicker">ANHUI · PROVINCE ATLAS</p>
        <h1>安徽十六城</h1>
      </div>
    </div>
    <p class="lede">从淮北平原到新安江畔，十六座城市各有山河。点击地图上的任一区域，展开它的风物、人物与故事。</p>
    <div class="legend" aria-label="区域图例">
      <span><i style="--c:var(--north)"></i>皖北</span>
      <span><i style="--c:var(--central)"></i>江淮</span>
      <span><i style="--c:var(--south)"></i>皖南</span>
    </div>
  </header>

  <main class="atlas">
    <section class="map-card" aria-labelledby="mapHeading">
      <div class="card-head">
        <h2 id="mapHeading">安徽省行政区划 · 互动地图</h2>
        <span class="head-hint"><i></i>点击城市区域</span>
      </div>
      <div class="map-shell">
        <svg id="anhuiMap" viewBox="0 0 760 980" role="img" aria-labelledby="mapTitle mapDesc">
          <title id="mapTitle">安徽省十六市互动地图</title>
          <desc id="mapDesc">安徽省地图按地级市分为十六个可点击区域，点击任一城市可查看该市简介。</desc>
          <defs>
            <filter id="mapShadow" filterUnits="userSpaceOnUse" x="-20" y="-20" width="800" height="1020">
              <feDropShadow dx="0" dy="12" stdDeviation="13" flood-color="#2a382f" flood-opacity=".17"/>
            </filter>
          </defs>
          <g class="map-cities" id="mapCities" filter="url(#mapShadow)">
          __CITY_PATHS__
          </g>
          <path class="province-line" d="__OUTLINE__"/>
          <g class="map-labels" id="mapLabels" aria-hidden="true">
          __LABELS__
          </g>
        </svg>
        <div class="north-mark" aria-hidden="true">
          <svg viewBox="0 0 24 28"><path d="M12 2 19 24 12 19 5 24Z" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/><path d="M12 6v10" stroke="currentColor" stroke-width="1.1"/></svg>
          <span>N</span>
        </div>
        <span class="map-note">边界示意图 · 非标准地图</span>
      </div>
      <div class="card-foot">
        <span><b>16</b>个地级市</span>
        <span><b>14.01</b>万平方公里</span>
        <span class="foot-tip">点击任意区域查看城市介绍</span>
      </div>
    </section>

    <aside class="index-card" aria-labelledby="indexHeading">
      <div class="index-head">
        <h2 id="indexHeading">城市索引</h2>
        <span>16 CITIES</span>
      </div>
      <p class="index-sub">按区域浏览，或直接点击地图。每个区域都可以打开一张城市名片。</p>
      <div class="index-groups" id="cityList">
        __CITY_INDEX__
      </div>
      <div class="index-foot">
        <p>皖北 · 江淮 · 皖南</p>
        <span>点击查看简介</span>
      </div>
    </aside>
  </main>

  <footer class="page-foot">
    <span>地图边界：DataV.GeoAtlas</span>
    <span>城市介绍据公开资料整理 · 仅作科普展示</span>
  </footer>
</div>

<div class="modal" id="cityModal" aria-hidden="true">
  <div class="modal-backdrop" data-close></div>
  <article class="sheet" role="dialog" aria-modal="true" aria-labelledby="modalTitle" aria-describedby="modalDesc">
    <button class="sheet-close" type="button" data-close aria-label="关闭城市介绍">
      <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 2l12 12M14 2 2 14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
    </button>
    <div class="sheet-head">
      <span class="sheet-badge" id="modalRegion"></span>
      <div class="sheet-titles">
        <h2 id="modalTitle"></h2>
        <p id="modalEn"></p>
      </div>
      <span class="sheet-glyph" id="modalGlyph" aria-hidden="true"></span>
    </div>
    <p class="sheet-tagline" id="modalTagline"></p>
    <div class="sheet-stats">
      <div><span>面积</span><strong id="modalArea"></strong><em>km²</em></div>
      <div><span>常住人口</span><strong id="modalPop"></strong><em>万人</em></div>
      <div><span>所属区域</span><strong id="modalRegionText"></strong><em>地区</em></div>
    </div>
    <p class="sheet-desc" id="modalDesc"></p>
    <div class="sheet-tags" id="modalTags"></div>
    <div class="sheet-spots">
      <h3>城市名片 <span>HIGHLIGHTS</span></h3>
      <ul id="modalSpots"></ul>
    </div>
    <p class="sheet-source">常住人口为 2023 年约数；城市介绍为简要概括，欢迎按需补充。</p>
  </article>
</div>

<script>
(function(){
  "use strict";
  const CITIES = __DATA_JSON__;
  const REGION_COLORS = __REGION_JSON__;

  const modal = document.getElementById("cityModal");
  const sheet = modal.querySelector(".sheet");
  const mapCities = document.getElementById("mapCities");
  const mapLabels = document.getElementById("mapLabels");
  const cityList = document.getElementById("cityList");
  const closeBtn = modal.querySelector(".sheet-close");
  let activeId = null;
  let lastFocused = null;

  const el = {
    region: document.getElementById("modalRegion"),
    title: document.getElementById("modalTitle"),
    en: document.getElementById("modalEn"),
    glyph: document.getElementById("modalGlyph"),
    tagline: document.getElementById("modalTagline"),
    area: document.getElementById("modalArea"),
    pop: document.getElementById("modalPop"),
    regionText: document.getElementById("modalRegionText"),
    desc: document.getElementById("modalDesc"),
    tags: document.getElementById("modalTags"),
    spots: document.getElementById("modalSpots")
  };

  function cityNodes(id){
    return {
      path: document.querySelector('.city[data-city="' + id + '"]'),
      label: document.querySelector('.city-label[data-city="' + id + '"]'),
      item: document.querySelector('.city-item[data-city="' + id + '"]')
    };
  }

  function clearActive(){
    mapCities.classList.remove("has-selection");
    mapLabels.classList.remove("has-selection");
    document.querySelectorAll(".city.is-active, .city-label.is-active, .city-item.is-active")
      .forEach(function(n){ n.classList.remove("is-active"); });
    activeId = null;
  }

  function openCity(id, rememberFocus){
    const city = CITIES[id];
    if(!city) return;
    if(activeId && activeId !== id){
      const prev = cityNodes(activeId);
      [prev.path, prev.label, prev.item].forEach(function(n){ if(n) n.classList.remove("is-active"); });
    }
    activeId = id;
    if(rememberFocus !== false) lastFocused = document.activeElement;

    const nodes = cityNodes(id);
    if(nodes.path) nodes.path.classList.add("is-active");
    if(nodes.label) nodes.label.classList.add("is-active");
    if(nodes.item) nodes.item.classList.add("is-active");
    mapCities.classList.add("has-selection");
    mapLabels.classList.add("has-selection");

    const color = REGION_COLORS[city.region] || "#6f9785";
    sheet.style.setProperty("--region-color", color);
    el.region.textContent = city.region;
    el.title.textContent = city.name;
    el.en.textContent = city.en;
    el.glyph.textContent = city.name.charAt(0);
    el.tagline.textContent = city.tagline;
    el.area.textContent = city.area;
    el.pop.textContent = city.pop;
    el.regionText.textContent = city.region;
    el.desc.textContent = city.desc;

    el.tags.replaceChildren();
    city.tags.forEach(function(t){
      const span = document.createElement("span");
      span.className = "tag";
      span.textContent = t;
      el.tags.appendChild(span);
    });

    el.spots.replaceChildren();
    city.spots.forEach(function(s){
      const li = document.createElement("li");
      li.textContent = s;
      el.spots.appendChild(li);
    });

    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("modal-open");
    window.setTimeout(function(){ closeBtn.focus({preventScroll:true}); }, 60);
  }

  function closeCity(){
    if(!modal.classList.contains("is-open")) return;
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("modal-open");
    clearActive();
    if(lastFocused && typeof lastFocused.focus === "function"){
      lastFocused.focus({preventScroll:true});
    }
    lastFocused = null;
  }

  function bindOpeners(){
    document.querySelectorAll(".city[data-city], .city-item[data-city]").forEach(function(node){
      node.addEventListener("click", function(){ openCity(node.getAttribute("data-city")); });
    });
    document.querySelectorAll(".city[data-city]").forEach(function(node){
      node.addEventListener("keydown", function(e){
        if(e.key === "Enter" || e.key === " "){
          e.preventDefault();
          openCity(node.getAttribute("data-city"));
        }
      });
    });
    modal.querySelectorAll("[data-close]").forEach(function(node){
      node.addEventListener("click", closeCity);
    });
  }

  document.addEventListener("keydown", function(e){
    if(e.key === "Escape") closeCity();
    if(e.key !== "Tab" || !modal.classList.contains("is-open")) return;
    const focusables = sheet.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    if(!focusables.length) return;
    const first = focusables[0], last = focusables[focusables.length - 1];
    if(e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
    else if(!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
  });

  bindOpeners();

  const params = new URLSearchParams(window.location.search);
  const initial = params.get("city") || window.location.hash.replace(/^#/, "");
  if(initial && CITIES[initial]){
    window.setTimeout(function(){ openCity(initial, false); }, 450);
  }
})();
</script>
</body>
</html>
"""

HTML = (
    HTML.replace("__CITY_PATHS__", build_city_paths())
    .replace("__OUTLINE__", build_outline())
    .replace("__LABELS__", build_labels())
    .replace("__CITY_INDEX__", build_index())
    .replace("__DATA_JSON__", DATA_JSON)
    .replace("__REGION_JSON__", REGION_JSON)
)

out = ROOT / "anhui-map.html"
out.write_text(HTML, encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size:,} bytes)")
print(f"cities={len(CITIES)} chars={len(HTML):,}")
