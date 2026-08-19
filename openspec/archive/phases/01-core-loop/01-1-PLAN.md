---
phase: 1
plan_num: 1
objective: "Validate the complete exo-cortex skeleton against v0.1 requirements"
files:
  - "tests/verify-core-loop.sh"
status: "ready"
---

<plan>
  <objective>
    Create and run a verification script that tests all v0.1 requirements (R1-R10) 
    against the current implementation. Fix any gaps found.
  </objective>

  <execution_context>
    The implementation already exists (33 files from Phase 0). This plan validates 
    rather than builds. The test is a bash script that checks file existence, content 
    patterns, and cross-reference integrity.
  </execution_context>

  <context>
    This is a markdown-native framework — no compile step, no running server, no 
    unit test framework. Verification means: do the right files exist, do they contain 
    the right content, and do they reference each other correctly.
  </context>

  <tasks>
    <task type="auto" n="1">
      <name>Create verification script</name>
      <files>
        <file>tests/verify-core-loop.sh</file>
      </files>
      <action>
        Write a bash script that tests all requirements R1-R10 from REQUIREMENTS.md.
        Each requirement becomes a test function that checks file existence and 
        content via grep. Track pass/fail counts. Exit 0 if all pass, exit 1 if any fail.
      </action>
      <verify>
        bash tests/verify-core-loop.sh exits with status code (0 or 1)
        Script output shows pass/fail for each requirement group (R1-R10)
      </verify>
      <done>
        All R1-R10 requirements have corresponding test assertions
        Script produces clear pass/fail output per requirement
      </done>
    </task>

    <task type="auto" n="2">
      <name>Run verification and fix gaps</name>
      <files>
        <file>Any files flagged by verification</file>
      </files>
      <action>
        Run the verification script. For each failure, diagnose and fix the 
        underlying file. Re-run until all tests pass.
      </action>
      <verify>
        bash tests/verify-core-loop.sh returns exit 0
        All requirement groups R1-R10 show PASS
      </verify>
      <done>
        Zero test failures
        All cross-references resolve
        All required content present
      </done>
    </task>
  </tasks>

  <verification>
    <check>bash tests/verify-core-loop.sh returns exit 0</check>
    <check>Output shows 10/10 requirement groups passing</check>
    <check>No FAIL lines in output</check>
  </verification>

  <success_criteria>
    - All 10 requirement groups (R1-R10) pass verification
    - Script is reusable for future regression testing
    - Any gaps found in implementation are fixed
    - Verification results documented
  </success_criteria>
</plan>
