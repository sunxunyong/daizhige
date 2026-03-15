# -*- coding: utf-8 -*-
"""
中医知识图谱生成脚本
生成概念节点、关系网络和索引文件
"""

import os
import json
from pathlib import Path
from collections import defaultdict

# 源目录
SOURCE_DIR = r"D:\古代文献所有资料2.0版20140103\医藏\医藏_公理化重构"
OUTPUT_DIR = r"D:\古代文献所有资料2.0版20140103\医藏\医藏_公理化重构\06_工具参考卷"


# 中医核心概念定义
TCM_CONCEPTS = {
    # 哲学基础
    "阴阳": {
        "id": "C001",
        "type": "哲学概念",
        "definition": "万物皆有阴阳二性，相互对立、相互依存、相互转化",
        "axiom": "A1",
        "attributes": ["对立", "互根", "消长", "转化"]
    },
    "五行": {
        "id": "C002",
        "type": "哲学概念",
        "definition": "木火土金水五种物质及其运动变化",
        "axiom": "A2",
        "attributes": ["木", "火", "土", "金", "水", "相生", "相克"]
    },

    # 脏腑系统
    "心": {
        "id": "C101",
        "type": "脏腑",
        "definition": "主血脉、藏神，开窍于舌",
        "axiom": "A3",
        "attributes": ["君主之官", "主血脉", "藏神", "开窍于舌", "在志为喜"]
    },
    "肝": {
        "id": "C102",
        "type": "脏腑",
        "definition": "主疏泄、藏血，开窍于目",
        "axiom": "A3",
        "attributes": ["将军之官", "主疏泄", "藏血", "开窍于目", "在志为怒"]
    },
    "脾": {
        "id": "C103",
        "type": "脏腑",
        "definition": "主运化、统血，开窍于口",
        "axiom": "A3",
        "attributes": ["仓廪之官", "主运化", "统血", "开窍于口", "在志为思"]
    },
    "肺": {
        "id": "C104",
        "type": "脏腑",
        "definition": "主气、司呼吸，开窍于鼻",
        "axiom": "A3",
        "attributes": ["相傅之官", "主气", "司呼吸", "开窍于鼻", "在志为悲"]
    },
    "肾": {
        "id": "C105",
        "type": "脏腑",
        "definition": "藏精、主水、纳气，开窍于耳",
        "axiom": "A3",
        "attributes": ["作强之官", "藏精", "主水", "纳气", "开窍于耳", "在志为恐"]
    },
    "胆": {
        "id": "C106",
        "type": "脏腑",
        "definition": "贮存和排泄胆汁，主决断",
        "axiom": "A3",
        "attributes": ["中正之官", "藏胆汁", "主决断"]
    },
    "胃": {
        "id": "C107",
        "type": "脏腑",
        "definition": "受纳腐熟水谷",
        "axiom": "A3",
        "attributes": ["水谷之海", "受纳", "腐熟"]
    },
    "小肠": {
        "id": "C108",
        "type": "脏腑",
        "definition": "受盛化物，泌别清浊",
        "axiom": "A3",
        "attributes": ["受盛之官", "化物", "泌别清浊"]
    },
    "大肠": {
        "id": "C109",
        "type": "脏腑",
        "definition": "传导糟粕",
        "axiom": "A3",
        "attributes": ["传导之官", "传化糟粕"]
    },
    "膀胱": {
        "id": "C110",
        "type": "脏腑",
        "definition": "贮存尿液",
        "axiom": "A3",
        "attributes": ["州都之官", "藏尿", "气化"]
    },
    "三焦": {
        "id": "C111",
        "type": "脏腑",
        "definition": "主持诸气，通行水道",
        "axiom": "A3",
        "attributes": ["决渎之官", "主持诸气", "通行水道"]
    },

    # 经络系统
    "十二正经": {
        "id": "C201",
        "type": "经络",
        "definition": "手足三阴三经，运行气血的主要通道",
        "axiom": "A5",
        "attributes": ["手太阴肺经", "手阳明大肠经", "足阳明胃经", "足太阴脾经",
                      "手少阴心经", "手太阳小肠经", "足太阳膀胱经", "足少阴肾经",
                      "手厥阴心包经", "手少阳三焦经", "足少阳胆经", "足厥阴肝经"]
    },
    "奇经八脉": {
        "id": "C202",
        "type": "经络",
        "definition": "督、任、冲、带、阴阳跷、阴阳维八脉",
        "axiom": "A5",
        "attributes": ["督脉", "任脉", "冲脉", "带脉", "阴跷脉", "阳跷脉", "阴维脉", "阳维脉"]
    },

    # 气血津液
    "气": {
        "id": "C301",
        "type": "生命物质",
        "definition": "人体生命活动的动力",
        "axiom": "A4",
        "attributes": ["推动", "温煦", "防御", "固摄", "气化"]
    },
    "血": {
        "id": "C302",
        "type": "生命物质",
        "definition": "循行于脉中的红色液体，濡养全身",
        "axiom": "A4",
        "attributes": ["濡养", "藏神", "化源于脾胃", "心主血", "肝藏血", "脾统血"]
    },
    "津液": {
        "id": "C303",
        "type": "生命物质",
        "definition": "机体一切正常水液的总称",
        "axiom": "A4",
        "attributes": ["津", "液", "滋润", "濡养"]
    },

    # 病因病机
    "六淫": {
        "id": "C401",
        "type": "病因",
        "definition": "风、寒、暑、湿、燥、火六种外感病邪",
        "axiom": "D1",
        "attributes": ["风邪", "寒邪", "暑邪", "湿邪", "燥邪", "火邪"]
    },
    "七情": {
        "id": "C402",
        "type": "病因",
        "definition": "喜、怒、忧、思、悲、恐、惊七种情志变化",
        "axiom": "D1",
        "attributes": ["喜", "怒", "忧", "思", "悲", "恐", "惊"]
    },

    # 诊断方法
    "四诊": {
        "id": "C501",
        "type": "诊断方法",
        "definition": "望、闻、问、切四种诊断方法",
        "axiom": "R1",
        "attributes": ["望诊", "闻诊", "问诊", "切诊"]
    },
    "八纲": {
        "id": "C502",
        "type": "辨证方法",
        "definition": "表、里、寒、热、虚、实、阴、阳八类证候",
        "axiom": "R1",
        "attributes": ["表证", "里证", "寒证", "热证", "虚证", "实证", "阴证", "阳证"]
    },
    "六经辨证": {
        "id": "C503",
        "type": "辨证方法",
        "definition": "太阳、阳明、少阳、太阴、少阴、厥阴六经病证",
        "axiom": "R1",
        "attributes": ["太阳病", "阳明病", "少阳病", "太阴病", "少阴病", "厥阴病"]
    },
    "卫气营血辨证": {
        "id": "C504",
        "type": "辨证方法",
        "definition": "温热病发展的四个阶段",
        "axiom": "R1",
        "attributes": ["卫分证", "气分证", "营分证", "血分证"]
    },

    # 治疗方法
    "治则": {
        "id": "C601",
        "type": "治疗原则",
        "definition": "治疗疾病的基本原则",
        "axiom": "D3",
        "attributes": ["治病求本", "扶正祛邪", "调整阴阳", "三因制宜"]
    },
    "八法": {
        "id": "C602",
        "type": "治疗方法",
        "definition": "汗、吐、下、和、温、清、消、补八种治法",
        "axiom": "D3",
        "attributes": ["汗法", "吐法", "下法", "和法", "温法", "清法", "消法", "补法"]
    },

    # 药物理论
    "四气五味": {
        "id": "C701",
        "type": "药性理论",
        "definition": "寒热温凉四气，酸苦甘辛咸五味",
        "axiom": "A3",
        "attributes": ["寒", "热", "温", "凉", "酸", "苦", "甘", "辛", "咸"]
    },
    "升降浮沉": {
        "id": "C702",
        "type": "药性理论",
        "definition": "药物作用趋向",
        "axiom": "A3",
        "attributes": ["升", "降", "浮", "沉"]
    },
    "归经": {
        "id": "C703",
        "type": "药性理论",
        "definition": "药物对某经某脏腑的选择性作用",
        "axiom": "A3",
        "attributes": ["十二经归经", "脏腑归经"]
    },

    # 方剂理论
    "君臣佐使": {
        "id": "C801",
        "type": "方剂配伍",
        "definition": "方剂组成的基本原则",
        "axiom": "D3",
        "attributes": ["君药", "臣药", "佐药", "使药"]
    },
    "七情和合": {
        "id": "C802",
        "type": "方剂配伍",
        "definition": "药物配伍的七种关系",
        "axiom": "D3",
        "attributes": ["单行", "相须", "相使", "相畏", "相杀", "相恶", "相反"]
    },
}


