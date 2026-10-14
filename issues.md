# Static Code Analysis Issues

Issues are ordered with higher-risk problems first. Line numbers refer to the original starter version of `bike_share_stations.py`.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection risk | Security (High) | 10 | Station name and numbers are concatenated directly into an SQL statement. A crafted name can change the query and input can break valid SQL. | Use parameterized SQL with `?` placeholders and pass all values separately. |
| Insecure PIN generation | Security (Medium) | 24 | `random.randint` is intended for general-purpose randomness, not security-sensitive PINs. | Use Python's `secrets` module to generate the PIN. |
| Mutable default argument | Correctness / maintainability (Medium) | 9 | `log=[]` is created once and reused across calls, so names can leak between independent calls. | Use `log=None` and create a new list inside the function when no list is supplied. |
| Missing-row crash in `hasBikes` | Correctness (Medium) | 39-42 | A station ID that does not exist makes `fetchone()` return `None`; indexing `row[0]` then raises an exception. | Check whether the query returned a row before accessing its value. |
| Silent exception handling | Reliability (Medium) | 33-37 | `resetStation` catches every exception and discards it, hiding failures from the caller. | Remove the broad `try/except`; report success/failure through the update row count and allow unexpected database errors to surface. |
| Missing return value in `rentBike` | Correctness (Low) | 17-21 | The function returns `None` in the no-bike or missing-station case, which makes the API less clear. | Return `False` for an unsuccessful rental and `True` only when a bike is rented. |
| Unused variable | Maintainability (Low) | 28-30 | `summary` is computed but never used. | Remove the variable. |
| Non-standard function naming and missing docstrings | Style (Low) | 9-44 | Names such as `addStation` do not follow PEP 8 snake_case, and functions lack descriptions. | Rename functions to snake_case and add docstrings. |
