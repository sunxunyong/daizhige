# -*- coding: utf-8 -*-
"""
中医古籍文献自动分类脚本
根据文件名关键词进行分类
"""

import os
import shutil
from pathlib import Path

# 源目录和目标目录
SOURCE_DIR = r"D:\古代文献所有资料2.0版20140103\医藏"
TARGET_DIR = r"D:\古代文献所有资料2.0版20140103\医藏\医藏_公理化重构"

# 分类规则：关键词到目标路径的映射
CLASSIFICATION_RULES = {
    # ===== 00_基础理论卷 =====
    "00_基础理论卷/01_阴阳学说": [
        "阴阳", "素问", "灵枢", "内经"
    ],
    "00_基础理论卷/02_五行学说": [
        "五行"
    ],
    "00_基础理论卷/03_脏腑理论": [
        "脏腑", "中藏经"
    ],
    "00_基础理论卷/04_经络学说": [
        "经络", "子午流注"
    ],
    "00_基础理论卷/05_气血津液": [
        "气血", "津液"
    ],
    "00_基础理论卷/06_病因病机": [
        "病源", "病机", "诸病源候论", "巢氏"
    ],

    # ===== 01_诊断学卷 =====
    "01_诊断学卷/01_四诊/04_切诊": [
        "脉经", "脉学", "脉法", "诊脉", "三指禅", "濒湖脉学",
        "诊家", "太素脉", "丹医脉法"
    ],
    "01_诊断学卷/01_四诊/01_望诊": [
        "望诊", "察舌", "舌诊", "金镜录"
    ],
    "01_诊断学卷/02_辨证": [
        "辨证", "辨症", "辨证录", "辨证奇闻"
    ],

    # ===== 02_药物学卷 =====
    "02_药物学卷/01_总论/01_本草理论": [
        "本草", "本草纲目", "本草备要", "本草求真", "本草衍义",
        "本草问答", "本草新编", "本草经", "本草图经", "本草品汇",
        "本草述", "本草思辨", "本草蒙筌", "本草崇原", "本草从新",
        "本草便读", "本草乘雅", "本草撮要", "本草分经", "本草害利",
        "本草简要", "本草易读", "本草择要", "本草征要", "本草征要",
        "得配本草", "滇南本草", "证类本草", "雷公", "炮炙", "修治",
        "本经逢原", "本经疏证", "药性", "药对", "药录", "吴氏本草",
        "李氏药录", "海药本草", "食疗本草", "本草拾遗", "删繁本草",
        "四声本草", "药总诀", "食疗"
    ],
    "02_药物学卷/01_总论/03_配伍禁忌": [
        "辅行", "十八反", "十九畏", "畏", "禁"
    ],

    # ===== 03_方剂学卷 =====
    "03_方剂学卷/01_方剂理论": [
        "方论", "古方", "成方", "医方", "方解", "方剂",
        "千金方", "千金要方", "翼方", "外台秘要", "和剂局方",
        "太平惠民和剂局方", "局方", "洪氏集验", "传信", "易简",
        "济生", "世医得效", "永类钤方", "玉机微义", "普济",
        "奇效", "秘传", "扶寿精方", "医方考", "医方集解",
        "成方切用", "古今医统", "赤水元珠"
    ],
    "03_方剂学卷/02_方剂分类/01_解表剂": [
        "伤寒", "金匮", "注解伤寒", "伤寒论", "伤寒金镜",
        "伤寒九十", "伤寒六书", "伤寒兼证", "伤寒审镜",
        "伤寒微旨", "伤寒总病", "伤寒百证", "伤寒溯源",
        "伤寒指掌", "伤寒缵论", "金匮要略", "金匮钩玄",
        "金匮翼", "金匮玉函"
    ],

    # ===== 04_临床各科卷 =====
    # 01_伤寒瘟病
    "04_临床各科卷/01_伤寒瘟病": [
        "温病", "温热", "瘟疫", "疫", "温疫论", "温热经纬",
        "温病条辨", "疫疹一得", "伤寒贯珠", "伤寒大白",
        "伤寒来苏", "伤寒辨证", "伤寒捷诀"
    ],
    # 02_内科
    "04_临床各科卷/02_内科": [
        "内科", "杂病", "证治", "慎柔", "理虚", "虚劳",
        "咳嗽", "痰", "哮", "喘", "肺", "心", "脾", "胃",
        "肝", "肾", "膈", "反胃", "噎", "关格", "肿胀",
        "泄泻", "痢", "滞下", "霍乱", "疟", "疸", "疸病",
        "消渴", "中风", "眩晕", "头痛", "胁痛", "腹痛",
        "腰痛", "疝", "癃闭", "淋", "遗精", "血证", "汗",
        "厥", "痉", "痹", "痿", "颤", "惊悸", "健忘",
        "不寐", "癫", "狂", "痫", "癎", "虫", "蛊",
        "中恶", "中蛊", "癫狂", "痫证", "惊痫", "百合病",
        "狐惑", "阴阳毒", "血痹", "虚劳", "肺痿", "肺痈",
        "胸痹", "心痛", "腹痛", "积聚", "症瘕", "鼓胀"
    ],
    # 03_外科
    "04_临床各科卷/03_外科": [
        "外科", "疡科", "外科精要", "外科正宗", "外科大成",
        "外科全生", "外科枢要", "外科学", "疡医", "痈疽",
        "疔毒", "瘿瘤", "疮疡", "疥癣", "杨梅", "梅毒",
        "花柳", "白喉", "喉", "喉证", "喉科", "玉钥",
        "跌打", "损伤", "金疮", "伤科", "正体", "接骨",
        "疯犬", "虫兽", "蛇伤", "破伤风", "乳痈", "乳岩",
        "痔疮", "瘘", "漏", "梅", "疮", "疔", "疽",
        "疡", "瘰", "疬", "流注", "发背", "对口",
        "风", "瘙", "痒", "丹毒", "斑疹", "痘", "疹"
    ],
    # 04_妇科
    "04_临床各科卷/04_妇科": [
        "妇科", "妇人", "女科", "产后", "胎前", "带下",
        "崩漏", "经", "月经", "子嗣", "种子", "产宝",
        "达生", "女科", "女科准绳", "济阴", "广嗣",
        "女科", "妇人", "胎产", "产科", "乳", "前阴"
    ],
    # 05_儿科
    "04_临床各科卷/05_儿科": [
        "儿科", "幼科", "小儿", "婴", "童", "痘疹",
        "麻疹", "惊风", "疳", "保婴", "幼幼", "慈幼",
        "痘", "疹", "痧", "惊", "疳"
    ],
    # 06_五官科
    "04_临床各科卷/06_五官科": [
        "眼科", "目", "视", "盲", "内障", "外障",
        "耳", "鼻", "齿", "牙", "口", "唇", "咽喉",
        "喉", "音", "声"
    ],
    # 07_针灸科
    "04_临床各科卷/07_针灸科": [
        "针灸", "针", "灸", "甲乙", "铜人", "玉龙",
        "资生", "针灸大成", "针灸大全", "针灸聚英",
        "针灸问对", "子午流注", "灵龟", "飞腾",
        "备急灸", "灸法", "采艾", "艾", "经络",
        "孔穴", "穴位", "俞穴"
    ],

    # ===== 05_医案医话卷 =====
    "05_医案医话卷/01_医案": [
        "医案", "方案", "临证", "治验", "得效", "治例",
        "笔记", "随笔", "类案", "古今医案", "续名医类案",
        "名医类案", "薛氏医案", "寓意草", "临证指南",
        "扫叶庄", "洄溪", "王氏医案", "吴鞠", "丁甘仁",
        "曹仁伯", "程杏轩", "陈莲舫", "丛桂草堂", "爱月庐",
        "程门雪"
    ],
    "05_医案医话卷/02_医话": [
        "医话", "随笔", "读医", "笔花", "冷庐", "归砚",
        "对山", "潜斋", "存存斋", "知医", "质疑", "读素问",
        "研经", "友渔", "先醒斋", "医悟", "医学从众",
        "医学读", "医学妙"
    ],

    # ===== 06_工具参考卷 =====
    "06_工具参考卷/03_综述": [
        "中国医籍", "医籍考", "综", "全书", "大全",
        "古今图书", "图书集成", "医部", "艺文"
    ],
}