# 概念关系定义
CONCEPT_RELATIONS = [
    # 阴阳关系
    {"from": "阴阳", "to": "五行", "type": "包含", "description": "阴阳五行是统一的哲学体系"},
    {"from": "阴阳", "to": "心", "type": "属性", "description": "心属阳"},
    {"from": "阴阳", "to": "肾", "type": "属性", "description": "肾属阴"},

    # 五行关系
    {"from": "五行", "to": "心", "type": "对应", "description": "心属火"},
    {"from": "五行", "to": "肝", "type": "对应", "description": "肝属木"},
    {"from": "五行", "to": "脾", "type": "对应", "description": "脾属土"},
    {"from": "五行", "to": "肺", "type": "对应", "description": "肺属金"},
    {"from": "五行", "to": "肾", "type": "对应", "description": "肾属水"},

    # 五行相生
    {"from": "肝", "to": "心", "type": "相生", "description": "木生火"},
    {"from": "心", "to": "脾", "type": "相生", "description": "火生土"},
    {"from": "脾", "to": "肺", "type": "相生", "description": "土生金"},
    {"from": "肺", "to": "肾", "type": "相生", "description": "金生水"},
    {"from": "肾", "to": "肝", "type": "相生", "description": "水生木"},

    # 五行相克
    {"from": "肝", "to": "脾", "type": "相克", "description": "木克土"},
    {"from": "脾", "to": "肾", "type": "相克", "description": "土克水"},
    {"from": "肾", "to": "心", "type": "相克", "description": "水克火"},
    {"from": "心", "to": "肺", "type": "相克", "description": "火克金"},
    {"from": "肺", "to": "肝", "type": "相克", "description": "金克木"},

    # 脏腑表里关系
    {"from": "心", "to": "小肠", "type": "表里", "description": "心与小肠相表里"},
    {"from": "肝", "to": "胆", "type": "表里", "description": "肝与胆相表里"},
    {"from": "脾", "to": "胃", "type": "表里", "description": "脾与胃相表里"},
    {"from": "肺", "to": "大肠", "type": "表里", "description": "肺与大肠相表里"},
    {"from": "肾", "to": "膀胱", "type": "表里", "description": "肾与膀胱相表里"},
    {"from": "心包", "to": "三焦", "type": "表里", "description": "心包与三焦相表里"},

    # 气血关系
    {"from": "气", "to": "血", "type": "生成", "description": "气为血之帅"},
    {"from": "血", "to": "气", "type": "承载", "description": "血为气之母"},
    {"from": "心", "to": "血", "type": "主管", "description": "心主血"},
    {"from": "肝", "to": "血", "type": "贮藏", "description": "肝藏血"},
    {"from": "脾", "to": "血", "type": "统摄", "description": "脾统血"},

    # 经络关系
    {"from": "十二正经", "to": "脏腑", "type": "联络", "description": "经络联络脏腑"},
    {"from": "奇经八脉", "to": "十二正经", "type": "统摄", "description": "奇经八脉统摄十二正经"},

    # 诊断关系
    {"from": "四诊", "to": "八纲", "type": "输入", "description": "四诊为辨证提供依据"},
    {"from": "八纲", "to": "六经辨证", "type": "基础", "description": "八纲是六经辨证的基础"},
    {"from": "八纲", "to": "卫气营血辨证", "type": "基础", "description": "八纲是卫气营血辨证的基础"},

    # 病因病机关系
    {"from": "六淫", "to": "表证", "type": "导致", "description": "外感六淫导致表证"},
    {"from": "七情", "to": "里证", "type": "导致", "description": "内伤七情导致里证"},
    {"from": "阴阳", "to": "疾病", "type": "失衡", "description": "阴阳失衡导致疾病"},

    # 治疗关系
    {"from": "八纲", "to": "八法", "type": "对应", "description": "辨证论治"},
    {"from": "八法", "to": "君臣佐使", "type": "指导", "description": "治法指导方剂配伍"},

    # 药物关系
    {"from": "四气五味", "to": "归经", "type": "决定", "description": "药性决定归经"},
    {"from": "君臣佐使", "to": "七情和合", "type": "配合", "description": "配伍原则"},
]


