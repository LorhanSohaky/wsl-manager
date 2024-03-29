from typing import TypedDict, Optional
from typing_extensions import NotRequired


class TypedSystem(TypedDict):
    id: NotRequired[str]
    name: str
    state: NotRequired[str]
    version: str
    base_path: str
    default_user: int


class System:
    def __init__(
        self,
        id: Optional[str],
        name: str,
        state: Optional[str],
        version: str,
        base_path: str,
        default_user: int,
    ):
        self.id = id
        self.name = name
        self.state = state
        self.version = version
        self.base_path = base_path
        self.default_user = default_user

    def __repr__(self):
        return (
            f"System(name={self.name}, state={self.state},"
            f" version={self.version})"
        )

    def __str__(self):
        return f"System {self.name} with state {self.state}"

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.name + self.state + self.version)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "version": self.version,
            "base_path": self.base_path,
        }

    @classmethod
    def from_dict(cls, data: TypedSystem):
        return cls(
            data.get("id"),
            data["name"],
            data.get("state"),
            data["version"],
            data["base_path"],
            data["default_user"],
        )

    @classmethod
    def is_running(cls, system: "System") -> bool:
        return system.state != "Stopped"

    @property
    def running(self) -> bool:
        return self.__class__.is_running(self)
