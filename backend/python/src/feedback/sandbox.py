# ruff: noqa: E501

from collections import Counter

from feedback.config import DATA_DIR
from feedback.core.ml.index import (
    build_index_from_json,
    load_tags,
    save_tags,
    unpack_tag_id,
)
from feedback.core.ml.llm import embed
from feedback.core.tag.tag import extract_quality_tags
from feedback.rounters.injest import (
    tag_good,
    tag_marked,
)

GOOD_EXAMPLE = (
    "Shakespeare constructs Prospero as a figure whose authority is fundamentally inseparable from his capacity for violence. "
    "Through the opening tempest, the playwright frames power not as benevolent governance but as an act of deliberate destabilisation. "
    "The storm is not merely atmospheric but structural — it unsettles the audience's assumptions about who holds legitimate control over the island. "
    "By positioning Prospero as the architect of this chaos, Shakespeare implicates him in the very disorder he claims to resolve."
)
MARKED_EXAMPLE = "Shakespeare employs the metaphor of the tempest to interrogate the moral legitimacy of Prospero's authority."
MARKED_COMMENT = "You've identified the metaphor but not explained what it constructs — why does Shakespeare use the tempest specifically to frame questions of authority?"

MODULE_CONTEXT = "HSC English Advanced. Prescribed text: The Tempest. Rubric criteria: thesis, evidence, analysis, conceptual depth, contextual knowledge"

WEAK_EXAMPLE = "Prospero uses magic to control the island and its inhabitants."
QUAITY_THRESHOLD = 0.7

GOOD_PATH = DATA_DIR / "good.json"
MASKED_PATH = DATA_DIR / "marked.json"


if __name__ == "__main__":
    good_record = tag_good("good.docx", GOOD_EXAMPLE, MODULE_CONTEXT)
    marked_record = tag_marked(
        "marked1.docx", [(MARKED_EXAMPLE, MARKED_COMMENT)], MODULE_CONTEXT
    )

    # Will be linked to the final save after route call
    save_tags(GOOD_PATH, [good_record])
    save_tags(MASKED_PATH, [marked_record])

    # Add a way to append if memory index is active

    good_index = build_index_from_json(GOOD_PATH)
    mark_index = build_index_from_json(MASKED_PATH)

    print(f"Good index: {good_index.ntotal} tags")
    print(f"Marked index: {mark_index.ntotal} tags")

    weak_tags = extract_quality_tags(WEAK_EXAMPLE, MODULE_CONTEXT)
    weak_embs = embed(weak_tags)

    scores, ids = good_index.search(weak_embs, k=5)  # type: ignore
    good_records = load_tags(GOOD_PATH)

    matched = {unpack_tag_id(int(tid)) for row in ids for tid in row}
    matched_doc_id = Counter(doc_id for doc_id, _ in matched).most_common(1)[0][0]
    dominant = good_records[matched_doc_id]

    matched_idxs = {tag_idx for doc_id, tag_idx in matched if doc_id == matched_doc_id}
    gap_idxs = set(range(len(dominant.tags))) - matched_idxs

    print("Matched:")
    for idx in sorted(matched_idxs):
        print(f"  {dominant.tags[idx].tag}")

    print("\nGaps:")
    for idx in sorted(gap_idxs):
        print(f"  {dominant.tags[idx].tag}")

    
    scores, ids = mark_index.search(weak_embs, k=5)  # type: ignore
    matched = {unpack_tag_id(int(tid)) for row in ids for tid in row}
    matched_doc_id = Counter(doc_id for doc_id, _ in matched).most_common(1)[0][0]
    dominant = load_tags(MASKED_PATH)[matched_doc_id]

    matched_idxs = {tag_idx for doc_id, tag_idx in matched if doc_id == matched_doc_id}

    print("Feedback:")
    for idx in sorted(matched_idxs):
        print(f"  {dominant.tags[idx].tag}")

    # query = "technique identified but significance not explained"
    # query_emb = embed([query])
    # scores, ids = good_index.search(query_emb, k=3)  # type: ignore

    # good_records = load_tags(GOOD_PATH)
    # for tag_id in ids[0]:
    #     doc_id, tag_idx = unpack_tag_id(int(tag_id))
    #     record = good_records[doc_id]
    #     tag = record.tags[tag_idx]
    #     print(f"[{tag_idx}] {tag.tag}")

    # good_records = load_tags("good_records")
    # record_keys = list(good_records.keys())

    # doc_id_map: dict[int, str] = {}
    # for key, record in good_records.items():
    #     for t in record["tags"]:
    #         if t["tag_id"] is not None:
    #             doc_id_map[unpack_tag_id(t["tag_id"])[0]] = key

    # print(f"\nQuery: '{query}'")
    # for score, packed_id in zip(scores[0], ids[0]):
    #     if packed_id == -1:
    #         continue
    #     record_doc_id, tag_idx = unpack_tag_id(int(packed_id))
    #     doc_id_str = doc_id_map[record_doc_id]
    #     tag = good_records[doc_id_str]["tags"][tag_idx]["tag"]
    #     print(f"  {score:.3f}  [{doc_id_str}]  {tag}")

# if __name__ == "__main__":
#     # SIMULATING GOOD EXAMPLE INJESTION

#     good_documents = [GOOD_EXAMPLE]
#     records: dict[int, dict] = {}

#     for doc in good_documents:
#         sentences = to_sentences(doc)
#         doc_id = gen_doc_id()
#         num_tags = 0

#         all_tags: list[str] = []
#         all_ids: list[int] = []
#         tag_records: list[dict] = []

