import json
from typing import Dict

def load_faq() -> Dict[str, str]:
    try:
        with open("data/faq.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Ошибка загрузки FAQ: {e}")
        return {}