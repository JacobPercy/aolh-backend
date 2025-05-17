import os
import json
from difflib import SequenceMatcher
from datetime import datetime
from typing import List

MEMORY_DIR = "/Users/jacobpercy/Desktop/github/aolh-backend/memories"

def load_all_memories():
    memories = []
    for folder in os.listdir(MEMORY_DIR):
        folder_path = os.path.join(MEMORY_DIR, folder)
        json_path = os.path.join(folder_path, "data.json")
        if os.path.isfile(json_path):
            with open(json_path, "r") as f:
                data = json.load(f)
                memories.append(data)
    return memories

def simple_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def score_memory(memory, query, query_time=None, user_relations=None):
    score = 0
    q = query.lower()

    score += 3 * simple_similarity(memory.get("title", ""), q)
    score += 2 * simple_similarity(memory.get("description", ""), q)

    for tag in memory.get("tags", []):
        score += 1.5 * simple_similarity(tag, q)
    
    for kw in memory.get("keywords", []):
        score += 1.5 * simple_similarity(kw, q)

    for person in memory.get("people", []):
        person_name = person.get("name", "")
        relation = person.get("relation", "")
        score += 2 * simple_similarity(person_name, q)
        score += 2 * simple_similarity(relation, q)
        if user_relations:
            if relation.lower() in [r.lower() for r in user_relations]:
                score += 1.5  # user-related person

    location = memory.get("location", {}).get("name", "")
    score += 1.5 * simple_similarity(location, q)

    if query_time:
        try:
            mem_time = datetime.fromisoformat(memory.get("timestamp", ""))
            delta_days = abs((mem_time - query_time).days)
            time_score = max(0, 1 - (delta_days / 3650))  # within ~10 years
            score += time_score
        except:
            pass

    return score

def sm(query: str, n: int = 5, query_time=None, user_relations: List[str] = None):
    all_memories = load_all_memories()
    scored = []

    for mem in all_memories:
        s = score_memory(mem, query, query_time, user_relations)
        scored.append((s, mem))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [mem for _, mem in scored[:n]]
