from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

# 示例配置数据
SAMPLE_URL = "https://mhome-i-game.com.cn"
SAMPLE_KEYWORDS = ["爱游戏", "游戏社区", "手游攻略"]

@dataclass
class KeywordNote:
    """
    关键词笔记的数据结构，用于存储单一关键词及其相关信息。
    """
    keyword: str
    note: str
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    source_url: Optional[str] = None

    def to_dict(self) -> dict:
        """将笔记对象转换为字典格式"""
        return {
            "keyword": self.keyword,
            "note": self.note,
            "created_at": self.created_at.isoformat(),
            "tags": self.tags,
            "source_url": self.source_url,
        }

    def formatted_brief(self) -> str:
        """返回简短格式化字符串"""
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        src = self.source_url or "无来源"
        return f"[{self.keyword}] {self.note[:50]}... ({src}) 标签: {tag_str}"


@dataclass
class KeywordNoteCollection:
    """
    管理多个关键词笔记的集合类，并提供格式化输出功能。
    """
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, keyword: str, note: str, tags: Optional[List[str]] = None,
                 source_url: Optional[str] = None) -> KeywordNote:
        """添加一条新的关键词笔记"""
        new_note = KeywordNote(
            keyword=keyword,
            note=note,
            tags=tags or [],
            source_url=source_url
        )
        self.notes.append(new_note)
        return new_note

    def search_by_keyword(self, keyword: str) -> List[KeywordNote]:
        """根据关键词精确查找笔记"""
        return [note for note in self.notes if note.keyword == keyword]

    def search_by_tag(self, tag: str) -> List[KeywordNote]:
        """根据标签查找笔记"""
        return [note for note in self.notes if tag in note.tags]

    def format_all_notes(self, include_source: bool = True) -> str:
        """将所有笔记格式化为可打印的字符串"""
        if not self.notes:
            return "暂无笔记。"

        lines = ["========== 关键词笔记列表 =========="]
        for idx, note in enumerate(self.notes, 1):
            lines.append(f"笔记 #{idx}")
            lines.append(f"  关键词: {note.keyword}")
            lines.append(f"  笔记内容: {note.note}")
            lines.append(f"  创建时间: {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if note.tags:
                lines.append(f"  标签: {', '.join(note.tags)}")
            if include_source and note.source_url:
                lines.append(f"  来源: {note.source_url}")
            lines.append("---")
        return "\n".join(lines)

    def export_to_dicts(self) -> List[dict]:
        """将所有笔记导出为字典列表，便于 JSON 序列化"""
        return [note.to_dict() for note in self.notes]


# 以下为示例用法，直接运行此脚本将展示功能
if __name__ == "__main__":
    # 创建集合
    collection = KeywordNoteCollection()

    # 添加一些示例笔记（包含核心关键词和关联 URL）
    collection.add_note(
        keyword="爱游戏",
        note="这是一个专注于游戏社区的平台，提供大量手游攻略和玩家交流功能。",
        tags=["游戏", "社区", "攻略"],
        source_url=SAMPLE_URL
    )

    collection.add_note(
        keyword="爱游戏",
        note="爱游戏平台最近推出了新的互动活动，吸引了大量玩家参与。",
        tags=["活动", "互动"],
        source_url=SAMPLE_URL
    )

    collection.add_note(
        keyword="手游攻略",
        note="针对热门手游的详细攻略，包括新手教程、角色培养和副本通关技巧。",
        tags=["攻略", "手游"],
        source_url=SAMPLE_URL
    )

    # 演示格式化输出
    print(collection.format_all_notes())

    # 演示搜索
    print("\n搜索关键词 '爱游戏' 的笔记：")
    for note in collection.search_by_keyword("爱游戏"):
        print(note.formatted_brief())

    print("\n搜索标签 '攻略' 的笔记：")
    for note in collection.search_by_tag("攻略"):
        print(note.formatted_brief())