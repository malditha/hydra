# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from omegaconf import MISSING

from hydra.types import TargetConf


def verify_hydra_pytest_plugin_not_installed() -> None:
    try:
        # This check can be removed in 1.1
        import hydra_pytest_plugin  # type: ignore

    except ImportError:
        hydra_pytest_plugin = None

    if hydra_pytest_plugin is not None:
        raise ValueError("hydra-pytest-plugin is no longer required, please uninstall")


verify_hydra_pytest_plugin_not_installed()


def module_function(x: int) -> int:
    return x


@dataclass
class AClass:
    def __init__(self, a: Any, b: Any, c: Any, d: Any = "default_value") -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    @staticmethod
    def static_method(z: int) -> int:
        return z


@dataclass
class UntypedPassthroughConf:
    _target_: str = "tests.UntypedPassthroughClass"
    a: Any = MISSING


class UntypedPassthroughClass:
    def __init__(self, a: Any) -> None:
        self.a = a

    def __eq__(self, other: Any) -> Any:
        return self.a == other.a


# Type not legal in a config
class IllegalType:
    def __eq__(self, other: Any) -> Any:
        return isinstance(other, IllegalType)


@dataclass
class AnotherClass:
    x: int


class ASubclass(AnotherClass):
    @classmethod
    def class_method(cls, y: int) -> Any:
        return cls(y + 1)

    @staticmethod
    def static_method(z: int) -> int:
        return z


class Parameters:
    def __init__(self, params: List[float]):
        self.params = params


@dataclass
class Adam:
    params: Parameters
    lr: float = 0.001
    betas: Tuple[float, ...] = (0.9, 0.999)
    eps: float = 1e-08
    weight_decay: int = 0
    amsgrad: bool = False


@dataclass
class NestingClass:
    a: ASubclass = ASubclass(10)


nesting = NestingClass()


class ClassWithMissingModule:
    def __init__(self) -> None:
        import some_missing_module  # type: ignore # noqa: F401

        self.x = 1


@dataclass
class AdamConf(TargetConf):
    _target_: str = "tests.Adam"
    lr: float = 0.001
    betas: Tuple[float, ...] = (0.9, 0.999)
    eps: float = 1e-08
    weight_decay: int = 0
    amsgrad: bool = False


@dataclass
class BadAdamConf(TargetConf):
    # Missing str annotation
    _target_ = "tests.Adam"


@dataclass
class User:
    name: str = MISSING
    age: int = MISSING


@dataclass
class UserGroup:
    name: str = MISSING
    users: List[User] = MISSING


# RECURSIVE
# Classes
class Transform:
    ...


class CenterCrop(Transform):
    def __init__(self, size: int):
        self.size = size

    def __eq__(self, other) -> Any:
        if isinstance(other, type(self)):
            return self.size == other.size
        else:
            return False


class Rotation(Transform):
    def __init__(self, degrees: int):
        self.degrees = degrees

    def __eq__(self, other) -> Any:
        if isinstance(other, type(self)):
            return self.degrees == other.degrees
        else:
            return False


class Compose:
    transforms: List[Transform]

    def __init__(self, transforms: List[Transform]):
        self.transforms = transforms

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.transforms == other.transforms
        else:
            return False


class Tree:
    value: int
    left: Optional["Tree"] = None
    right: Optional["Tree"] = None

    def __init__(
        self, value: int, left: Optional["Tree"] = None, right: Optional["Tree"] = None
    ) -> None:
        self.value = value
        self.left = left
        self.right = right

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (
                self.value == other.value
                and self.left == other.left
                and self.right == other.right
            )

        else:
            return False


# Configs
@dataclass
class TransformConf:
    ...


@dataclass
class CenterCropConf(TransformConf):
    _target_: str = "tests.CenterCrop"
    size: int = MISSING


@dataclass
class RotationConf(TransformConf):
    _target_: str = "tests.Rotation"
    degrees: int = MISSING


@dataclass
class ComposeConf:
    _target_: str = "tests.Compose"
    transforms: List[TransformConf] = MISSING


@dataclass
class TreeConf:
    _target_: str = "tests.Tree"
    left: Optional["TreeConf"] = None
    right: Optional["TreeConf"] = None
    value: int = MISSING
