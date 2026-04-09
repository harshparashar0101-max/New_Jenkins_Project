import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

JUNIT_FILE = "reports/results.xml"
MAPPING_FILE = "xray_mapping.json"
OUTPUT_FILE = "reports/xray_results.json"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def load_mapping():
    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_junit():
    tree = ET.parse(JUNIT_FILE)
    root = tree.getroot()

    testcases = []

    # pytest junit xml may have root = testsuite or testsuites
    suites = []
    if root.tag == "testsuite":
        suites = [root]
    elif root.tag == "testsuites":
        suites = root.findall("testsuite")

    for suite in suites:
        for case in suite.findall("testcase"):
            name = case.attrib.get("name", "").strip()
            classname = case.attrib.get("classname", "").strip()
            time_taken = case.attrib.get("time", "0")

            if case.find("failure") is not None:
                status = "FAIL"
                comment = case.find("failure").attrib.get("message", "Test failed")
            elif case.find("error") is not None:
                status = "FAIL"
                comment = case.find("error").attrib.get("message", "Test errored")
            elif case.find("skipped") is not None:
                status = "TODO"
                comment = "Test skipped"
            else:
                status = "PASS"
                comment = "Automated execution from Jenkins"

            testcases.append(
                {
                    "name": name,
                    "classname": classname,
                    "status": status,
                    "comment": comment,
                    "time": time_taken,
                }
            )

    return testcases


def build_xray_json(testcases, mapping):
    now = utc_now()

    tests = []
    for tc in testcases:
        test_name = tc["name"]
        test_key = mapping.get(test_name)

        if not test_key:
            print(f"Skipping unmapped test: {test_name}")
            continue

        tests.append(
            {
                "testKey": test_key,
                "start": now,
                "finish": now,
                "comment": tc["comment"],
                "status": tc["status"],
            }
        )

    result = {
        "info": {
            "summary": "Jenkins automated execution",
            "description": "Execution imported from Jenkins using Xray JSON",
            "startDate": now,
            "finishDate": now,
        },
        "tests": tests,
    }

    return result


def main():
    os.makedirs("reports", exist_ok=True)

    mapping = load_mapping()
    testcases = parse_junit()
    xray_json = build_xray_json(testcases, mapping)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(xray_json, f, indent=2)

    print(f"Created {OUTPUT_FILE}")


if __name__ == "__main__":
    main()