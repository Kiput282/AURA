import json
from pathlib import Path

from loguru import logger

from aura.journal.journal_entry import JournalEntry


class ProjectJournal:
    """
    File-based project journal for AURA.

    Current format:
    - JSON Lines
    - one journal entry per line
    - stored in data/journal/aura_journal.jsonl
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.journal_dir = self.project_root / "data" / "journal"
        self.journal_file = self.journal_dir / "aura_journal.jsonl"

        self.journal_dir.mkdir(parents=True, exist_ok=True)
        self.journal_file.touch(exist_ok=True)

        logger.info(f"ProjectJournal initialized at {self.journal_file}")

    def save(self, entry: JournalEntry) -> None:
        with self.journal_file.open("a", encoding="utf-8") as file:
            file.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")

        logger.info(f"Journal entry saved: {entry.id}")

    def add(
        self,
        title: str,
        content: str,
        metadata: dict | None = None,
    ) -> JournalEntry:
        entry = JournalEntry(
            title=title,
            content=content,
            metadata=metadata or {},
        )
        self.save(entry)
        return entry

    def list_all(self) -> list[JournalEntry]:
        if not self.journal_file.exists():
            return []

        entries: list[JournalEntry] = []
        lines = self.journal_file.read_text(encoding="utf-8").splitlines()

        for line in lines:
            if not line.strip():
                continue

            try:
                data = json.loads(line)
                entries.append(JournalEntry.from_dict(data))
            except Exception as error:
                logger.exception(f"Failed to load journal line: {error}")

        return entries

    def list_recent(self, limit: int = 5) -> list[JournalEntry]:
        return self.list_all()[-limit:]

    def count(self) -> int:
        return len(self.list_all())
