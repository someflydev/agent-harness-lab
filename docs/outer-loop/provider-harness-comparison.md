# Provider Harness Comparison

This comparison keeps driver choices explicit. AHL driver records are local
contracts, not provider support claims.

| Driver | Safety Boundary | Auth | Output Capture | Model Selection | Testing Posture |
| --- | --- | --- | --- | --- | --- |
| Codex subscription CLI | Live runs require `outer run --execute`; probes use PATH and help only. | Operator authenticates outside AHL. | Final-message capture remains unverified; no raw transcripts by default. | Passed only when the contract marks selection verified or supported. | Unit tests may mock subprocess calls; no real provider calls. |
| Gemini subscription CLI | Same explicit execute and probe boundary as Codex. | Operator authenticates outside AHL. | Final-message capture remains unverified; no raw transcripts by default. | Passed only when verified or supported. | Unit tests may mock subprocess calls; no real provider calls. |
| Pi external harness | Live invocation is `manual-confirmation-required` until print/JSON behavior is verified. | Pi owns subscription login, API keys, provider config, and package settings. | Help previews and dry-run metadata are safe; print/JSON final capture is unverified. | Pi owns provider, model, and thinking selection. AHL records requested values only. | Tests cover registry shape, probe degradation, dry-run planning, and guarded live execution without invoking Pi. |
| Manual driver | Human operator controls the assistant session. | Whatever tool the operator chooses. | Human summarizes outcomes into durable artifacts. | Human chooses model in the external tool. | Tests verify no subprocess invocation and manual-action records. |
| Future API-backed drivers | Must add explicit cost, credential, rate-limit, logging, and consent design first. | AHL would need reviewed credential handling before implementation. | Structured capture may be possible but needs transcript and retention policy. | Driver-specific provider API parameters. | Requires fake providers, fixtures, and no live network calls in tests. |

Codex and Gemini are the smallest live-run candidates because AHL can treat
them as subscription CLIs. Pi is richer but less direct: it is a harness that
may run many providers and extensions internally. API-backed drivers are a
separate future category because they would make AHL responsible for provider
credentials and direct API behavior.
