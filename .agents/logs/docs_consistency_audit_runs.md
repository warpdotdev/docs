# Docs consistency audit run log

Scheduled and manual runs prepend one compact entry through the standing state branch.
## 2026-10-30 — partial
- Run: https://staging.warp.dev/conversation/9774d58d-c11f-4ebe-93ec-652abf6cb0cc
- Source commits: docs 232cf27943a1fbbc11eead43792cf224e4b5f226; warp b17a2ed0207a4aaf5e2481e1da1d4460e0852e42; private authority revision retained transiently
- Coverage: partial; 8/400 pages extracted; 61 unchanged pages reused; 331 deferred with prior manifest hashes and shards preserved
- Findings: 1 new; 0 changed; 0 resolved; 3 active; 2 saved privacy findings carried forward, not rechecked (retention exception and training-policy wording)
- Suppressed: 0; expired: 0; 16 candidates unverified pending fresh extraction or additional scope evidence
- Cost: 87687 characters; 29 candidates; 3 model JSON generations
- Sources unavailable / blocker: generated CLI help not collected (public source fallback used); no blocker
- State PR: https://github.com/warpdotdev/docs/pull/876
## 2026-10-28 — partial
- Run: https://staging.warp.dev/conversation/50454ccd-1ed3-4373-96bc-37cb88a3741e
- Source commits: docs 17b29842c15b738de6febb400b13ae9d08e9d9e2; warp 23adf48cf4e4c57416dcb078b25bcb04472e575c; private authority revision retained transiently
- Coverage: partial; 8/392 pages extracted; 53 unchanged pages reused; 331 deferred with prior manifest hashes and shards preserved
- Findings: 0 new; 0 changed; 0 resolved; 2 saved active carried forward, not rechecked (retention exception and training-policy wording)
- Suppressed: 0; expired: 0; 17 candidates unverified pending fresh extraction
- Cost: 70912 characters; 26 candidates; 2 model JSON generations
- Sources unavailable / blocker: generated CLI help not collected (public source parsing used); no blocker
- State PR: https://github.com/warpdotdev/docs/pull/876
## 2026-10-21 — blocked
- Run: https://platform.staging.warp.dev/rBn42naTYeqJPuRZ7i7KOR/runs/01a15f67-d1a4-7180-a751-cfb4cf077bfb
- Source commits: docs 1bec888607558cd9c727fc324058bfbcce86eab4; warp 96d816ad2b3881418b56d946e70bfb004e89bd03; private authority revision retained transiently
- Coverage: blocked; 0/390 pages extracted; 30 redirect-normalization cycle errors across 718 routes
- Findings: 0 new; 0 changed; 0 resolved; 2 active (unchanged)
- Suppressed: 0; expired: 0
- Cost: 0 characters; 0 candidates; 0 model calls
- Sources unavailable: authorities not refreshed after normalization blocker; prior manifest, shards, backlog, findings, and receipts preserved
- State PR: https://github.com/warpdotdev/docs/pull/876
## 2026-10-19 — blocked
- Run: https://platform.staging.warp.dev/rBn42naTYeqJPuRZ7i7KOR/runs/01a1551b-199b-7a92-8522-9ca4250507e1
- Source commits: docs 87e5182b9a0c2e6d6c5a2f206a620b3d02796b35; warp d5667a308e5d1000554097db1d18e9132872cb75; private authority revision retained transiently
- Coverage: blocked; 0/390 pages extracted; 30 redirect-normalization cycle errors across 549 routes, including /agents
- Findings: 0 new; 0 changed; 0 resolved; 2 active (unchanged)
- Suppressed: 0; expired: 0
- Cost: 0 characters; 0 candidates; 0 model calls
- Sources unavailable: authorities not refreshed after normalization blocker; prior manifest, shards, backlog, findings, and receipts preserved
- State PR: https://github.com/warpdotdev/docs/pull/876
## 2026-10-16 — blocked
- Run: https://platform.staging.warp.dev/rBn42naTYeqJPuRZ7i7KOR/runs/01a145a8-058e-7318-8016-1047a48522e3
- Source commits: docs 756982e49a28058e6657616d262660b333aed779; warp a38e4416db8ab94953f6e780b1996cfd9bca7e8e; private authority revision retained transiently
- Coverage: blocked; 0/388 pages extracted; 30 redirect-normalization cycles, first at /agents
- Findings: 0 new; 0 changed; 0 resolved; 2 active (unchanged)
- Suppressed: 0; expired: 0
- Cost: 0 characters; 0 candidates; 0 model calls
- Sources unavailable: authorities not refreshed after normalization blocker; prior manifest, shards, backlog, findings, and receipts preserved
- State PR: https://github.com/warpdotdev/docs/pull/876

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
