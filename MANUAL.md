# CLI

lab-ops: Autonomous Scientific Intelligence OS

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `status`: Inspect registered repositories and verify...
* `report`: Summarize execution metrics and benchmark...
* `ingest`: Ingest a PDF research paper into local...
* `extract`: Query local literature store and extract...
* `changelog`: Synthesize raw Git commits into structured...
* `analyze-notebook`: Analyze cell outputs of a sandbox notebook...

## `status`

Inspect registered repositories and verify their paths on disk.

**Usage**:

```console
$ status [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `report`

Summarize execution metrics and benchmark results for a target repo.

**Usage**:

```console
$ report [OPTIONS]
```

**Options**:

* `-r, --repo <str>`: Target repo key from config (e.g. &#x27;mechanics&#x27;)  [required]
* `--help`: Show this message and exit.

## `ingest`

Ingest a PDF research paper into local LanceDB literature store.

**Usage**:

```console
$ ingest [OPTIONS] {pdf_path}
```

**Arguments**:

* `pdf_path`: Path to PDF research paper to ingest into local database  [required]

**Options**:

* `--help`: Show this message and exit.

## `extract`

Query local literature store and extract structured kinetic parameters for ODE bounds.

**Usage**:

```console
$ extract [OPTIONS] {query}
```

**Arguments**:

* `query`: Kinetic search query (e.g. &#x27;aPKC phosphorylation rate of Lgl&#x27;)  [required]

**Options**:

* `--help`: Show this message and exit.

## `changelog`

Synthesize raw Git commits into structured version release notes.

**Usage**:

```console
$ changelog [OPTIONS]
```

**Options**:

* `-r, --repo <str>`: Target repository key in config  [default: polarity]
* `--from <str>`: Git ref start (e.g., HEAD~15 or v0.1.0)  [default: HEAD~15]
* `--to <str>`: Git ref end (defaults to HEAD)  [default: HEAD]
* `--help`: Show this message and exit.

## `analyze-notebook`

Analyze cell outputs of a sandbox notebook and extract key findings.

**Usage**:

```console
$ analyze-notebook [OPTIONS] {notebook_path}
```

**Arguments**:

* `notebook_path`: Path to executed .ipynb file  [required]

**Options**:

* `--help`: Show this message and exit.
