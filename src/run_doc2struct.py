# SPDX-License-Identifier: MIT

from html import escape
import json
from pathlib import Path
import re

import doc2struct
from parse_bench.evaluation.metrics.parse.formatting_v2 import FULL, formatting_v2_metrics, rules_reference
from parse_bench.evaluation.metrics.parse.table_next import table_next_metrics
from parse_bench.evaluation.metrics.parse.text_next import reference_markdown, text_next_metrics
from parse_bench.schemas.parse_output import ParseOutput
from parse_bench.test_cases.parse_rule_schemas import coerce_parse_rule_list


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RUN_DIR = ROOT / "runs" / "doc2struct"
DEFAULT_RULES = ROOT / "rules" / "doc2struct.json"

def _paragraph(value):
    if not value:
        return ""
    return "<p>" + escape(value).replace("\n", "<br>\n") + "</p>"


def _table_html(row, current_title):
    blocks = []
    title = row.get("text")
    if title and title != current_title:
        blocks.append(_paragraph(title))
    blocks.append(_paragraph(row.get("preamble")))
    table = ["<table>", "<tbody>"]
    for cells in row.get("matrix") or []:
        rendered = [f"<td>{escape(cell or '')}</td>" for cell in cells]
        table.append("<tr>" + "".join(rendered) + "</tr>")
    table.extend(["</tbody>", "</table>"])
    blocks.append("\n".join(table))
    for marker, text in row.get("footnotes") or []:
        blocks.append(_paragraph(" ".join(part for part in (marker, text) if part)))
    blocks.append(_paragraph(row.get("postamble")))
    return "\n\n".join(block for block in blocks if block)


def convert_to_eval(standardized_rows, example_id):
    # doc2struct -> ParseBench: render blocks as Markdown and matrix cells as HTML.
    chunks = []
    pending = []
    current_title = None

    def flush() -> None:
        if pending:
            rendered = doc2struct.convert_standardized_text_to_markdown(
                pending, redundant="plain"
            )
            if rendered.strip():
                chunks.append(rendered.strip())
            pending.clear()

    for row in standardized_rows:
        if row.get("type") == "title":
            current_title = row.get("text")
        if row.get("type") == "table":
            flush()
            chunks.append(_table_html(row, current_title))
        else:
            pending.append(row)
    flush()
    markdown = "\n\n".join(chunks)
    return {
        "task_type": "parse",
        "example_id": example_id,
        "pipeline_name": "doc2struct",
        "pages": [{"page_index": 0, "markdown": markdown}],
        "markdown": markdown,
    }


def evaluate(converted, descriptor, metric_name):
    metadata = descriptor.get("metadata", {})
    rules = coerce_parse_rule_list(descriptor.get("test_rules") or [])
    reference = reference_markdown(descriptor.get("expected_markdown"), rules)
    markdown = converted["markdown"]

    if metric_name == "table_next":
        reference = descriptor.get("expected_markdown")
        flags = {
            name: descriptor.get(name, metadata.get(name, default))
            for name, default in (
                ("max_top_title_rows", 1),
                ("allow_splitting_ambiguous_merged_tables", False),
                ("trm_unsupported", False),
                ("allow_merged_sub_rows", False),
            )
        }
        metrics = table_next_metrics(reference, markdown, **flags)
    elif metric_name == "text_next":
        metrics = text_next_metrics(reference, ParseOutput.model_validate(converted))
    elif metric_name == "formatting_v2":
        reference, scope = (reference, FULL) if reference else rules_reference(rules)
        metrics = formatting_v2_metrics(reference, markdown, scope)
    else:
        raise ValueError(f"Unknown metric: {metric_name}")
    score = next(metric.value for metric in metrics if metric.metric_name == metric_name)
    return score, reference or ""


def main():
    rules = doc2struct.load_rules(DEFAULT_RULES)
    parsers = {".html": doc2struct.parse_html, ".htm": doc2struct.parse_html, ".pdf": doc2struct.parse_pdf}
    for path in sorted(DATA_DIR.glob("*/*/expected.json")):
        descriptor = json.loads(path.read_text(encoding="utf-8"))
        case = path.parent.relative_to(DATA_DIR)
        metric = descriptor.get("metadata", {}).get("primary_metric") or {
            "headings": "formatting_v2", "text": "text_next"
        }.get(case.parts[0], "table_next")
        source = path.parent / descriptor["document"]
        suffix = source.suffix.lower()
        if suffix == ".pdf" and metric == "table_next":
            continue
        data = source.read_bytes()
        if suffix == ".txt":
            partial_sgml = re.search(rb"<(?:TABLE|PAGE|CAPTION|S|C)(?:\s|>)", data, re.I)
            parser = doc2struct.parse_partialsgml if partial_sgml else doc2struct.parse_text
        else:
            parser = parsers[suffix]
        converted = convert_to_eval(parser(data, rules=rules), descriptor["id"])
        score, reference = evaluate(converted, descriptor, metric)
        destination = RUN_DIR / case / "result.md"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            f"## Parser Markdown\n\n{converted['markdown']}\n\n"
            f"## Eval Markdown\n\n{reference}\n\n"
            f"## Eval Score\n\n{metric}: {score:.6f} ({score:.2%})\n",
            encoding="utf-8",
        )
        print(f"{case.as_posix()}: {score:.2%}", flush=True)


if __name__ == "__main__":
    main()
