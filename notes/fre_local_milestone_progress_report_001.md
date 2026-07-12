# FRE local milestone progress report 001

Report date: 2026-07-12

Repository: `rookinc/fre`
Milestone class: completed local OpenFHE support-mode throughline

## 1. Executive summary

FRE has progressed from an empty research scaffold to a bounded,
contract-governed homomorphic computation with public, schema-validated
receipts.

The completed path now contains:

- an immutable mathematical contract;
- a closed public receipt schema;
- a six-row fixture declaration;
- a tested plaintext reference evaluator;
- a pinned and fail-closed OpenFHE backend;
- a predeclared one-shot execution gate;
- a private OpenFHE implementation;
- one completed four-fixture encrypted execution;
- an execution audit;
- four public receipts;
- an independent receipt-set audit; and
- a practical throughline document.

All four encrypted results matched the plaintext reference exactly.
The two certified uniform fixtures earned `regularity=true` receipts.
The two nonuniform fixtures remained algebraic controls and received
`regularity=unavailable`, because no geometric source certification was
available for them.

The implementation milestone is commit
`a7521e397e676e3deaf12c67c45e122260660c5d`. The practical throughline
documentation is commit
`4656da931685931c740ff127987b3ebeabc4b179`.

The repository is intentionally stopped at local closure. It does not
claim observational closure, production cryptographic security,
external truth, or a physical result.

## 2. Research synthesis

The working FRE design combines two distinct contributions.

Project 39 supplies the exact support-mode calculation. For six support
coordinates `h_i`, the repository computes:

- `S = sum(h_i)`
- `d_i = 6*h_i - S`
- `K = sum(d_i*d_i)`
- `computed_regular = (K == 0)`

For a source already certified inside the declared geometric domain,
`K=0` supports the regularity claim. Outside that certified source
boundary, the same polynomial remains a valid algebraic computation but
does not automatically become a geometric statement.

The Centroid witness-field work supplies the accountability discipline:
declare the comparison before execution, preserve source boundaries,
separate public and private material, record finite witnesses, and make
claims only when the receipt is congruent with the admitted computation.

Practically, FRE is the envelope joining those ideas. OpenFHE performs
the encrypted arithmetic. FRE controls admission and records what the
result is allowed to mean.

## 3. Phase history

### Phase 0: admission-locked scaffold

The project began with the backend closed. The initial repository
contained directory structure, boundary notes, a CMake scaffold, and
explicit prohibitions against key generation, encryption, evaluation,
decryption, or receipt emission.

This established the central rule: implementation capability must not
silently become execution authority.

### Phase 1: contract, schema, and fixtures

Contract `fre.support_mode.regularity.v0.1` fixed the six-coordinate
mathematical surface. Its SHA-256 is:

`25622e5185cd1289f28e51157d9236d13fc5ddaf863097522ac46b6d9e4ccda6`

The v0.1 public receipt schema closed the allowed fields and prohibited
private material and external-truth claims. Its SHA-256 is:

`6235f085e55fa00e07f380ab96531d50b0d45ef738ea6dc54f98a8e7a5d3bda9`

The fixture set declared six rows before evaluator work:

- two certified uniform geometric fixtures;
- two nonuniform algebraic controls;
- one invalid coordinate-count control; and
- one invalid nonpositive-support control.

Only the two uniform rows were certified in the geometric source class.

### Phase 2: plaintext reference

The C++ reference evaluator implemented checked integer calculation of
`S`, all six `d_i`, and `K`. It rejects malformed input before computing
a result and performs overflow checks.

All six declared fixture rows passed the reference audit. The positive
fixtures produced the expected values, while the two malformed controls
were rejected with the expected return classes.

This checkpoint was published as commit `b58c613`.

### Phase 3: fail-closed OpenFHE linkage

Existing Aletheos execution evidence was inspected before selecting a
profile. Executed evidence was ranked above plans and declarations. That
resolved two historical conflicts:

- planned ring dimension `2048` versus executed ring dimension `1024`;
- earlier depth `1` versus executed EvalMult depth `2`.

