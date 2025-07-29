from typing import List

import flyte

env = flyte.TaskEnvironment(name="hello_world")


@env.task
def say_hello(data: str, lt: List[int]) -> str:
    return f"Hello {data} {lt}"


@env.task
def square(i: int = 3) -> int:
    return i * i


@env.task
def say_hello_nested(data: str = "default string") -> str:
    squared = []
    for i in range(3):
        squared.append(square(i=i))

    return say_hello(data=data, lt=squared)


def test_run_local_controller():
    flyte.init_from_config(None)

    result = flyte.with_runcontext(mode="local").run(say_hello_nested, data="hello world")
    assert result.outputs() == "Hello hello world [0, 1, 4]"


def test_run_pure_function():
    result = say_hello_nested(data="hello world")
    assert result == "Hello hello world [0, 1, 4]"
