PROMPT_TEMPLATE = """
You are a Software QA Engineer.

Generate 3 to 5 test cases.

Return ONLY valid JSON.

Do not use markdown.
Do not use ```json.
Do not write explanations.

Return exactly this format:

{{
  "test_cases": [
    {{
      "id": 1,
      "title": "",
      "preconditions": "",
      "steps": [
        "Step 1",
        "Step 2"
      ],
      "expected_result": ""
    }}
  ]
}}

Document:

{document}
"""