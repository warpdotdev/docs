# Docs consistency audit run log

Scheduled and manual runs prepend one compact entry through the standing state branch.

## 2026-10-14 — blocked
- Run: https://platform.staging.warp.dev/rBn42naTYeqJPuRZ7i7KOR/runs/01a13b5b-4e26-7614-a96d-c65e1b73194a
- Source commits: docs 2756ce2feecfec803f356fb90b945408a4adb114; warp 9e57f4f6a5c521f62ddacfa1413b66b9c162440f; private authority revision retained transiently
- Coverage: blocked; 8/388 pages extracted; comparison unavailable
- Findings: 0 new; 0 changed; 0 resolved; 2 active
- Suppressed: 0; expired: 0
- Cost: 63535 characters; 0 candidates (prepass blocked); 2 model JSON generations
- Sources unavailable: generated CLI help; blocker: trailing-slash redirect normalization
- State PR: https://github.com/warpdotdev/docs/pull/876

## 2026-10-07 — partial
- Run: https://platform.staging.warp.dev/rBn42naTYeqJPuRZ7i7KOR/runs/01a1174e-c87a-7dd8-b072-61ac8c8cbab5
- Source commits: docs 3aa4a90e8914a3039d38d86c3cfa265720f59736; warp d888f2946c57e570ba822f72dc79c79728cc1fac; warp-server a361c4d7c5e161bd661c9b47cccb7ed999e41307
- Coverage: partial; 80/387 pages
- Findings: 2 new; 0 changed; 0 resolved; 2 active
- Suppressed: 0; expired: 0
- Cost: 606525 characters; 22 candidates; 80 model calls
- Sources unavailable: none
- State PR: unavailable
