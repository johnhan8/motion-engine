# Motion Engine v1 — System Definition

This document is the **guiding vision** for this repository: scope, architecture intent, constraints, and direction. Prefer it when choosing between features or tradeoffs; use `ARCHITECTURE.md` alongside it for structural rules (especially IMU vs legacy).

---

## Goal

Build a real-time motion processing engine that ingests IMU (and later vision) data and outputs stable motion state representations for downstream classification and analysis.

---

## IMU pipeline: architecture boundaries

The **active** system is a single real-time **IMU motion pipeline**. Data flows in one direction across **layers**. Each layer has a narrow responsibility and must not leak concerns from layers below or above except through defined data types.

**Data flow (target mental model)**

```text
Sensor ingestion → Filtering → Feature extraction (future) → Output / downstream consumers
        ↑                ↑              ↑                              ↑
   sensors/          filtering/   (reserved; see below)     core/pipeline.py loggers
```

**Orchestration (current)**  
`core/pipeline.py` composes ingestion + filtering + output logging. **`main.py`** is the CLI entrypoint and delegates to `core.pipeline.run` only (see `ARCHITECTURE.md` for stability rules).

---

### Sensor ingestion layer

**Responsibility:** Produce **raw** IMU readings at the pipeline’s nominal rate: 3-axis accelerometer and 3-axis gyroscope, as structured samples.

**Owns**

- **`sensors/`** — today: `ImuSimulator`, `ImuSample` (`sensors/imu_simulator.py`).

**Boundary rules**

- This layer exposes **sensor-side** concerns only (synthetic or, in future, hardware): units consistent with simulator/docs, timestep advance internal to the source or driven by orchestration pacing.
- It **does not** import **`filtering/`** or **`core/pipeline.py`**, and must **not** depend on **`perception/`** or **`exercises/`** (see `ARCHITECTURE.md`).
- Raw samples are handed **up** to the pipeline; smoothing, features, and interpretation happen elsewhere.

---

### Filtering layer

**Responsibility:** Turn each raw IMU sample into a **filtered** sample (same physical quantities, reduced noise/jitter).

**Owns**

- **`filtering/`** — today: `EmaFilter`, `FilteredImuSample`, and `ScalarEma` (`filtering/ema_filter.py`). The IMU path uses **`EmaFilter`** over full `ImuSample` payloads.

**Boundary rules**

- Consumes **`ImuSample`** (or equivalent raw contract); emits **`FilteredImuSample`** (or equivalent filtered contract).
- **No** ingestion of streams from **`perception/`** or **`exercises/`**.
- Algorithms stay **purely signal-level** until a dedicated feature stage exists; no classification or semantic labels here.

---

### Feature extraction layer (future)

**Responsibility:** From a **series** or **window** of filtered samples, compute compact **motion features** (statistics, deltas, energies, norms) for classification, dashboards, or logging.

**Status:** **Not implemented** as a dedicated package in the IMU path yet. Reserved boundary: new code should live in a **separate**, IMU-only module set (for example top-level placeholders like `features/` remain available; naming and layout TBD when implemented) and **consume** filtered output only.

**Boundary rules**

- Inputs: filtered timeline (and timestamps when added). Outputs: feature vectors / records for downstream jobs.
- **No** coupling to **`perception/`** inside core IMU orchestration unless an explicit fusion project adds a documented bridge (out of scope for the default pipeline).

---

### Output surface (within orchestration today)

**Responsibility:** Emit each tick’s data for observability or export.

**Current implementation**

- **`core/pipeline.py`** defines loggers (`ConsoleLogger`, `CsvLogger`) and calls them once per iteration inside `ImuPipeline.run`.

This is **orchestration + I/O**, not a separate architectural “layer,” but bounded so it stays thin: format and write-only, no physics or semantics.

---

## Main execution loop: real-time constraints

The **principal** loop runs in **`core/pipeline.py`** (`ImuPipeline.run`), driven by **`ImuSimulator`** reads, **`EmaFilter`** updates, logger callbacks, pacing via **`sample_rate_hz`**, and optional **`time.sleep`** alignment.

**Non-negotiables for default “real-time” operation**

1. **No blocking waits** unrelated to pacing (no network/filesystem dialogs, no `input()` in the steady path).
2. **Bounded work per tick**: one raw read → one filter update → bounded logging (today: print one line or append one CSV row).
3. **Monotonic progression of wall-clock timestamps** inside the loop (enforced today by assertions in `core/pipeline.py`).

**Current caveats (documented deviations)**

- **`--interactive-tuning`** in `main.py` uses **`stdin` / `input()`** inside the loop: useful for tuning **EMA alpha** manually, **not** real-time safe; treat as developer-only mode.
- **CSV logging** performs a **synchronous write per sample**: acceptable at moderate rates and log sizes; for very high throughput, future work may buffer or offload I/O explicitly.

**CLI entry constraint**

- **`main.py`** should remain a **thin shell**: argument parsing → **`core.pipeline.run`**, preserving the documented entry path and isolation from legacy stacks.

---

## Current behavior (summary)

- Continuous paced loop (`ImuSimulator`; rate from `sample_rate_hz` on `ImuPipeline`)
- Prints raw + filtered vectors (CSV via `scripts/run_imu_harness.py`)
- **`alpha`** controls EMA smoothing strength
- Runtime checks: **3-axis** accel/gyro shapes, finite filtered values; **strictly increasing** `time.perf_counter()` timestamps in the run loop when more than one sample is taken

---

## Legacy system

KineticAI vision-based tracking (`perception/`, `exercises/`, `session/`, etc.) is **out of scope** for default IMU work and **must not** be imported by **`core/pipeline.py`** for the stable IMU path. Retained for future integration; see **`ARCHITECTURE.md`**.

---

## Next development goals (architecture-aligned)

- **Sensor ingestion:** timestamped samples, calibration hooks; hardware backend behind same boundary as **`ImuSimulator`**.
- **Filtering:** alternative filters behind the same ingest/emit contracts as **`EmaFilter`**.
- **Feature extraction:** implement the dedicated layer consuming **filtered windows** without bloating **`ImuPipeline.run`** (or move heavy work explicitly off-thread with a defined contract later).
- **Structured logging:** JSONL or schema’d logs alongside CSV; keep hot path predictable.
- **Future:** classification / vision fusion only via explicit modules and contracts—not by routing legacy perception into **`core/pipeline.py`**.

---

## Long-term vision

This system evolves into a **multi-sensor motion intelligence engine** suitable for **rehabilitation / physical therapy feedback**: stable representations, reproducible logs, and clear layer boundaries from acquisition to actionable output.
