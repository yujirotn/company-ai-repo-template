"""Build CATALOG.md from harness component metadata without running any component."""

import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
FIELD = re.compile(r"^(name|description):[ \t]*(.*)$")
MARKDOWN_ESCAPES = str.maketrans({character: "\\" + character for character in "\\|*_~`[]"})
COLLECTIONS = {"members": "_ひな形", "plugins": "_部署のひな形"}
PLUGIN_MANIFESTS = ("plugin.json", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json")
SECTIONS = {
    "スキル": {"members": ("skills/*/SKILL.md",), "plugins": ("skills/*/SKILL.md",)},
    "フック": {"members": ("hooks/*/README.md",), "plugins": ("hooks/*/README.md",)},
    "決まり": {"members": ("rules/*/README.md",), "plugins": ("rules/*/README.md",)},
    "エージェント": {
        "members": ("agents/*/README.md",),
        "plugins": ("agents/*.md", "agents/*/README.md"),
    },
    "設定": {"members": ("settings/*/README.md",), "plugins": ("settings/*/README.md",)},
    "プラグイン": {},
}


def read_fields(path):
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("先頭に --- で囲った name と description が必要です")
    end = next((index for index, line in enumerate(lines[1:], 1) if line.rstrip() == "---"), None)
    if end is None:
        raise ValueError("先頭の項目を --- で閉じてください")

    fields = {}
    for index, line in enumerate(lines[1:end], 1):
        match = FIELD.fullmatch(line)
        if not match:
            continue
        key, first = match.groups()
        if key in fields:
            raise ValueError(f"{key} が重複しています")
        continuation = []
        for following in lines[index + 1 : end]:
            if following and not following[0].isspace():
                break
            continuation.append(following.strip())
        fields[key] = read_scalar(first, continuation)

    if not fields.get("name") or not fields.get("description"):
        raise ValueError("name と description に値を入れてください")
    return fields["name"], fields["description"]


def read_scalar(first, continuation):
    if re.fullmatch(r"[>|](?:[1-9][+-]?|[+-][1-9]?)?(?:[ \t]+#.*)?", first.strip()):
        value = " ".join(continuation)
    else:
        value = " ".join([first, *continuation]).strip()
        if value.startswith('"'):
            decoded, end = json.JSONDecoder().raw_decode(value)
            if not re.fullmatch(r"\s*(?:#.*)?", value[end:]):
                raise ValueError("二重引用符の後はコメントだけを書けます")
            value = decoded
        elif value.startswith("'"):
            match = re.fullmatch(r"'((?:[^']|'')*)'\s*(?:#.*)?", value)
            if not match:
                raise ValueError("一重引用符を閉じてください。文中の一重引用符は2つ重ねます")
            value = match.group(1).replace("''", "'")
        else:
            value = re.split(r"(?:^|\s)#", value, maxsplit=1)[0]
    return " ".join(value.split())


def table_text(value):
    # Keep descriptions and member names as literal text inside Markdown cells.
    return html.escape(value, quote=False).replace("\n", " ").translate(MARKDOWN_ESCAPES)


def check_path(path):
    relative = path.relative_to(ROOT)
    for part in (relative, *relative.parents):
        if (ROOT / part).is_symlink():
            raise ValueError(f"{part.as_posix()}: シンボリックリンクは使えません")


def read_component(path):
    name, description = read_fields(path)
    if path.name == "SKILL.md" and (
        name != path.parent.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
    ):
        raise ValueError("name とフォルダ名を同じ半角英小文字・数字・ハイフンにしてください")
    return name, description


def read_plugin(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("プラグインの定義は JSON オブジェクトで書いてください")
    name = data.get("name")
    description = data.get("description", "")
    if not isinstance(name, str) or not name.strip() or not isinstance(description, str):
        raise ValueError("name と description は文字列で書いてください（description は省略可）")
    return name.strip(), " ".join(description.split()) or "プラグインの定義を参照"


def owners(collection):
    directory = ROOT / collection
    check_path(directory)
    for path in sorted(directory.glob("*")):
        if path.name == COLLECTIONS[collection] or path.name.startswith("."):
            continue
        check_path(path)
        if path.is_dir():
            yield path


def component_paths(kind, collection, owner):
    if kind == "プラグイン":
        bundles = [owner] if collection == "plugins" else sorted((owner / "plugins").glob("*/"))
        for bundle in bundles:
            check_path(bundle)
            for filename in PLUGIN_MANIFESTS:
                manifest = bundle / filename
                check_path(manifest)
                if manifest.is_file():
                    yield manifest
                    break
        return

    for pattern in SECTIONS[kind][collection]:
        for path in sorted(owner.glob(pattern)):
            if pattern == "agents/*.md" and path.name == "README.md":
                continue
            yield path


def render_row(kind, collection, owner, path):
    relative = path.relative_to(ROOT)
    try:
        check_path(path)
        reader = read_plugin if kind == "プラグイン" else read_component
        name, description = reader(path)
    except (OSError, ValueError) as error:
        sys.exit(f"{relative.as_posix()}: {error}")

    if collection == "plugins":
        owner = "会社" if kind == "プラグイン" else f"会社（{owner}）"
    location = f"[{table_text(path.name)}]({quote(relative.as_posix())})"
    cells = [table_text(value) for value in (kind, name, owner, description)]
    return "| " + " | ".join([*cells, location]) + " |"


def main():
    rows = [
        "# ハーネス部品一覧",
        "",
        "メンバーのおすすめと会社のプラグインを種類別に探せます。更新するには `python3 scripts/catalog.py` を実行します。",
        "フック・設定は、台本や設定の全文を確認してから使う人が自分で設定に足します。",
    ]
    collections = {collection: list(owners(collection)) for collection in COLLECTIONS}
    for kind in SECTIONS:
        rows.extend([
            "",
            f"## {kind}",
            "",
            "| 種類 | 名前 | 持ち主 | 一言 | 場所 |",
            "| --- | --- | --- | --- | --- |",
        ])
        entries = [
            render_row(kind, collection, owner.name, path)
            for collection, paths in collections.items()
            for owner in paths
            for path in component_paths(kind, collection, owner)
        ]
        rows.extend(entries or [f"| {kind} | — | — | 掲載された部品はありません | — |"])

    output = ROOT / "CATALOG.md"
    check_path(output)
    output.write_text("\n".join(rows) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        sys.exit(str(error))