#         for sentence in sentences:
#             tags = extract_technique_tags(sentence, MODULE_CONTEXT)
#             tag_ids = [
#                 gen_tag_id(doc_id, num_tags + idx + 1) for idx in range(len(tags))
#             ]
#             num_tags += len(tags)

#             for tag, tag_id in zip(tags, tag_ids, strict=True):
#                 all_tags.append(tag)
#                 all_ids.append(tag_id)
#                 tag_records.append({"tag_id": tag_id, "tag": tag})

#         embs = embed(all_tags)
#         good_index = build_id_index(embs, all_ids)

#         records[doc_id] = {
#             "filename": "good_example",
#             "uploaded_at": datetime.now().isoformat(),
#             "tags": tag_records,
#         }

#         print(f"Indexed {good_index.ntotal} tags from {len(sentences)} sentences")
#         print(f"Document ID: {doc_id}")

#     with open(DATA_DIR / "good_records.json", "w") as f:
#         json.dump({str(k): v for k, v in records.items()}, f, indent=2)

#     print(f"Saved records to {DATA_DIR}/good_records.json")

# SIMULATING STUDENT CHECK

# weak = WEAK_EXAMPLE
# weak_tags = extract_technique_tags(WEAK_EXAMPLE, MODULE_CONTEXT)
# weak_embs = embed(weak_tags)

# results = search_index(weak_embs[0], index, k=10)
# best_doc_id = top_doc_id(results)
# doc_tags = [tag for _, tag_id in results if unpack_tag_id(tag_id)[0] == best_doc_id]

# mark_tags = extract_markback_tags(TRAIN_EXAMPLE, TRAIN_COMMENT, MODULE_CONTEXT)
# print("\nmarkback Tags on past examples:")
# print_tags(mark_tags)

# mark_index, stored_mark_tags = build_index(mark_tags)
# print(f"markback Index: {mark_index.ntotal} tags")

# quality_tags = extract_quality_tags(WEAK_EXAMPLE, MODULE_CONTEXT)
# print("\nQuality Tags on student example:")
# print_tags(quality_tags)

# missing = []
# if quality_tags:
#     q_embs = embed(quality_tags)
#     g_embs = embed(stored_good_tags)
#     sim_matrix = g_embs @ q_embs.T
#     for i, good_tag in enumerate(stored_good_tags):
#         if float(sim_matrix[i].max()) < QUALITY_THRESHOLD:
#             missing.append(good_tag)

# print("\nMissing (not in student):")
# print_tags(missing)

# if missing:
#     record_hits: dict[int, float] = {}
#     for tag in missing:
#         for score, matched_tag in search_index(
#             tag, mark_index, stored_mark_tags, k=3
#         ):
#             idx = stored_mark_tags.index(matched_tag)
#             record_hits[idx] = record_hits.get(idx, 0) + score

#     ranked = sorted(record_hits.items(), key=lambda x: x[1], reverse=True)
#     top_markback = [stored_mark_tags[i] for i, _ in ranked[:3]]

#     print("\nRetrieved markback tags:")
#     print_tags(top_markback)


# # ruff: noqa: E501


# from feedback.config import DATA_DIR
# from feedback.core.ml.index import (
#     unpack_tag_id,
# )
# from feedback.core.ml.llm import embed
# from feedback.rounters.injest import (
#     build_index_from_json,
#     load_tags,
#     process_good,
#     process_marked,
#     save_tags,
# )

# GOOD_EXAMPLE = (
#     "Shakespeare constructs Prospero as a figure whose authority is fundamentally inseparable from his capacity for violence. "
#     "Through the opening tempest, the playwright frames power not as benevolent governance but as an act of deliberate destabilisation. "
#     "The storm is not merely atmospheric but structural — it unsettles the audience's assumptions about who holds legitimate control over the island. "
#     "By positioning Prospero as the architect of this chaos, Shakespeare implicates him in the very disorder he claims to resolve."
# )
# MARKED_EXAMPLE = "Shakespeare employs the metaphor of the tempest to interrogate the moral legitimacy of Prospero's authority."
# MARKED_COMMENT = "You've identified the metaphor but not explained what it constructs — why does Shakespeare use the tempest specifically to frame questions of authority?"

# MODULE_CONTEXT = "HSC English Advanced. Prescribed text: The Tempest. Rubric criteria: thesis, evidence, analysis, conceptual depth, contextual knowledge"

# WEAK_EXAMPLE = "Prospero uses magic to control the island and its inhabitants."
# QUAITY_THRESHOLD = 0.7


# if __name__ == "__main__":
#     good_id, good_record = process_good(
#         "good_example.docx", GOOD_EXAMPLE, MODULE_CONTEXT
#     )
#     marked_id, marked_record = process_marked(
#         "marked_example.docx", (MARKED_EXAMPLE, MARKED_COMMENT), MODULE_CONTEXT
#     )

#     save_tags("good_records", {str(good_id): good_record})
#     save_tags("marked_records", {str(marked_id): marked_record})

#     print("Saved good and marked records")

#     good_index = build_index_from_json(DATA_DIR / "good_records.json")
#     mark_index = build_index_from_json(DATA_DIR / "marked_records.json")

#     print(f"Good index: {good_index.ntotal} tags")
#     print(f"Marked index: {mark_index.ntotal} tags")

#     query = "technique identified but significance not explained"
#     q_vec = embed([query])
#     scores, ids = good_index.search(q_vec, k=3)  # type: ignore

#     good_records = load_tags("good_records")
#     record_keys = list(good_records.keys())