def classify_document(filename):
    """根据文件名判断分类"""
    for category, keywords in CLASSIFICATION_RULES.items():
        for keyword in keywords:
            if keyword in filename:
                return category
    # 默认放入临床各科卷/02_内科
    return "04_临床各科卷/02_内科"


def get_metadata_from_filename(filename):
    """从文件名提取元数据"""
    # 移除.txt后缀
    name = filename.replace(".txt", "")

    # 尝试从常见文献中提取作者和朝代
    metadata = {
        "title": name,
        "dynasty": "待考",
        "author": "佚名",
        "type": "待定",
        "concepts": [],
        "axioms": []
    }

    # 已知文献的元数据（可扩展）
    known_docs = {
        "本草纲目": {"dynasty": "明", "author": "李时珍", "type": "本草"},
        "伤寒论": {"dynasty": "汉", "author": "张仲景", "type": "临床"},
        "金匮要略": {"dynasty": "汉", "author": "张仲景", "type": "临床"},
        "黄帝内经素问": {"dynasty": "先秦", "author": "佚名", "type": "理论"},
        "黄帝内经灵枢": {"dynasty": "先秦", "author": "佚名", "type": "理论"},
        "八十一难经": {"dynasty": "汉", "author": "佚名", "type": "理论"},
        "脉经": {"dynasty": "晋", "author": "王叔和", "type": "诊断"},
        "濒湖脉学": {"dynasty": "明", "author": "李时珍", "type": "诊断"},
        "备急千金要方": {"dynasty": "唐", "author": "孙思邈", "type": "方剂"},
        "丹溪心法": {"dynasty": "元", "author": "朱震亨", "type": "临床"},
        "景岳全书": {"dynasty": "明", "author": "张介宾", "type": "临床"},
        "温病条辨": {"dynasty": "清", "author": "吴鞠通", "type": "临床"},
        "证治准绳": {"dynasty": "明", "author": "王肯堂", "type": "临床"},
        "医宗金鉴": {"dynasty": "清", "author": "吴谦", "type": "综合"},
        "脾胃论": {"dynasty": "金", "author": "李东垣", "type": "理论"},
        "儒门事亲": {"dynasty": "金", "author": "张从正", "type": "临床"},
        "格致余论": {"dynasty": "元", "author": "朱震亨", "type": "理论"},
        "局方发挥": {"dynasty": "元", "author": "朱震亨", "type": "理论"},
        "本草备要": {"dynasty": "清", "author": "汪昂", "type": "本草"},
        "医方集解": {"dynasty": "清", "author": "汪昂", "type": "方剂"},
        "成方切用": {"dynasty": "清", "author": "吴仪洛", "type": "方剂"},
        "中藏经": {"dynasty": "汉", "author": "华佗", "type": "理论"},
        "褚氏遗书": {"dynasty": "南齐", "author": "褚澄", "type": "理论"},
        "扁鹊心书": {"dynasty": "宋", "author": "窦材", "type": "临床"},
        "素问玄机原病式": {"dynasty": "金", "author": "刘完素", "type": "理论"},
        "宣明论方": {"dynasty": "金", "author": "刘完素", "type": "临床"},
        "儒门事亲": {"dynasty": "金", "author": "张从正", "type": "临床"},
        "内外伤辨惑论": {"dynasty": "金", "author": "李东垣", "type": "理论"},
        "兰室秘藏": {"dynasty": "金", "author": "李东垣", "type": "临床"},
        "此事难知": {"dynasty": "元", "author": "王好古", "type": "理论"},
        "汤液本草": {"dynasty": "元", "author": "王好古", "type": "本草"},
        "世医得效方": {"dynasty": "元", "author": "危亦林", "type": "方剂"},
        "外科精要": {"dynasty": "宋", "author": "陈自明", "type": "外科"},
        "外科正宗": {"dynasty": "明", "author": "陈实功", "type": "外科"},
        "妇人大全良方": {"dynasty": "宋", "author": "陈自明", "type": "妇科"},
        "济阴纲目": {"dynasty": "明", "author": "武之望", "type": "妇科"},
        "幼科发挥": {"dynasty": "明", "author": "万全", "type": "儿科"},
        "幼幼集成": {"dynasty": "清", "author": "陈复正", "type": "儿科"},
        "针灸大成": {"dynasty": "明", "author": "杨继洲", "type": "针灸"},
        "针灸甲乙经": {"dynasty": "晋", "author": "皇甫谧", "type": "针灸"},
        "铜人针灸图经": {"dynasty": "宋", "author": "王惟一", "type": "针灸"},
    }

    # 检查是否是已知文献
    for doc_name, doc_meta in known_docs.items():
        if doc_name in name:
            metadata.update(doc_meta)
            break

    # 根据分类确定相关公理
    category = classify_document(filename)
    if "基础理论" in category or "阴阳" in category or "五行" in category:
        metadata["axioms"] = ["A1", "A2", "A3"]
        metadata["concepts"] = ["阴阳", "五行", "脏腑"]
    elif "诊断" in category:
        metadata["axioms"] = ["R1"]
        metadata["concepts"] = ["四诊", "八纲", "辨证"]
    elif "药物" in category or "本草" in category:
        metadata["axioms"] = ["A2", "A3"]
        metadata["concepts"] = ["四气五味", "归经", "升降浮沉"]
    elif "方剂" in category:
        metadata["axioms"] = ["A3", "D3"]
        metadata["concepts"] = ["君臣佐使", "配伍", "方剂"]
    elif "临床" in category:
        metadata["axioms"] = ["A1", "A3", "R1", "R2"]
        metadata["concepts"] = ["辨证论治", "治则", "疾病"]

    return metadata


