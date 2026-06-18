# Edge — Decentralized Content Governance & Sustainability (Issue 10)

Edge's hardware and power story is strong; the long-term risk is **content**:
keeping curriculum, language resources, and software current across many schools
and countries without a central team. This document defines a decentralized model
where ministries, schools, NGOs, and local teachers each publish updates
independently, and hubs adopt them safely.

## The problem

A single central maintainer doesn't scale to multi-country deployment and breaks
the moment connectivity or funding lapses. We need updates to flow from many
publishers, over sneakernet, **without** a hub blindly trusting whatever arrives.

## The model: signed, versioned content manifests

Every content folder carries a `manifest.json` describing each file's **checksum,
version, publisher, and timestamp** (see
[tools/content_manifest.py](../tools/content_manifest.py)). This adds the trust
layer on top of the existing USB sync.

Publishers and their scope:

| Publisher | Scope | Example |
|---|---|---|
| Ministry of Education | National curriculum, authoritative | `MoE-MY`, `DepEd-PH` |
| NGO / partner | Supplementary material, languages | `UNICEF`, local NGO |
| School | Local lessons, context | `SK-Long-Lamai` |
| Teacher | Glossary terms, translation corrections | per-teacher token |

## Update flow

```
Publisher                         USB                          Hub
  build manifest  ──►  new_curriculum/ + manifest.json  ──►  sneakernet sync
  (version, sig)                                              merge manifests
                                                              verify checksums
                                                              re-index RAG
```

1. **Publish.** A publisher runs `content_manifest build --publisher <id> --version <n>`
   over their folder and ships it on USB.
2. **Merge.** The hub merges the incoming manifest into its local one. Per file,
   the **higher version wins**; provenance (who published the winning file) is kept.
3. **Verify.** Before indexing, the hub verifies files against the manifest
   (`content_manifest verify`) to catch tampering or corruption — changed,
   missing, or untracked files are reported, not silently trusted.
4. **Index.** Verified content is ingested by the existing `ingest_pdfs` path.

```bash
# Publisher side
python -m tools.content_manifest build --dir ./new_curriculum --publisher MoE-MY --version 4

# Hub side (after sneakernet copy)
python -m tools.content_manifest build --dir data/curriculum --merge --publisher local
python -m tools.content_manifest verify --dir data/curriculum
```

## Conflict resolution

- **Version wins:** higher `version` is adopted; ties favour the incoming push.
- **Authority precedence (policy):** where a school and a ministry both touch the
  same file, deployments may pin ministry content as authoritative — the manifest
  records publisher so this policy is enforceable.
- **Teacher contributions** (glossary, translation corrections) are additive and
  de-identified; they flow *up* via exported reports for model improvement rather
  than overwriting curriculum.

## Roadmap (trust hardening)

| Capability | Status |
|---|---|
| Checksums + versioning + provenance | ✅ `content_manifest` |
| Tamper/drift verification before indexing | ✅ `verify` |
| Decentralized merge (higher version wins) | ✅ `merge_manifests` |
| Cryptographic signatures per publisher | ⏳ add a `signature` field + public-key check |
| Hub-side signature trust store | ⏳ roadmap |
| Wire verify+merge into `sneakernet_sync.py` | ⏳ next integration step |

## Why this is sustainable

No central server is required: any publisher can produce a manifest offline, and
any hub can verify and merge it offline. Content stays current as long as *some*
local actor — ministry, NGO, school, or teacher — keeps publishing, which matches
how education systems actually maintain materials.