The pinned local test profile is:

- scheme: BGVRNS;
- OpenFHE version: 1.5.1;
- plaintext modulus: 65537;
- multiplicative depth: 2;
- ring dimension: 1024;
- batch size: 8; and
- security level: `HEStd_NotSet`.

OpenFHE was copied from a temporary build prefix to:

`~/dev/cori/toolchains/openfhe-1.5.1-termux-aarch64`

The copied libraries loaded successfully in dependency order:

`OPENFHEcore -> OPENFHEbinfhe -> OPENFHEpke`

The installed CMake metadata retained old absolute-prefix references, so
FRE did not pretend it was relocatable. The backend links directly to
the durable prefix. OpenFHE include directories are marked `SYSTEM`, so
third-party warnings do not weaken `-Werror` for FRE sources.

At this checkpoint the backend was available and linked, but the
profile was not admitted and crypto remained closed. This was published
as commit `3cc24b5`.

### Phase 4: pre-execution declaration

Contract v0.2 extended the already locked mathematical contract with a
bounded execution surface. Its SHA-256 is:

`a7c28f080730aa5fa7f4183573b1270794c3246939137aac4240d90eaf5a69ba`

The corresponding receipt schema SHA-256 is:

`3b256060e49d2f6599e9a1713eaf2c2b3aa27e135e5537ca8b967ee937127741`

The one-shot gate admitted exactly these seven operation stages:

1. `ContextGen`
2. `KeyGen`
3. `EvalMultKeyGen`
4. `Encrypt`
5. `EvalAdd`
6. `EvalMult`
7. `DecryptVerify`

`EvalSub` and rotations remained outside the gate.

The coordinate range was bounded to `1..22`. The maximum expected
absolute result was `288`, below the centered signed-safe bound `32768`
for plaintext modulus `65537`.

The pre-execution package was published as commit `ac4ce3f`.

## 4. Implemented encrypted circuit

OpenFHE runtime types remain private to
`src/backends/openfhe/openfhe_support_mode.cpp`. The public C++ header
contains only normalized result structures.

Each fixture encrypts six public support values and one public `-1`.
Subtraction is avoided as a separate admitted operation:

1. add the six encrypted supports to form `S`;
2. multiply encrypted `S` by encrypted `-1`;
3. build each `6*h_i` through additions;
4. add negative `S` to obtain each `d_i`;
5. square each `d_i`; and
6. add the squares to obtain `K`.

The predeclared structural count per fixture is:

- Encrypt: 7;
- EvalAdd: 46;
- EvalMult: 7; and
- DecryptVerify: 8.

Across the four-fixture batch, the declared counts are:

- ContextGen: 1;
- KeyGen: 1;
- EvalMultKeyGen: 1;
- Encrypt: 28;
- EvalAdd: 184;
- EvalMult: 28; and
- DecryptVerify: 32.

These are contract and circuit-structure counts, not a separate
instrumentation trace.

## 5. Observed execution

The one admitted batch executed once in runtime memory.

| Fixture | S | d | K | Reference |
| --- | ---: | --- | ---: | --- |
| `regular_uniform_10` | 60 | `[0,0,0,0,0,0]` | 0 | exact match |
| `regular_uniform_20` | 120 | `[0,0,0,0,0,0]` | 0 | exact match |
| `balanced_exchange_10` | 60 | `[6,-6,0,0,0,0]` | 72 | exact match |
| `balanced_exchange_20` | 120 | `[12,-12,0,0,0,0]` | 288 | exact match |

All unused packed slots decrypted to zero. No key, ciphertext, secret
input, or OpenFHE runtime object was committed.

The execution-audit artifact SHA-256 is:

`9f7dbc0b41ab1ab91ab6916ed7994361a81344ea86537e0ab676557900975f2d`

## 6. Receipt results

Four v0.2 public receipts were emitted and bound to the execution audit.

The certified uniform receipts have:

- input certification `certified_fixture_set_v0.1`;
- claim type `regularity`;
- claim status `earned`; and
- result `true`.