def generate_knowledge_graph():
    """生成知识图谱JSON文件"""
    graph = {
        "nodes": [],
        "edges": [],
        "metadata": {
            "title": "中医知识图谱",
            "description": "基于公理化重构的中医概念知识图谱",
            "version": "1.0",
            "axioms": {
                "A1": "阴阳公理 - 万物皆有阴阳二性",
                "A2": "五行公理 - 木火土金水相生相克",
                "A3": "脏腑公理 - 五脏六腑功能协调",
                "A4": "气血公理 - 气血调和则健康",
                "A5": "经络公理 - 经络运行气血"
            }
        }
    }

    # 添加概念节点
    for name, concept in TCM_CONCEPTS.items():
        node = {
            "id": concept["id"],
            "name": name,
            "type": concept["type"],
            "definition": concept["definition"],
            "axiom": concept["axiom"],
            "attributes": concept["attributes"]
        }
        graph["nodes"].append(node)

    # 添加关系边
    for rel in CONCEPT_RELATIONS:
        from_id = TCM_CONCEPTS.get(rel["from"], {}).get("id", "")
        to_id = TCM_CONCEPTS.get(rel["to"], {}).get("id", "")

        if from_id and to_id:
            edge = {
                "from": from_id,
                "to": to_id,
                "from_name": rel["from"],
                "to_name": rel["to"],
                "type": rel["type"],
                "description": rel["description"]
            }
            graph["edges"].append(edge)

    # 保存JSON文件
    output_path = Path(OUTPUT_DIR) / "02_图谱" / "tcm_knowledge_graph.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

    print(f"[OK] 知识图谱已生成: {output_path}")
    print(f"     节点数: {len(graph['nodes'])}")
    print(f"     边数: {len(graph['edges'])}")

    return graph


