# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a disk-backed cache implementation project for Pydantic objects, featuring a two-tier LRU cache with in-memory and SQLite-backed persistent storage.

The project follows the specification in `spec.md`.

Implementation follows the plan in `IMPLEMENTATION_PLAN.md` - and progress is updated there.

## Development Guidelines

### **Development Workflow Quick Start**
```bash
# 1. Validations
./devtools/run_all_agent_validations.sh    # Always run before responding
uv run pytest tests/test_specific.py -v       # Run specific tests for faster feedback

# 2. Common Commands
git status                                  # Check working directory
```


### **Testing & Validations Strategy**
**IMPORTANT**:
After ANY change, before responding to the user and before moving to the next sub-task or next task, 
the `./devtools/run_all_agent_validations.sh` must pass without any errors or warnings.
Don't accept any errors or warnings unless you failed fixing them.

All changes must pass full validation suite before user response.

In order to finish every task and sub-task, you must run `./devtools/run_all_agent_validations.sh`.
You must never move to the next sub-task before running `./devtools/run_all_agent_validations.sh` and getting a result
without errors or warnings.


🚨🚨🚨 ABSOLUTE ZERO TOLERANCE POLICY 🚨🚨🚨
**EVERY SINGLE TEST MUST PASS. EVERY SINGLE WARNING MUST BE FIXED.**
**🔥 BEFORE RESPONDING TO USER 🔥**
**YOU MUST ACHIEVE 100% SUCCESS ON ALL OF THESE:**

`./devtools/run_all_agent_validations.sh`
- ZERO test failures
- ZERO linting errors  
- ZERO type errors
- ZERO warnings

### **🔧 WHEN ANYTHING FAILS 🔧**

1. **STOP IMMEDIATELY**
2. **FIX THE ROOT CAUSE** (no workarounds)
3. **RE-RUN ALL VALIDATIONS**
4. **REPEAT UNTIL 100% SUCCESS**
5. **ONLY THEN** respond to user

**THERE ARE NO EXCEPTIONS TO THESE RULES.**

**✅ THERE ARE ONLY 2 ACCEPTABLE OUTCOMES ✅**
- All tests and validations pass as-is.
- You've tried to fix the errors and failed.


If you failed fixing, stop and tell the user.

### **🚫 FORBIDDEN PHRASES 🚫**

**NEVER SAY:**
- "Some tests are skipped but acceptable"
- "Only minor warnings remain"  
- "Most tests pass"
- "Timing issues are expected"
- "This is acceptable"
- "Tests pass in isolation but fail in parallel"
- "Serial mode fixes the problem"
- "Parallel execution timing issues"
- "Race conditions are expected"



## **Core Development Principles**
- **One Change = One Complete, testable Capability**
- **Validation-Driven Development** (every change must pass all validations)
- **Test-First Implementation** (behavior tests that target the API of the package are Priority 1)
- **No Layer-Based Changes**. Complete capabilities only - DO NOT implement multiple distinct capabilities in the same change. DO implement a capability and all its tests before continuing to the next capability.

### **Small parts principle**
Prefer breaking down functionality into small capabilities that are individually testable.
In addition to the external API-level tests, also create tests for the smaller capabilities.
For example, a serialization and deserialization capability based on the model type is individually testable.

### **Testing guidelins**
A test should almost always test a single fact about the behavior of the code. test_after_put_get_returns_the_object is a good example.

Test scope: Test behavior == cohesive whole == complete story
for example, in order to test put(), you also need to test get().
It's ok to test a small part of something larger - as long as that part is a "complete stroy" in itself.
Test behaviors instead of implementations (again, an implementation detail that is in itself a cohesive whole is fine to test).

Tests must be isolated so they never interfere with each other.

Tests must use clear language: decisive, specific and explicit.

Avoid using mocks. Simulators for quick tests are fine (for example, it's ok to test using in-memory sqlite some of the time instead of disk based for performance).

Test file names should be significant, specific and descriptive of content. 
GOOD: test_basic_put_and_get.py
BAD: test_step_03_basic_put_and_get.py
BAD: test_cache.py





## Architecture

The project implements a two-tier cache system as specified in `spec.md`:

- **In-Memory Cache**: Fast access, limited size, shorter TTL
- **SQLite Disk Cache**: Persistent storage, larger capacity, longer TTL
- **LRU Eviction**: Least Recently Used eviction strategy with count and size-based limits
- **Thread Safety**: Read-write locks for concurrent access

### Core Components

1. **CacheableModel** (`disk_backed_cache.py`): Base Pydantic model with schema versioning
2. **DiskBackedCache** (`disk_backed_cache.py`): Main cache implementation with SQLite persistence
3. **Tests** (`tests/`): Test suite covering cache operations

## Tool Configuration

- **Package Manager**: uv (all commands use `uv run`)
- **Python Version**: 3.13+
- **Linter/Formatter**: Ruff (configured in `pyproject.toml`)
- **Type Checker**: ty
- **Test Runner**: pytest with pytest-testmon and pytest-watch
- **Test Database**: Uses `:memory:` SQLite for testing

