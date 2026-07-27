# Scanning And LiDAR Lessons

Load this reference for rotating-mirror, polygon/cube-mirror, angular-grid, range-profile, or LiDAR client-emulation work.

## Geometry And Datum

- Define the angular zero mark as an explicit physical datum. If it is the normal to one mirror face, encode and display that definition instead of tuning an unexplained visual offset.
- Treat the outgoing beam origin and mirror geometry as independent parameters. Raising the source, changing its radial position, and changing angular zero are different operations.
- Verify a state where the beam should hit a face center. Use it as a regression fixture.
- Keep face numbering, active face, encoder mark, optical incidence, mirror rotation, and outgoing direction visible in diagnostics.

## Scan Grid And Sector

- Support arbitrary angular resolution within the real configuration range, while retaining useful presets.
- Include a coarse “one shot per face” mode when it is meaningful; permit values up to a 90-degree step when the device workflow requires it.
- Represent the sector with explicit start/end semantics and wraparound behavior.
- Show the shot grid, allowed shots, rejected shots, intersections, returns, and no-returns as distinct concepts.
- Report counts for generated grid nodes, scheduled shots, returns, no-returns, sector filtering, correction rejection, and packet splits.

## Scan Space

- Let the user define the space being scanned as object geometry or a range profile rather than only drawing free rays.
- Support deterministic profiles with line segments/polygons first; add curved or imported profiles only when needed.
- Compute the physical intersection and returned distance independently of how client software later places the point.
- Export point data with enough fields to audit grid angle, correction, physical direction, hit/no-hit, distance, packet index, transmitted first angle, and reconstructed client angle.

## Calibration Table Behavior

- Match production table validation exactly: signedness, integer-only rules, ranges, row counts, strictly increasing angle nodes, and import/export encoding.
- Interpolate between adjacent cells exactly as the active FPGA/firmware does.
- Preserve target intermediate widths and truncation order. A mathematically equivalent floating-point formula may disagree around overflow and exact-node boundaries.
- Make the correction sign explicit in the coordinate equation.
- Show the selected segment, neighboring nodes, interpolated correction, corrected raw angle, and skipped-node reason.
- Detect and report segments that overflow the active arithmetic even when every cell is accepted by the production configuration UI.

## Packet Reconstruction

Some scan protocols transmit one initial angle and let the client derive subsequent point angles as:

```text
angle[i] = first_angle + i * angular_resolution
```

For such a protocol:

- Do not insert visible angular holes merely because internal logic did not schedule a shot.
- Determine whether the device closes the current packet and starts a new packet with a new first angle after a skipped node.
- Reconstruct the client view from actual packet boundaries and point counts.
- Show physical directions and client-reconstructed directions side by side.
- Treat “no return sent,” “zero/invalid distance sent,” “shot omitted,” and “new packet started” separately.

## Interaction And Readability

- Zoom around the position under the mouse cursor, not automatically toward the LiDAR origin.
- Allow deep zoom beyond a small fixed factor and permit panning while zoomed.
- Provide fit/reset and a visible scale.
- Keep plots readable at dense angular resolutions through display decimation that does not alter simulated data.
- Retain presets and manual angular-resolution entry together.
- Permit table-cell editing by mouse wheel, but use the same integer step and bounds as direct entry.
- Size headings for the value and unit; use multiline headers or wider columns instead of clipping them.
- Move scan-space, calibration, packet, and client-reconstruction controls to a dedicated tab when the mechanical view becomes crowded.
