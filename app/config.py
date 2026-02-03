from dataclasses import dataclass

@dataclass(frozen=True)
class SecurityConfig:
    # Argon2id parameters
    # memory_cost is in kibibytes (KiB). 65536 KiB = 64 MiB
    memory_cost: int = 65536
    time_cost: int = 3
    parallelism: int = 2

SECURITY = SecurityConfig()
