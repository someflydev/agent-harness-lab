# Traceability Graph And Semantic Retrieval

Future retrieval should help operators find durable evidence faster without
turning derived storage into a second source of truth.

## Source Of Truth

Repo files and git history remain authoritative. Prompts, docs, runbooks,
templates, reports, findings, schemas, helper scripts, and commits are the
records that future sessions should trust. Any graph or vector index must be
derived, disposable, and rebuildable from those records.

## Graph Guidance

Graph-style structure may later help answer "what is connected and why?" Useful
edges could connect prompts to changed files, run records to validation
commands, findings to evidence, runbooks to templates, or commits to prompt
ids. The value of a graph is traceability: a reviewer should be able to follow
an edge back to a concrete path or commit.

Neo4j is one possible future tool for this kind of structure, but it is not a
current dependency or preferred requirement.

## Semantic Retrieval Guidance

Semantic retrieval may later help answer "what is similar or likely relevant?"
It could support prompt authors looking for related prior prompts, operators
looking for a matching runbook, or reviewers looking for similar findings.

Qdrant is one possible future tool for vector retrieval, but it is not a
current dependency or preferred requirement.

## Graph First, Vector Second

A useful later pattern may be graph-first narrowing and vector-second
enrichment. The graph can constrain retrieval to trusted durable artifacts and
known relationships. Semantic search can then rank likely relevant documents
within that narrowed set.

This order keeps retrieval anchored to explicit evidence instead of letting
similarity scores decide authority.

## Boundaries

Neither graph nor vector storage should become a dumping ground. Raw assistant
transcripts should not be indexed by default. Temporary handoffs, scratch
notes, and local runtime files should enter durable retrieval only after an
explicit review or promotion path converts them into repo artifacts.

This page is architecture guidance, not an implementation plan.
