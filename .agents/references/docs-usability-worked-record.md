# Worked usability record

Synthetic example using the [validation record template](../templates/usability-validation.md), not a live product test. Paths and versions below identify supplied fixture text, not deployed pages.

## Usability validation

* Scope: A browser-only invitee needs to accept an invitation or find a supported next action. Q1 is the primary task. Product changes are excluded.
* Scenarios: Browser-only and blocked-action scenarios map to Q1. Novice context is included. Admin setup and existing configurations do not apply to accepting this invitation.
* Tested version: Synthetic `fixture-v1`, followed by `fixture-v2`; no local changes or preview. No real test time applies to this illustrative record.
* Method and limitations: Rendered-text inspection of the supplied `/invite` page. No search, visual, responsive, accessibility, authentication, or product interactions were tested.

### Q1: How do I accept my invitation if I only have a browser?

* Persona and priority: Invitee who cannot install an app on this device; primary, selected before testing.
* Sufficient answer: State whether browser acceptance is supported and give a next action if it is not.
* Entry and path: Direct arrival at `/invite` from the synthetic invitation. No outgoing links, redirects, or preview escapes.
* Answer evidence: `fixture-v1`, `/invite`, “Accepting an invitation”: “Open the Example desktop app to accept your invitation.” This is the entire answer on the tested path.
* Result: Partial.
* Findability and completeness: The invitation reaches the answer, but the answer leaves the browser-only reader without an explicit limitation or recovery step.
* Finding and next action: Primary-task blocker at `/invite`. State the limitation and identify a supported device or the person who can help. Initial readiness: blocked.
* Correction: In `fixture-v2`, replace the answer with: “Invitation acceptance requires the Example desktop app; browser acceptance is unsupported. If you cannot install the app on this device, open the invitation on a device where installation is allowed, or ask your administrator for an approved device.”
* Retest: Same Q1, persona, sufficient answer, and invitation path on `fixture-v2`. Clear: the replacement states the limitation and gives a supported next action. The original Partial result and passage above remain part of the record. This does not claim the invitation was accepted in a product.

### Readiness

Ready for review within this synthetic text walkthrough after the Q1 retest. No known primary-task docs blocker remains. Product behavior and availability still require their separate verification; this example grants no human acceptance for an untested real journey.