def generate_concept_index():
    """生成概念索引文件"""
    index_lines = []
    index_lines.append("=" * 80)
    index_lines.append("中医知识概念索引")
    index_lines.append("=" * 80)
    index_lines.append("")

    # 按类型分组
    by_type = defaultdict(list)
    for name, concept in TCM_CONCEPTS.items():
        by_type[concept["type"]].append((name, concept))

    # 生成索引
    for concept_type, concepts in sorted(by_type.items()):
        index_lines.append(f"\n【{concept_type}】")
        index_lines.append("-" * 80)

        for name, concept in sorted(concepts):
            index_lines.append(f"\n{name} ({concept['id']})")
            index_lines.append(f"  定义: {concept['definition']}")
            index_lines.append(f"  公理: {concept['axiom']}")
            index_lines.append(f"  属性: {', '.join(concept['attributes'][:3])}...")

    # 保存索引文件
    output_path = Path(OUTPUT_DIR) / "01_索引" / "概念索引.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(index_lines))

    print(f"[OK] 概念索引已生成: {output_path}")


def generate_axiom_summary():
    """生成公理摘要文件"""
    summary_lines = []
    summary_lines.append("=" * 80)
    summary_lines.append("中医知识公理化体系摘要")
    summary_lines.append("=" * 80)
    summary_lines.append("")

    summary_lines.append("一、基础公理层 (Axioms)")
    summary_lines.append("-" * 80)
    summary_lines.append("")
    summary_lines.append("【A1. 阴阳公理】")
    summary_lines.append("  表述: 万物皆有阴阳二性，阴阳相互对立、相互依存、相互转化")
    summary_lines.append("  形式化: ∀x (Yin(x) ⊕ Yang(x)) ∧ (Yin(x) ↔ ¬Yang(x))")
    summary_lines.append("  推论: 阴阳平衡则健康，阴阳失衡则疾病")
    summary_lines.append("")

    summary_lines.append("【A2. 五行公理】")
    summary_lines.append("  表述: 宇宙万物可归类为木火土金水五行，五行之间存在相生相克关系")
    summary_lines.append("  元素集: Elements = {木, 火, 土, 金, 水}")
    summary_lines.append("  相生关系: 木→火→土→金→水→木")
    summary_lines.append("  相克关系: 木→土→水→火→金→木")
    summary_lines.append("")

    summary_lines.append("【A3. 脏腑公理】")
    summary_lines.append("  表述: 人体以五脏六腑为核心，各有特定功能，相互协调")
    summary_lines.append("  五脏: 心、肝、脾、肺、肾（藏精气而不泻）")
    summary_lines.append("  六腑: 胆、胃、大肠、小肠、膀胱、三焦（传化物而不藏）")
    summary_lines.append("")

    summary_lines.append("【A4. 气血公理】")
    summary_lines.append("  表述: 气为血之帅，血为气之母，气血调和则生命旺盛")
    summary_lines.append("  气的功能: 推动、温煦、防御、固摄、气化")
    summary_lines.append("  血的功能: 濡养、藏神")
    summary_lines.append("")

    summary_lines.append("【A5. 经络公理】")
    summary_lines.append("  表述: 经络是运行气血、联络脏腑肢节的通道系统")
    summary_lines.append("  十二正经: 手足三阴三经")
    summary_lines.append("  奇经八脉: 督、任、冲、带、阴跷、阳跷、阴维、阳维")
    summary_lines.append("")

    summary_lines.append("\n二、基本定义层 (Definitions)")
    summary_lines.append("-" * 80)
    summary_lines.append("")
    summary_lines.append("【D1. 疾病定义】")
    summary_lines.append("  定义: 疾病是阴阳失衡、气血失调、脏腑功能失常的病理状态")
    summary_lines.append("  分类: 外感六淫、内伤七情、饮食劳倦、虫兽外伤")
    summary_lines.append("")

    summary_lines.append("【D2. 证候定义】")
    summary_lines.append("  定义: 证候是疾病在某一阶段的病理概括，反映疾病当前的病位与病性")
    summary_lines.append("  八纲: 表里、寒热、虚实、阴阳")
    summary_lines.append("")

    summary_lines.append("【D3. 治则定义】")
    summary_lines.append("  定义: 治疗原则是调整阴阳、补虚泻实、扶正祛邪")
    summary_lines.append("  正治: 寒者热之、热者寒之、虚者补之、实者泻之")
    summary_lines.append("  反治: 热因热用、寒因寒用、通因通用、塞因塞用")
    summary_lines.append("")

    summary_lines.append("\n三、演绎规则层 (Rules)")
    summary_lines.append("-" * 80)
    summary_lines.append("")
    summary_lines.append("【R1. 辨证规则】")
    summary_lines.append("  - 表里判定: 病位浅者为表，深者为里")
    summary_lines.append("  - 寒热判定: 恶寒喜热为寒，恶热喜冷为热")
    summary_lines.append("  - 虚实判定: 正气不足为虚，邪气亢盛为实")
    summary_lines.append("  - 阴阳判定: 阳盛则热，阴盛则寒；阳虚则寒，阴虚则热")
    summary_lines.append("")

    summary_lines.append("【R2. 脏腑相关规则】")
    summary_lines.append("  - 五行生克: 某脏病变可影响相生或相克的脏腑")
    summary_lines.append("  - 表里关系: 脏腑相表里，病变可相互影响")
    summary_lines.append("  - 开窍主项: 心开窍于舌、肝开窍于目、脾开窍于口、肺开窍于鼻、肾开窍于耳")
    summary_lines.append("")

    summary_lines.append("【R3. 经络循行规则】")
    summary_lines.append("  - 走向规律: 手足三阴三经的走向规律")
    summary_lines.append("  - 交接规律: 阴经与阳经的交接规律")
    summary_lines.append("  - 流注时序: 十二经气血流注的时间顺序")
    summary_lines.append("")

    # 保存摘要文件
    output_path = Path(OUTPUT_DIR) / "03_综述" / "公理体系摘要.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary_lines))

    print(f"[OK] 公理体系摘要已生成: {output_path}")


def main():
    """主函数"""
    print("=" * 80)
    print("中医知识图谱生成工具")
    print("=" * 80)
    print()

    # 生成知识图谱
    print("生成知识图谱...")
    graph = generate_knowledge_graph()

    # 生成概念索引
    print("\n生成概念索引...")
    generate_concept_index()

    # 生成公理摘要
    print("\n生成公理体系摘要...")
    generate_axiom_summary()

    print("\n" + "=" * 80)
    print("知识图谱生成完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()
