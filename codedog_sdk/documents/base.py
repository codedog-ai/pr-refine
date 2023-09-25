from __future__ import annotations

from typing import Optional

from langchain.schema import Document


class Chapter:
    def __init__(self, raw_chapter: list[str]):
        self.name = raw_chapter[-1]
        self.level = len(raw_chapter)
        self.path = raw_chapter
        self.key = " - ".join(raw_chapter)
        self.children: list[Chapter] = []
        self.parent: Optional[Chapter] = None

    def add_child(self, child: Chapter):
        self.children.append(child)

    def set_parent(self, chapter: Chapter):
        self.parent = chapter

    def pretty_name(self):
        return " " * 2 * self.level + " - " + self.name

    def pretty_index(self):
        return f"{self.name}:\n" + "\n".join(f"  - {c.name}" for c in self.children)


class DocumentIndex:
    def __init__(self):
        self.chapters: list[Chapter] = []
        self.docs: list[Document] = []

        self.root_chapters: list[Chapter] = []
        self._chapter_ids = {}
        self._id_docs = {}

    def get(self, doc_id: str) -> Document:
        return self._id_docs.get(doc_id, None)

    def get_by_chapter(self, chapter: Chapter) -> Document:
        return self._id_docs.get(self._chapter_ids.get(chapter.key, None), None)

    def add_chapter(self, chapter: Chapter, doc: Document, root=False):
        self.chapters.append(chapter)
        self.docs.append(doc)
        doc_id = len(self.docs)
        self._chapter_ids[chapter.key] = doc_id
        self._id_docs[doc_id] = doc

        if root:
            self.root_chapters.append(chapter)

        return doc_id