def generate_metadata_header(filename):
    """生成元数据头部"""
    metadata = get_metadata_from_filename(filename)
    category = classify_document(filename)

    header = f'''================================================================================
                           中医古籍文献 - 公理化重构版本
================================================================================

【元数据】
文献名称：{metadata['title']}
朝代：{metadata['dynasty']}
作者：{metadata['author']}
所属类别：{category}
核心概念：{', '.join(metadata['concepts'])}
相关公理：{', '.join(metadata['axioms'])}
文献类型：{metadata['type']}

================================================================================
                                    正文开始
================================================================================

'''
    return header


def main():
    """主函数"""
    print("=" * 80)
    print("中医古籍文献公理化重构 - 自动分类脚本")
    print("=" * 80)

    # 获取所有txt文件
    source_path = Path(SOURCE_DIR)
    txt_files = list(source_path.glob("*.txt"))

    print(f"\n找到 {len(txt_files)} 个文本文件\n")

    # 统计分类
    classification_stats = {}
    processed_files = []
    unclassified_files = []

    for txt_file in txt_files:
        filename = txt_file.name

        # 跳过已处理的文件和临时文件
        if "公理化" in filename or "tmp" in filename:
            continue

        # 获取分类
        category = classify_document(filename)

        # 统计
        if category not in classification_stats:
            classification_stats[category] = []
        classification_stats[category].append(filename)

        # 确定目标路径
        target_path = Path(TARGET_DIR) / category / filename
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # 复制文件
        try:
            shutil.copy2(txt_file, target_path)
            processed_files.append((filename, category))

            # 添加元数据头部
            metadata_header = generate_metadata_header(filename)

            # 读取原内容
            with open(target_path, 'r', encoding='utf-8', errors='ignore') as f:
                original_content = f.read()

            # 写入带元数据的版本
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(metadata_header)
                f.write(original_content)

            print(f"[OK] {filename[:30]:<30} -> {category}")

        except Exception as e:
            print(f"[ERROR] {filename}: {e}")
            unclassified_files.append(filename)

    # 输出统计
    print("\n" + "=" * 80)
    print("分类统计")
    print("=" * 80)

    for category, files in sorted(classification_stats.items()):
        print(f"\n{category}: {len(files)} 个文件")
        for f in files[:5]:  # 只显示前5个
            print(f"  - {f}")
        if len(files) > 5:
            print(f"  ... 还有 {len(files) - 5} 个文件")

    print(f"\n\n总计处理: {len(processed_files)} 个文件")
    print(f"未处理: {len(unclassified_files)} 个文件")

    # 保存分类报告
    report_path = Path(TARGET_DIR) / "分类报告.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("中医古籍文献分类报告\n")
        f.write("=" * 80 + "\n\n")

        for category, files in sorted(classification_stats.items()):
            f.write(f"\n{category}: {len(files)} 个文件\n")
            f.write("-" * 80 + "\n")
            for filename in files:
                f.write(f"  {filename}\n")

        f.write(f"\n\n总计处理: {len(processed_files)} 个文件\n")

    print(f"\n分类报告已保存到: {report_path}")


if __name__ == "__main__":
    main()
