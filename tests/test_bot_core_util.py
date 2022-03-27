from typing import List
import pytest
from disnake import Embed
from bot.core.util import normalize_embed


@pytest.mark.parametrize(
    "embed, expected_embeds",
    [
        pytest.param(
            Embed(title="Test").add_field(
                name="Long single-line string", value=f"{'x' * 1050}"
            ),
            [
                Embed(title="Test")
                .add_field(name="Long single-line string", value=f"{'x' * 1021}...")
                .add_field(name="Long single-line string", value=f"...{'x' * 29}")
            ],
            id="Test embed field with a long single-line value",
        ),
        pytest.param(
            Embed(title="Test").add_field(
                name="Long multi-line string",
                value="\n".join(
                    [
                        "a" * 250,
                        "b" * 250,
                        "c" * 250,
                        "d" * 250,
                        "e" * 250,  # 1250-character embed
                    ]
                ),
                inline=False,
            ),
            [
                Embed(title="Test")
                .add_field(
                    name="Long multi-line string",
                    value="\n".join(
                        [
                            "a" * 250,
                            "b" * 250,
                            "c" * 250,
                            "d" * 250,
                        ]
                    ),
                    inline=False,
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join(["e" * 250]),
                    inline=False,
                )
            ],
            id="Test embed field with a long multi-line value",
        ),
        pytest.param(
            Embed(title="Test")
            .add_field(name="Long single-line string", value=f"{'x' * 1050}")
            .add_field(name="Short single-line string", value="This is short"),
            [
                Embed(title="Test")
                .add_field(name="Long single-line string", value=f"{'x' * 1021}...")
                .add_field(name="Long single-line string", value=f"...{'x' * 29}")
                .add_field(name="Short single-line string", value="This is short"),
            ],
            id="Test embed with two fields, the first of which is a long single-line value",
        ),
        pytest.param(
            Embed(title="Test")
            .add_field(name="Short single-line string", value="This is short")
            .add_field(name="Long single-line string", value=f"{'x' * 1050}"),
            [
                Embed(title="Test")
                .add_field(name="Short single-line string", value="This is short")
                .add_field(name="Long single-line string", value=f"{'x' * 1021}...")
                .add_field(name="Long single-line string", value=f"...{'x' * 29}"),
            ],
            id="Test embed with two fields, the second of which is a long single-line value",
        ),
        pytest.param(
            Embed(title="Test")
            .add_field(name="Short single-line string", value="This is short")
            .add_field(name="Long single-line string", value=f"{'x' * 1050}")
            .add_field(
                name="Another short single-line string", value="This is also short"
            ),
            [
                Embed(title="Test")
                .add_field(name="Short single-line string", value="This is short")
                .add_field(name="Long single-line string", value=f"{'x' * 1021}...")
                .add_field(name="Long single-line string", value=f"...{'x' * 29}")
                .add_field(
                    name="Another short single-line string", value="This is also short"
                ),
            ],
            id="Test embed with three fields, the second of which is a long single-line value",
        ),
        pytest.param(
            Embed(title="Test")
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'a' * 500}", f"{'a' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'b' * 500}", f"{'b' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'c' * 500}", f"{'c' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'d' * 500}", f"{'d' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'e' * 500}", f"{'e' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'f' * 500}", f"{'f' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'g' * 500}", f"{'g' * 500}"]),
            ),
            [
                Embed(title="Test")
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'a' * 500}", f"{'a' * 500}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'b' * 500}", f"{'b' * 500}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'c' * 500}", f"{'c' * 500}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'d' * 500}", f"{'d' * 500}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'e' * 500}", f"{'e' * 500}"]),
                ),
                Embed(title="Test")
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'f' * 500}", f"{'f' * 500}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'g' * 500}", f"{'g' * 500}"]),
                ),
            ],
            id="Test embed with seven fields, each of which is 1000 characters in length",
        ),
        pytest.param(
            Embed(title="Test")
            .add_field(name="Long single-line string", value=f"{'a' * 1500}")
            .add_field(name="Long single-line string", value=f"{'b' * 1000}")
            .add_field(name="Long single-line string", value=f"{'c' * 1000}")
            .add_field(name="Long single-line string", value=f"{'d' * 1000}")
            .add_field(name="Long single-line string", value=f"{'e' * 1000}")
            .add_field(name="Long single-line string", value=f"{'f' * 1000}")
            .add_field(name="Long single-line string", value=f"{'g' * 1000}"),
            [
                Embed(title="Test")
                .add_field(name="Long single-line string", value=f"{'a' * 1021}...")
                .add_field(name="Long single-line string", value=f"...{'a' * 479}")
                .add_field(name="Long single-line string", value=f"{'b' * 1000}")
                .add_field(name="Long single-line string", value=f"{'c' * 1000}")
                .add_field(name="Long single-line string", value=f"{'d' * 1000}")
                .add_field(name="Long single-line string", value=f"{'e' * 1000}"),
                Embed(title="Test")
                .add_field(name="Long single-line string", value=f"{'f' * 1000}")
                .add_field(name="Long single-line string", value=f"{'g' * 1000}"),
            ],
            id="Test embed with seven fields, single-line, each is 1000 characters in length",
        ),
        pytest.param(
            Embed(title="Test")
            .add_field(name="Long single-line string", value=f"{'a' * 1500}")
            .add_field(name="Long single-line string", value=f"{'b' * 1000}")
            .add_field(name="Long single-line string", value=f"{'c' * 1000}")
            .add_field(name="Long single-line string", value=f"{'d' * 1000}")
            .add_field(name="Long single-line string", value=f"{'e' * 1000}")
            .add_field(name="Long single-line string", value=f"{'f' * 1000}")
            .add_field(name="Long single-line string", value=f"{'g' * 1000}"),
            [
                Embed(title="Test")
                .add_field(name="Long single-line string", value=f"{'a' * 1021}...")
                .add_field(name="Long single-line string", value=f"...{'a' * 479}")
                .add_field(name="Long single-line string", value=f"{'b' * 1000}")
                .add_field(name="Long single-line string", value=f"{'c' * 1000}")
                .add_field(name="Long single-line string", value=f"{'d' * 1000}")
                .add_field(name="Long single-line string", value=f"{'e' * 1000}"),
                Embed(title="Test")
                .add_field(name="Long single-line string", value=f"{'f' * 1000}")
                .add_field(name="Long single-line string", value=f"{'g' * 1000}"),
            ],
            id="Test embed with seven fields, most are 1000 characters in length, first is 1500",
        ),
        pytest.param(
            Embed(title="Test")
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'a' * 750}", f"{'a' * 750}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'b' * 500}", f"{'b' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'c' * 500}", f"{'c' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'d' * 500}", f"{'d' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'e' * 500}", f"{'e' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'f' * 500}", f"{'f' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'g' * 500}", f"{'g' * 500}"]),
            ),
            [
                Embed(title="Test")
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'a' * 750}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'a' * 750}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'b' * 500}", f"{'b' * 500}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'c' * 500}", f"{'c' * 500}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'d' * 500}", f"{'d' * 500}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'e' * 500}", f"{'e' * 500}"]),
                ),
                Embed(title="Test")
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'f' * 500}", f"{'f' * 500}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'g' * 500}", f"{'g' * 500}"]),
                ),
            ],
            id=(
                "Test embed with seven fields, most of which are 1000 characters in length, first "
                "is 1500"
            ),
        ),
        pytest.param(
            Embed(title="Test")
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'a' * 500}", f"{'a' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'b' * 500}", f"{'b' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'c' * 500}", f"{'c' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'d' * 500}", f"{'d' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'e' * 500}", f"{'e' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'f' * 500}", f"{'f' * 500}"]),
            )
            .add_field(
                name="Long multi-line string",
                value="\n".join([f"{'g' * 750}", f"{'g' * 750}"]),
            ),
            [
                Embed(title="Test")
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'a' * 500}", f"{'a' * 500}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'b' * 500}", f"{'b' * 500}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'c' * 500}", f"{'c' * 500}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'d' * 500}", f"{'d' * 500}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'e' * 500}", f"{'e' * 500}"]),
                ),
                Embed(title="Test")
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'f' * 500}", f"{'f' * 500}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'g' * 750}"]),
                )
                .add_field(
                    name="Long multi-line string",
                    value="\n".join([f"{'g' * 750}"]),
                ),
            ],
            id=(
                "Test embed with seven fields, most of which are 1000 characters in length, last "
                "is 1500"
            ),
        ),
    ],
)
def test_normalize_embed(embed: Embed, expected_embeds: List[Embed]) -> None:
    assert [e.to_dict() for e in normalize_embed(embed)] == [
        e.to_dict() for e in expected_embeds
    ]
