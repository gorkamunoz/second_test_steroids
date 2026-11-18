---
id: 2
title: ./dash picks the wrong python when CONDA_DEFAULT_ENV matches but CONDA_PREFIX points elsewhere
type: bug
status: open
author: agent:worker
waiting_on: gorkamunoz
labels: []
links:
- thread:1
created: 2026-11-18 11:24
updated: 2026-11-18 11:24
---

In the watcher run for [[thread:1]], `./dash show 1` failed with `ModuleNotFoundError: No module named 'markdown'`.

**Cause** ([[file:dashboard/env.sh]], `_find_py`): the session had `CONDA_DEFAULT_ENV=second_test_steroids`, but
`CONDA_PREFIX=/home/gorka/miniforge3`, which is a different conda install's base env. Because the env *name* matched,
`_find_py` returned `$CONDA_PREFIX/bin/python` (miniforge base, which has no dashboard deps). The real env is at
`~/miniconda3/envs/second_test_steroids`.

**Workaround used:** `export PROJECT_PY=~/miniconda3/envs/second_test_steroids/bin/python`.

**Suggested fix:** in `_find_py`, only trust `$CONDA_PREFIX` when `basename "$CONDA_PREFIX"` equals `$ENV_NAME`,
or when that python can `import markdown`. Otherwise fall through to the folder search.
This touches `dashboard/`, so I didn't change it without asking.

<!-- comment author="agent:worker" date="2026-11-18 11:24" -->
Needs a go-ahead to change dashboard/env.sh (small fix described above).

_waiting on: gorkamunoz_
