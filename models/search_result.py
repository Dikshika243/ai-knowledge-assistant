from dataclasses import dataclass


@dataclass
class SearchResult:
    documents: list[str]
    metadatas: list[dict]