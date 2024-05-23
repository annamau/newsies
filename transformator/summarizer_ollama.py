import json, time, ollama
from tools import printProgressBar as printP


def summarize():
    with open("data/raw_data.json", "r") as f:
        conf = json.load(f)

    data = {}
    for key, items in conf.items():
        if items is not None:
            i = 0
            total_items = len(items) * len(conf)
            printP(0, total_items, prefix=f"  - Summarizing {key} ", suffix="Complete", length=50)
            for item in items:
                try:
                    data[key].append(
                        __create_structure(item)
                    )
                except KeyError:
                    data[key] = [
                        __create_structure(item)
                    ]
                printP(
                    i,
                    total_items,
                    prefix=f"  - Summarizing {key} ",
                    suffix="Complete",
                    length=50,
                )
                i += 1

    with open("data/summarized.json", "w") as f:
        json.dump(data, f)

def __create_structure(item):
    return {
        "title": item["title"],
        "text": ollama.chat(
            model="summarizer",
            messages=[
                {
                    "role": "user",
                    "content": item["text"],
                },
            ],
        )["message"]["content"],
        "link": item["link"],
    }

if __name__ == "__main__":
    start = time.time()
    summarize()
    end = time.time()
    print(f"  - Total time to summarize: {end - start}s \n")
