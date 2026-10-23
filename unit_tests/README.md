# Assignment 3 - Unit Test Automation (pytest)

Project under test: [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python) (our fork).
Modules under test: `data_structures/stacks/stack.py`, `data_structures/queues/circular_queue.py`, `maths/prime_check.py`.

## Task 1 - Local setup (Python 3.12 or newer)
```bash
git clone https://github.com/<group-account>/Python.git
cd Python/unit_tests
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1      Linux/macOS:  source .venv/bin/activate
pip install -r requirements-test.txt
python -m pytest            # must show: 168 passed, 1 xfailed
```
Python 3.12+ is required because `Stack` uses the `class Stack[T]` syntax. Nothing from the repo's own
`pyproject.toml` needs installing; this suite only imports the pure-Python modules.
Always run pytest from `unit_tests/` (or `pytest unit_tests` from the repo root) so our `pytest.ini` is used.

## Task 2/3 - What is where
| Path | Content |
|---|---|
| `tests/24F-3001/`, `tests/24F-3057/` | automated tests, one folder per person |
| `docs/notes_24F-3001.md`, `docs/notes_24F-3057.md` | ECP / BVA notes |
| `data/*.csv` | external test data consumed by the CSV-driven tests |
| `test_cases_24F-3001.xlsx`, `test_cases_24F-3057.xlsx` | Excel test-case sheets (TC ID matches CSV `tc_id`) |
| `tools/build_excel.py` | regenerates the Excel files from the CSVs + latest results |

## Task 4 - Running (groups, order, parallel, parameterization)
```bash
python -m pytest                                  # everything, in group order
python -m pytest -n auto --dist loadgroup         # parallel (pytest-xdist); one worker per module group
python -m pytest -m smoke                         # suites by marker
python -m pytest -m 24F-3001                      # only Person A's tests
python -m pytest -m "stack and bva"               # combine markers
python -m pytest -m "not csv_driven"
python -m pytest -k "enqueue"                     # by name
python -m pytest --html=reports/report.html --self-contained-html   # HTML report (summary evidence)
python -m pytest --junitxml=reports/junit.xml && python tools/build_excel.py   # refresh Excel status
```
- **Groups (markers):** `stack` `queue` `prime` | `24F-3001` `24F-3057` | `smoke` `ecp` `bva` `negative` `scenario` `csv_driven`
  (declared in `pytest.ini`, `--strict-markers` catches typos).
- **Order:** `conftest.py` numbers every test: `smoke -> ecp -> bva -> negative -> scenario -> csv_driven`.
  Inside a group use `@pytest.mark.case_order(n)` (1-99; default 50). Serial runs follow this exactly; with `-n`
  the order holds per worker only.
- **Parallel:** `pytest-xdist`; `@pytest.mark.xdist_group` + `--dist loadgroup` keeps each module's tests on one worker.
- **Parameterization:** `@pytest.mark.parametrize` everywhere; CSV tests build their parameters from `data/*.csv`.

## Who commits what
**Person A**
- infra (shared): `README.md`, `pytest.ini`, `conftest.py`, `requirements-test.txt`, `.gitignore`, `tools/build_excel.py`
- `tests/24F-3001/*`, `data/prime_ecp.csv`, `data/stack_scenarios.csv`, `docs/notes_24F-3001.md`, `test_cases_24F-3001.xlsx`

**Person B**
- `tests/24F-3057/*`, `data/prime_bva.csv`, `data/queue_scenarios.csv`, `docs/notes_24F-3057.md`, `test_cases_24F-3057.xlsx`

**Both / whoever records it:** setup video (Task 1, same for all) and `reports/report.html`.
GitHub rejects files over 100 MB: keep the video short and compressed, or commit it as `unit_tests/docs/setup_video.md` containing the Drive/YouTube link if it is too big.

Git flow that keeps history attributable (graded under "Task distribution"):
```bash
git pull
git checkout -b person-a-tests          # Person B: person-b-tests
git add <your files only>
git commit -m "Add stack push/pop/peek tests with ECP/BVA"   # several small commits, not one big one
git push -u origin person-a-tests       # open PR, other person merges
```
Make sure each of you has `git config user.name` / `user.email` set to your own GitHub identity before committing.

## Known finding (xfail, on purpose)
`Stack(-1).is_full()` is `False` although `push()` raises `StackOverflowError` - see `docs/notes_24F-3057.md`.
