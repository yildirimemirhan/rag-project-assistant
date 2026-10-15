"""Periodic eval (paid: calls Groq). Run before shipping a knowledge change.

Usage: python evals/run_eval.py [--threshold 0.85]
Needs GROQ_API_KEY and a built index (python build_index.py).
Each case checks: retrieved sources contain an expected doc, the answer contains
one of `any`, and contains none of `none`. Exit 1 if pass rate < threshold.
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from rag_chatbot import init_rag, answer_query  # noqa: E402


def check(case, result):
    answer = result["answer"].lower()
    problems = []
    if case["sources"] and not any(s in result["sources"] for s in case["sources"]):
        problems.append(f"sources {result['sources']} missing any of {case['sources']}")
    if case["any"] and not any(k.lower() in answer for k in case["any"]):
        problems.append(f"answer lacks any of {case['any']}")
    for bad in case["none"]:
        if bad.lower() in answer:
            problems.append(f"answer contains forbidden '{bad}'")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=0.85)
    args = ap.parse_args()

    with open(os.path.join(ROOT, "evals", "cases.json"), encoding="utf-8") as f:
        cases = json.load(f)

    state = init_rag(verbose=True)
    passed = 0
    for case in cases:
        result = answer_query(case["q"], state)
        problems = check(case, result)
        passed += not problems
        print(("PASS " if not problems else "FAIL ") + case["q"])
        for p in problems:
            print("   -", p)
        if problems:
            print("   answer:", result["answer"][:300].replace("\n", " "))

    rate = passed / len(cases)
    print(f"\n{passed}/{len(cases)} passed ({rate:.0%}), threshold {args.threshold:.0%}")
    sys.exit(0 if rate >= args.threshold else 1)


if __name__ == "__main__":
    main()
