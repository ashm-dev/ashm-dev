## Hi there 🥷🏻

I'm Shamil Abdulaev, a backend and systems engineer. I contribute to CPython, glibc and the Python typing ecosystem, mostly memory-safety and concurrency fixes found with sanitizers.

## Open-source contributions

Each project below expands into the full list of my pull requests and issues. ✅ merged or resolved · 🟡 open. Pull requests closed without landing are left out. Updated daily by [a workflow](.github/workflows/update-readme.yml). Same list on [ashm-dev.github.io](https://ashm-dev.github.io/).

<!-- contributions:start -->
<details>
<summary><b>python/cpython</b> — 33 merged PRs · 43 issues</summary>

#### Pull requests

- ✅ [#157412](https://github.com/python/cpython/pull/157412) gh-157378: Fix SyntaxError.offset for "Non-UTF-8 code" error
- 🟡 [#157370](https://github.com/python/cpython/pull/157370) gh-157364: Fix use-after-free in TextIOWrapper during reentrant detach
- 🟡 [#157179](https://github.com/python/cpython/pull/157179) gh-157176: Fix GC tracking in PyStructSequence\_New
- ✅ [#156769](https://github.com/python/cpython/pull/156769) gh-156762: Fix tp\_clear slot signature for operator.methodcaller
- ✅ [#156403](https://github.com/python/cpython/pull/156403) gh-156402: Modernize annotation usage in libregrtest
- ✅ [#156300](https://github.com/python/cpython/pull/156300) gh-156114: Fix crash in perf trampoline with unencodable code names
- ✅ [#156130](https://github.com/python/cpython/pull/156130) gh-155911: Fix curses detection with libraries in LIBS
- ✅ [#150079](https://github.com/python/cpython/pull/150079) [3.13] gh-142831: Fix use-after-free in json encoder during re-entrant mutation (gh-142851)
- ✅ [#150078](https://github.com/python/cpython/pull/150078) [3.14] gh-142831: Fix use-after-free in json encoder during re-entrant mutation (gh-142851)
- ✅ [#148833](https://github.com/python/cpython/pull/148833) gh-148832: Use `-icf=0` in BOLT\_APPLY\_FLAGS
- ✅ [#148702](https://github.com/python/cpython/pull/148702) gh-148701: Add missing test coverage for asyncio.graph
- ✅ [#148595](https://github.com/python/cpython/pull/148595) gh-146553: Fix infinite loop in typing.get\_type\_hints() on circular \_\_wrapped\_\_
- ✅ [#146201](https://github.com/python/cpython/pull/146201) gh-146196: Fix potential Undefined Behavior in \_PyUnicodeWriter\_WriteASCIIString
- ✅ [#145840](https://github.com/python/cpython/pull/145840) gh-144712: Export \_Py\_jit\_entry symbol via PyAPI\_DATA
- ✅ [#144987](https://github.com/python/cpython/pull/144987) gh-144986: Fix memory leak in atexit.register()
- ✅ [#143097](https://github.com/python/cpython/pull/143097) Fix UBSan error in \_testcapi: correct create\_attr\_from\_spec signature
- ✅ [#142851](https://github.com/python/cpython/pull/142851) gh-142831: Fix UAF in `_json` module
- ✅ [#142492](https://github.com/python/cpython/pull/142492) gh-142476: fix memory leak when creating JIT executors
- ✅ [#141554](https://github.com/python/cpython/pull/141554) gh-141553: Fix incorrect function signatures in `_testmultiphase`
- ✅ [#141529](https://github.com/python/cpython/pull/141529) gh-42400: Fix buffer overflow in \_Py\_wrealpath for long paths
- ✅ [#140910](https://github.com/python/cpython/pull/140910) gh-140594: Fix an out of bounds read when feeding NUL byte to `PyOS_StdioReadline`
- ✅ [#140909](https://github.com/python/cpython/pull/140909) gh-140260: Fix data race in \_struct module initialization with subinterpreters
- ✅ [#140684](https://github.com/python/cpython/pull/140684) [3.13] gh-140301: Fix memory leak in subinterpreter PyConfig cleanup (GH-140303)
- ✅ [#140637](https://github.com/python/cpython/pull/140637) Remove dead stores to 'size' in UTF-8 decoder (unicodeobject.c)
- ✅ [#140585](https://github.com/python/cpython/pull/140585) Remove unreachable break statements in \_ctypes\_test.c
- ✅ [#140400](https://github.com/python/cpython/pull/140400) gh-140398: Fix memory leaks in readline module when PySys\_Audit fails
- ✅ [#140397](https://github.com/python/cpython/pull/140397) [3.13] gh-140306: Fix memory leaks in cross-interpreter data handling
- ✅ [#140307](https://github.com/python/cpython/pull/140307) gh-140306: Fix memory leaks in cross-interpreter data handling
- ✅ [#140303](https://github.com/python/cpython/pull/140303) gh-140301: Fix memory leak in subinterpreter PyConfig cleanup
- ✅ [#140274](https://github.com/python/cpython/pull/140274) gh-140272: Fix memory leak in \_gdbm.gdbm.clear()
- ✅ [#140265](https://github.com/python/cpython/pull/140265) gh-140257: fix data race on eval\_breaker during finalization
- ✅ [#140111](https://github.com/python/cpython/pull/140111) gh-140067: Fix memory leak in sub-interpreter creation 
- ✅ [#139271](https://github.com/python/cpython/pull/139271) gh-139269: Fix unaligned memory access in JIT code patching functions
- ✅ [#138667](https://github.com/python/cpython/pull/138667) gh-138665: Move `platform.invalidate_caches` docs
- ✅ [#134750](https://github.com/python/cpython/pull/134750) gh-134664: Document cleanup\_socket parameter in asyncio.start\_unix\_server()

#### Issues

- 🟡 [#158126](https://github.com/python/cpython/issues/158126) pickle.dumps() creates and discards an AttributeError on every call since 3.13.1
- 🟡 [#158090](https://github.com/python/cpython/issues/158090) Hang at shutdown: take\_gil() clears the GIL drop request after releasing gil-&gt;mutex
- 🟡 [#158086](https://github.com/python/cpython/issues/158086) JIT: test\_unittest fails with -X lazy\_imports=all: unittest.main is a module
- 🟡 [#157379](https://github.com/python/cpython/issues/157379) `_csv.reader`: NULL deref via re-entrant iterator that reaches EOF with an open quoted field
- 🟡 [#157378](https://github.com/python/cpython/issues/157378) Wrong `SyntaxError.offset` for "Non-UTF-8 code starting with ..." when a non-ASCII character precedes the invalid byte
- 🟡 [#157176](https://github.com/python/cpython/issues/157176) Memory leak on interpreter shutdown when reference cycle exists between `structseq` type and its instance
- 🟡 [#157062](https://github.com/python/cpython/issues/157062) Segfault during BOLT profile collection in `test_functools` (`fib`) when building with `--enable-bolt --enable-optimizations`
- ✅ [#156762](https://github.com/python/cpython/issues/156762) `_operator`: `methodcaller_clear` has the wrong signature for the `tp_clear` slot (returns `void`, not `int`)
- 🟡 [#156570](https://github.com/python/cpython/issues/156570) test.support.warnings\_helper.check\_warnings() raises KeyError: 'warnings' under -X lazy\_imports=all
- 🟡 [#156402](https://github.com/python/cpython/issues/156402) Modernize annotation usage in libregrtest
- ✅ [#151039](https://github.com/python/cpython/issues/151039) Crash: NULL deref in \_datetime when a static type outlives its module
- ✅ [#148832](https://github.com/python/cpython/issues/148832) Build: BOLT `-icf=1` breaks type-slot function-pointer identity, causes SIGSEGV
- ✅ [#148775](https://github.com/python/cpython/issues/148775) c-analyzer: bump MAX\_SIZES for Modules/clinic/\_testclinic.c.h
- ✅ [#148701](https://github.com/python/cpython/issues/148701) Add missing test coverage for asyncio.graph
- ✅ [#148443](https://github.com/python/cpython/issues/148443) Recursive \_testcapi.pyobject\_vectorcall() aborts with fatal stack overflow instead of raising RecursionError in a small-stack thread
- ✅ [#146429](https://github.com/python/cpython/issues/146429) Uninitialized variable replace usage in charmapencode\_output (Objects/unicodeobject.c) discovered by scan-build
- ✅ [#146196](https://github.com/python/cpython/issues/146196) Undefined Behavior in \_PyUnicodeWriter\_WriteASCIIString: NULL pointer passed to memcpy when len is 0
- ✅ [#145953](https://github.com/python/cpython/issues/145953) Segmentation fault in `test_call.py` (`c_recurse`) on Linux with Clang (LTO+PGO)
- ✅ [#144986](https://github.com/python/cpython/issues/144986) Memory leak in `atexit.register()`: missing `Py_DECREF` for `func_args` tuple
- ✅ [#142985](https://github.com/python/cpython/issues/142985) Build failure with `--enable-experimental-jit` and ASan: Memory leak in `allocate_executor` during module freezing
- ✅ [#142543](https://github.com/python/cpython/issues/142543) SIGSEGV in test\_isinstance and test\_json with --enable-experimental-jit=yes and --with-lto=full
- ✅ [#142476](https://github.com/python/cpython/issues/142476) ASan memory leak in test\_gc with --enable-experimental-jit (allocate\_executor)
- 🟡 [#141621](https://github.com/python/cpython/issues/141621) UBSan SEGV in `_Py_LazyJitTrampoline` when building with Clang and `--with-undefined-behavior-sanitizer` + experimental JIT
- ✅ [#141553](https://github.com/python/cpython/issues/141553) Fix incorrect function signatures in \_testmultiphase (UBSan)
- ✅ [#140431](https://github.com/python/cpython/issues/140431) Segfault in gc\_free\_threading.c after PR #140262 with ASAN build and free-threading tests
- 🟡 [#140404](https://github.com/python/cpython/issues/140404) LeakSanitizer detects memory leaks in test\_import with \_testsinglephase module in subinterpreter
- ✅ [#140398](https://github.com/python/cpython/issues/140398) Memory leaks in readline module when PySys\_Audit fails
- ✅ [#140332](https://github.com/python/cpython/issues/140332) MemorySanitizer: use-of-uninitialized-value in \_ssl.txt2obj via OpenSSL's OBJ\_txt2obj
- ✅ [#140306](https://github.com/python/cpython/issues/140306) Memory leak in test\_\_interpchannels: \_PyXIData\_New not freed in channel\_send
- ✅ [#140301](https://github.com/python/cpython/issues/140301) Memory leak in test\_capi with subinterpreter creation
- ✅ [#140272](https://github.com/python/cpython/issues/140272) Memory leak in \_gdbm.gdbm.clear() method: missing free() for gdbm\_firstkey() result
- ✅ [#140267](https://github.com/python/cpython/issues/140267) ThreadSanitizer reports thread leak in multiprocessing.Manager accepter thread
- ✅ [#140260](https://github.com/python/cpython/issues/140260) ThreadSanitizer: data race in \_struct module initialization with InterpreterPoolExecutor (free-threading build)
- ✅ [#140257](https://github.com/python/cpython/issues/140257) ThreadSanitizer: data race in interpreter\_clear() vs take\_gil() during finalization with daemon threads
- 🟡 [#140209](https://github.com/python/cpython/issues/140209) TSAN reports multiple data races, SEGV errors, and thread leaks when running the full test suite
- ✅ [#140159](https://github.com/python/cpython/issues/140159) Build Failure in posixmodule.c with Clang, ThreadSanitizer, and free-threaded build enabled
- ✅ [#140120](https://github.com/python/cpython/issues/140120) Memory leak in `hmac` module with HACL\* backend detected by AddressSanitizer
- ✅ [#140067](https://github.com/python/cpython/issues/140067) Memory leak in test\_sys with subinterpreters creation (AddressSanitizer detection)
- 🟡 [#139834](https://github.com/python/cpython/issues/139834) JIT: Segfault in \_Py\_LazyJitTrampoline with ASan/UBSan enabled
- ✅ [#139393](https://github.com/python/cpython/issues/139393) `test_capi.test_opt.test_call_len_known_length` fails on JIT+debug builds
- ✅ [#139288](https://github.com/python/cpython/issues/139288) JIT: Segmentation fault in \_Py\_LazyJitTrampoline when running test\_asyncio after gh-139269 fix
- ✅ [#139269](https://github.com/python/cpython/issues/139269) JIT: UB: unaligned store in `patch_*` functions
- ✅ [#127685](https://github.com/python/cpython/issues/127685) Performance Overhead in Ternary Operator Due to Value Loading vs Constant Loading

</details>

<details>
<summary><b>sqlalchemy/sqlalchemy</b> — 10 merged PRs · 2 issues</summary>

#### Pull requests

- ✅ [#13261](https://github.com/sqlalchemy/sqlalchemy/pull/13261) Add sqlite.JSONB type for binary JSON storage (SQLite &gt;= 3.45.0)
- ✅ [#13244](https://github.com/sqlalchemy/sqlalchemy/pull/13244) Remove unused TypeVars and compat import from typing modules
- ✅ [#13239](https://github.com/sqlalchemy/sqlalchemy/pull/13239) Add mypy ignore comments for Python 3.14 module imports
- ✅ [#12989](https://github.com/sqlalchemy/sqlalchemy/pull/12989) Fix parameter mutation in orm\_pre\_session\_exec()
- ✅ [#12988](https://github.com/sqlalchemy/sqlalchemy/pull/12988) Fix type hint for with\_for\_update() to support tuples of table classes
- ✅ [#12568](https://github.com/sqlalchemy/sqlalchemy/pull/12568) Remove unused typing imports
- ✅ [#12539](https://github.com/sqlalchemy/sqlalchemy/pull/12539) refactor(testing-and-utils): Remove unused code and fix style issues
- ✅ [#12538](https://github.com/sqlalchemy/sqlalchemy/pull/12538) refactor (sql): simplify and optimize internal SQL handling
- ✅ [#12535](https://github.com/sqlalchemy/sqlalchemy/pull/12535) refactor: clean up unused variables in engine module
- ✅ [#12534](https://github.com/sqlalchemy/sqlalchemy/pull/12534) refactor: simplify and clean up dialect-specific code

#### Issues

- 🟡 [#13281](https://github.com/sqlalchemy/sqlalchemy/issues/13281) Modernize type annotations to PEP 604 union syntax
- ✅ [#13240](https://github.com/sqlalchemy/sqlalchemy/issues/13240) mypy errors on Python 3.14 version-gated imports in compat.py

</details>

<details>
<summary><b>python/typeshed</b> — 9 merged PRs · 0 issues</summary>

#### Pull requests

- 🟡 [#16438](https://github.com/python/typeshed/pull/16438) [untangle] Update to 1.3.\*
- ✅ [#16426](https://github.com/python/typeshed/pull/16426) [PyMySQL] Update to 1.2.3
- ✅ [#14802](https://github.com/python/typeshed/pull/14802) fix(types): cr\_frame may be None
- ✅ [#14770](https://github.com/python/typeshed/pull/14770) cachetools: precise typing for decorators and cached(); expose cache\_info/cache\_clear and fix keys signatures
- ✅ [#14153](https://github.com/python/typeshed/pull/14153) Remove corus stubs
- ✅ [#14142](https://github.com/python/typeshed/pull/14142) Remove caldav stubs
- ✅ [#14141](https://github.com/python/typeshed/pull/14141) Remove pygit2 stubs
- ✅ [#13493](https://github.com/python/typeshed/pull/13493) remove pyOpenSSL stubs
- ✅ [#12596](https://github.com/python/typeshed/pull/12596) Improve type annotations in Flask-Cors stubs
- ✅ [#12585](https://github.com/python/typeshed/pull/12585) Add missing constants to flask-cors stubs

</details>

<details>
<summary><b>open-webui/open-webui</b> — 8 merged PRs · 6 issues</summary>

#### Pull requests

- ✅ [#24118](https://github.com/open-webui/open-webui/pull/24118) style(env): satisfy ruff lint on backend/open\_webui/env.py
- ✅ [#22987](https://github.com/open-webui/open-webui/pull/22987) refactor: modernize typing 
- ✅ [#22766](https://github.com/open-webui/open-webui/pull/22766) chore: align black with Ruff backend formatting
- ✅ [#22594](https://github.com/open-webui/open-webui/pull/22594) refactor: modernize type hints and imports in access\_control module
- ✅ [#22576](https://github.com/open-webui/open-webui/pull/22576) feat: add ruff linter &amp; formatter
- ✅ [#22265](https://github.com/open-webui/open-webui/pull/22265) feat: add OpenTelemetry system metrics instrumentation
- ✅ [#21453](https://github.com/open-webui/open-webui/pull/21453) i18n: Add missing Russian (ru-RU) translations
- ✅ [#8212](https://github.com/open-webui/open-webui/pull/8212) feat: Small optimization

#### Issues

- ✅ [#23793](https://github.com/open-webui/open-webui/issues/23793) feat: cache get\_user\_by\_id — 25% of all DB queries with zero caching
- ✅ [#21955](https://github.com/open-webui/open-webui/issues/21955) bug: Duplicate images displayed when model with thinking/reasoning generates an image (e.g., Gemini 3 Pro Image Preview)
- ✅ [#21641](https://github.com/open-webui/open-webui/issues/21641) feat: Add Ruff linter &amp; formatter for Python code quality
- ✅ [#21411](https://github.com/open-webui/open-webui/issues/21411) bug: File descriptor leak in audio.py and pipelines.py — open() without close
- ✅ [#21410](https://github.com/open-webui/open-webui/issues/21410) bug: Memory leak in SESSION\_POOL, USAGE\_POOL and YdocManager (with and without Redis)
- ✅ [#9491](https://github.com/open-webui/open-webui/issues/9491) Proxy Configuration via Environment Variables and Global Request Sessions

</details>

<details>
<summary><b>glibc (sourceware)</b> — 8 committed patches · 8 bugs</summary>

#### Patches

- 🟡 [patch 144254](https://patchwork.sourceware.org/patch/144254/) [v2] libio: Use \_\_wunderflow in \_IO\_getwline\_info
- 🟡 [patch 143415](https://patchwork.sourceware.org/patch/143415/) [v2] termios: Add tcgetwinsize and tcsetwinsize [BZ #32074]
- ✅ [patch 143055](https://patchwork.sourceware.org/patch/143055/) elf: Do not load cache extensions from an old-format ld.so.cache [BZ #34600]
- ✅ [patch 142924](https://patchwork.sourceware.org/patch/142924/) [v2] math: Set errno to ERANGE for logb (+-0) [BZ #6793]
- ✅ [patch 142808](https://patchwork.sourceware.org/patch/142808/) [v2] libio: Add test for fopen with an empty ", ccs=" value [BZ #34574]
- ✅ [patch 142193](https://patchwork.sourceware.org/patch/142193/) stdlib, wcsmbs: Add missing \_\_nonnull to strto\*/wcsto\* [BZ #33053]
- ✅ [patch 134886](https://patchwork.sourceware.org/patch/134886/) [v3] libio: Fix race in \_IO\_new\_file\_init\_internal initialization order [BZ #33785]
- ✅ [patch 134231](https://patchwork.sourceware.org/patch/134231/) hugepages: close fd on error path in \_\_get\_thp\_mode
- ✅ [patch 133861](https://patchwork.sourceware.org/patch/133861/) [v2] manual: clarify \_FILE\_OFFSET\_BITS Y2038 implications [BZ #34095]
- ✅ [patch 133858](https://patchwork.sourceware.org/patch/133858/) README: fix stale bug-reporting URL [BZ #34094]

#### Bugs

- 🟡 [BZ #34613](https://sourceware.org/bugzilla/show_bug.cgi?id=34613) sem\_open with O\_CREAT|O\_EXCL returns uninitialized pointer if write fails
- 🟡 [BZ #34612](https://sourceware.org/bugzilla/show_bug.cgi?id=34612) localedef: charmap ..(2).. ellipsis incorrectly treated as decimal range
- ✅ [BZ #34611](https://sourceware.org/bugzilla/show_bug.cgi?id=34611) wcsftime ignores '#' and '^' flags for %Z (regression introduced in 79b2667d1e)
- ✅ [BZ #34610](https://sourceware.org/bugzilla/show_bug.cgi?id=34610) fts\_open: invalid free on NULL parent with empty argv on allocation failure
- 🟡 [BZ #34609](https://sourceware.org/bugzilla/show_bug.cgi?id=34609) authdes\_pk\_create: free() called on uninitialized pointer on memory allocation failure
- 🟡 [BZ #34608](https://sourceware.org/bugzilla/show_bug.cgi?id=34608) wordexp: heap buffer overflow (write of size 1 to malloc(0)) expanding $\* or $@ with no positional arguments
- 🟡 [BZ #34607](https://sourceware.org/bugzilla/show_bug.cgi?id=34607) localedef crashes with SIGSEGV in handle\_ellipsis when LC\_COLLATE contains only an ellipsis
- ✅ [BZ #34600](https://sourceware.org/bugzilla/show_bug.cgi?id=34600) [2.44 regression] ld.so segfaults at startup with an old-format ld.so.cache

</details>

<details>
<summary><b>streamlit/streamlit</b> — 4 merged PRs · 0 issues</summary>

#### Pull requests

- ✅ [#13074](https://github.com/streamlit/streamlit/pull/13074) Fix empty Markdown code blocks rendering as “undefined”
- ✅ [#11090](https://github.com/streamlit/streamlit/pull/11090) Fix encoding
- ✅ [#10410](https://github.com/streamlit/streamlit/pull/10410) Time formatting logic update: seconds/minutes/hours display
- ✅ [#10358](https://github.com/streamlit/streamlit/pull/10358) Extend st.navigation functionality to support various page input types

</details>

<details>
<summary><b>typeddjango/django-stubs</b> — 3 merged PRs · 0 issues</summary>

#### Pull requests

- ✅ [#2504](https://github.com/typeddjango/django-stubs/pull/2504) fix format\_lazy typing
- ✅ [#2317](https://github.com/typeddjango/django-stubs/pull/2317) Add Typing for EmailField with Support for String Set and Get Types
- ✅ [#2316](https://github.com/typeddjango/django-stubs/pull/2316) Fixed bugs with RawQuerySet

</details>

<details>
<summary><b>ag2ai/ag2</b> — 1 merged PRs · 1 issues</summary>

#### Pull requests

- ✅ [#2111](https://github.com/ag2ai/ag2/pull/2111) fix(io): make console input non-blocking in async processor

#### Issues

- ✅ [#2110](https://github.com/ag2ai/ag2/issues/2110) [Bug]: Blocking I/O in AsyncConsoleEventProcessor halts the event loop

</details>

<details>
<summary><b>elastic/elasticsearch</b> — 1 merged PRs · 0 issues</summary>

#### Pull requests

- ✅ [#117235](https://github.com/elastic/elasticsearch/pull/117235) Deprecate ChunkingOptions parameter

</details>

<details>
<summary><b>celery/celery</b> — 1 merged PRs · 0 issues</summary>

#### Pull requests

- ✅ [#9173](https://github.com/celery/celery/pull/9173) Add check for soft\_time\_limit and time\_limit values

</details>

<details>
<summary><b>anthropics/claude-code</b> — 0 merged PRs · 1 issues</summary>

#### Issues

- 🟡 [#96014](https://github.com/anthropics/claude-code/issues/96014) [Feature Request] Reduce false positive rate in safety guardrails for benign code review requests

</details>

<details>
<summary><b>c3lang/c3c</b> — 0 merged PRs · 1 issues</summary>

#### Issues

- ✅ [#3155](https://github.com/c3lang/c3c/issues/3155) Add monadic operations (`map`, `bind`, `or_else`) to `std::collections::maybe`

</details>

<details>
<summary><b>llvm/llvm-project</b> — 0 merged PRs · 1 issues</summary>

#### Issues

- 🟡 [#163263](https://github.com/llvm/llvm-project/issues/163263) [BOLT] llvm-bolt segmentation fault during Python optimization with -frame-opt=hot after allocation combiner pass

</details>

<details>
<summary><b>pgadmin-org/pgadmin4</b> — 0 merged PRs · 1 issues</summary>

#### Issues

- ✅ [#8500](https://github.com/pgadmin-org/pgadmin4/issues/8500) Upgrade Dependencies and Base Systems to Latest Versions

</details>

<details>
<summary><b>litestar-org/litestar</b> — 0 merged PRs · 1 issues</summary>

#### Issues

- ✅ [#3848](https://github.com/litestar-org/litestar/issues/3848) Bug: Missing WebSocket Connection State Validation on Close and Message Send Operations

</details>
<!-- contributions:end -->
