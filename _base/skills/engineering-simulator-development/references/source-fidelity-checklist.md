# Source-Fidelity Checklist

Use this checklist when a simulator claims to reproduce an existing hardware/software system.

## Baseline

- Identify the writable simulator repository and every read-only reference repository.
- Record Git remote, branch, commit, build configuration, feature flags, and protocol revision.
- Confirm which revision is deployed or otherwise authoritative; do not use a convenient branch silently.
- Define the observable outputs that must match and the tolerances for physical approximations.

## Authority Matrix

| Concern | Preferred evidence |
| --- | --- |
| Coordinate frame and mechanics | drawings, CAD, measured geometry, explicit user datum |
| Accepted configuration values | production configuration UI plus its validators/import code |
| Calibration arithmetic | active RTL/firmware implementation and testbench |
| Wire behavior | packet producer, binary layout, capture, and consumer |
| Client reconstruction | production client source or verified executable behavior |
| Build/release | simulator repository scripts and clean-environment build |

Resolve contradictions instead of averaging them. Report which source won and why.

## Coordinate And Geometry Contract

- Define origin, axis directions, handedness, positive angle, units, normalization range, and face numbering.
- Define the zero datum geometrically, for example as the normal to a particular mirror face.
- Distinguish angular zero offset, source translation, source height, mirror-center displacement, and sensor/client rotation. Never compensate one with another without saying so.
- Draw or log the initial state and at least one easily checked symmetric state.
- Test face centers, edges, wraparound, and exact boundary angles.

## Digital Arithmetic Contract

For every value and intermediate, record:

- bit width and signedness;
- scaling and units;
- extension before arithmetic;
- width retained after multiplication;
- wrap, saturation, or clamp behavior;
- division rule, including negative-value rounding;
- lookup interval selection at an exact table node;
- interpolation order;
- handling of under-range, over-range, invalid, or skipped samples.

Implement these operations explicitly. Ordinary language integer or floating-point behavior is not evidence that the target RTL behaves the same.

Create golden vectors for:

- first and last table entries;
- exact interior nodes and values immediately on both sides;
- positive and negative slopes;
- maximum legal values;
- first overflow/wrap transition;
- division with a negative numerator;
- correction larger than the uncorrected coordinate;
- coordinate wraparound.

When possible, run the same vectors through an independent firmware/RTL simulator and compare exact integers.

## Configuration Tables

- Mirror production constraints for type, range, monotonicity, number of rows, and selectors.
- Apply identical bounds to typed edits, paste, imports, and mouse-wheel changes.
- Match import/export radix, order, count, endianness, and rejection behavior.
- Model interpolation between cells; do not treat table rows as isolated corrections when hardware interpolates.
- Distinguish “accepted by configuration software” from “safe in current digital arithmetic.”
- Warn about legal tables that trigger target overflow or sample rejection.

## Protocol And Client Reconstruction

- Model what is encoded, not what would be convenient to display.
- Trace a sample from scheduler through packet fields into the client point index.
- Determine whether every point carries an angle or whether a first angle plus fixed increment reconstructs the rest.
- Determine how skipped shots affect packet length, first angle, point count, new-packet boundaries, and client indexing.
- Do not draw “empty angular space” unless the client receives information that can represent that gap.
- Model no-return, missing sample, invalid distance, dropped packet, and intentionally unscheduled shot as different states when the protocol distinguishes them.
- Show physical rays separately from client reconstruction when the two can diverge.

## Validation Evidence

- Keep deterministic scenario/configuration fixtures.
- Test model, file formats, protocol, and GUI separately.
- Add differential tests against authoritative code or executable output.
- Visually inspect labels, units, table columns, ray density, zoom anchoring, and reconstructed geometry.
- Smoke-test the packaged artifact from a neutral working directory.
- Record source revisions and evidence in the simulator UI, test logs, or requested report.

## Stop Conditions

Do not claim exact equivalence when:

- the production revision is unknown;
- a critical branch or feature flag is guessed;
- protocol behavior is inferred only from a screenshot;
- floating-point code stands in for unverified fixed-width arithmetic;
- client reconstruction has not been checked;
- only source-mode tests passed but the packaged application was not run.
