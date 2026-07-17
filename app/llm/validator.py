import json


class LLMValidator:

    @staticmethod
    def validate(response):

        try:

            data = json.loads(response)

            return data

        except Exception:

            return None