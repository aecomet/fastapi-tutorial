from dataclasses import dataclass


@dataclass
class Dpar:
    key: str
    value: str
    ttl: int | None  # 残り TTL（秒）。None は無期限