The balanced-exchange controls have:

- input certification `unavailable`;
- claim type `regularity`;
- claim status `unavailable`; and
- result `null`.

This distinction is deliberate. FRE records exact algebraic results for
the controls without manufacturing geometric authority.

All receipts use exact integer equality with tolerance zero, name all
seven admitted operations, record local closure, and set the
external-truth claim to false.

The independent receipt-audit artifact SHA-256 is:

`95325fa052ac6ea4016c7438ac97188a371dc956a585db3f7aa11dd8f5735276`

Its verdict is:

`schema_bound_receipt_congruence_for_bounded_local_batch`

## 7. Evidence and privacy model

The committed public face includes:

- contracts and schemas;
- profile and durable-prefix provenance;
- source and binary hashes;
- normalized fixture outputs;
- execution and receipt audits;
- claim status; and
- boundary statements.

The private runtime body included the OpenFHE context, key pair,
plaintexts, ciphertexts, and evaluated ciphertexts only while the
admitted process was running.

The repository contains no secret key, ciphertext body, serialized
runtime object, or hidden input. The fixtures are public and disposable.

The public receipt does not assert that cryptography proves geometry.
It asserts that an admitted encrypted computation produced output
congruent with its predeclared plaintext reference, and then applies the
predeclared certification rule.

## 8. Engineering incidents and repairs

Several failures improved the project boundary rather than weakening it.

- The initial GitHub publication check misread the default branch even
  though `main` was already correct. A targeted read-only repair verified
  local, remote, visibility, and branch state.
- A porcelain-status parser stripped the leading space from modified
  tracked files. It was repaired to preserve Git's two-column status
  format.
- The durable-prefix loader initially attempted `OPENFHEpke` before its
  `OPENFHEbinfhe` dependency. The load order was corrected.
- Relocated OpenFHE CMake metadata proved nonrelocatable. FRE adopted
  explicit durable-prefix linkage instead of recording a false
  relocation claim.
- OpenFHE header warnings were promoted by FRE's `-Werror`. Third-party
  includes were marked `SYSTEM`; FRE's own warning policy stayed strict.
- A CLI checker searched escaped JSON text incorrectly. The checker was
  repaired without changing the already-correct CLI source.
- The checkpoint clipboard was temporarily overwritten by a nested audit
  report. A read-only HEAD/origin verification proved the implementation
  commit had already succeeded.
- Markdown hard-break whitespace was rejected by `git diff --check`. It
  was replaced with a blank line before the documentation commit.

These incidents are part of the practical FRE story: evidence parsers,
build metadata, and publication checks are themselves inside the
accountability surface.

## 9. Current boundary

The one-shot v0.2 gate is consumed. Its committed JSON remains an
immutable record of pre-execution admission, not permission to rerun the
smoke indefinitely.

The completed milestone establishes:

- exact plaintext calculation;
- bounded encrypted calculation;
- encrypted/reference congruence for four declared public fixtures;
- correct claim withholding for uncertified controls;
- public/private material separation; and
- local receipt congruence.

It does not establish:

- observational closure;
- generalization beyond the four admitted fixtures;
- independent external verification;
- production-security parameters;
- secret-input privacy performance;
- a physical regularity result; or
- external truth.

A future observational phase must be a separate contract revision and
gate. It should use independently sourced inputs, preserve anti-tuning
rules, define repetition and failure handling in advance, and preferably
use an independently operated verifier. A production-security phase
would additionally require a security-bearing OpenFHE profile and a
fresh performance and correctness budget.

## 10. Milestone conclusion

The FRE project now has a complete, honest local throughline.

The important achievement is not merely that OpenFHE returned the right
numbers. The project demonstrates that encrypted computation can be
surrounded by a finite accountability envelope: source class,
predeclared circuit, bounded admission, runtime privacy, exact reference
comparison, claim discipline, public receipt, and explicit closure
limits.

That is the practical value contributed by the Project 39 calculation
and the Centroid receipt architecture together.
