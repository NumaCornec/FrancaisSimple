# FrancaisSimple

An agent skill that forces an LLM to write readable technical French in one pass, with the discipline of a controlled language.

The skill bans the four habits that make machine-written French hard to read: the conditional, the subjunctive, the present participle, and nominalization. It ships with a deterministic linter, a reproducible benchmark, and no runtime dependency beyond the Python standard library.

## Example

**Before** (unedited model output):

> **Connexion timeouts.** If sqlpipe hangs or fails with `dial tcp: i/o timeout`, you should check that the host running sqlpipe can actually reach the Postgres port (usually 5432) — this is often a security group or a firewall rule blocking the connection. In the case where you connect to a managed database (RDS, Cloud SQL, etc.), it would be advisable to confirm that the instance allows connections from sqlpipe's IP.

**After** (classified as procedural, conditions first, one action per step):

> **Délais de connexion.** sqlpipe s'arrête avec `dial tcp: i/o timeout` quand il ne peut pas joindre le port Postgres, 5432 par défaut.
>
> 1. Vérifier que l'hôte qui exécute sqlpipe peut joindre le port Postgres. Un pare-feu ou un groupe de sécurité bloque souvent la connexion.
> 2. Si la base est managée, vérifier que l'instance accepte les connexions depuis l'adresse IP de sqlpipe.
> 3. Si le réseau est lent, augmenter `source.connect_timeout_seconds` dans la configuration.
>
> Le délai par défaut est de trente secondes.

Seven more hand-written pairs live in [`examples/before-after.md`](examples/before-after.md).

## What the skill refuses

Marketing copy, brand voice, and blog articles stay out of scope. The skill produces flat, repetitive prose on purpose. The tired reader is the real reader.

## Installation

Claude Code plugin, from this repository as a marketplace:

```
/plugin marketplace add <owner>/FrancaisSimple
/plugin install francais-simple@francais-simple
```

Codex plugin and ChatGPT plugin, from a repo marketplace:

```
cp -r FrancaisSimple ~/.codex/plugins/francais-simple
```

The manifest at `.codex-plugin/plugin.json` follows the Codex compatibility layout documented in the official OpenAI documentation. The manifest at `.claude-plugin/plugin.json` follows the Claude Code plugin manifest reference. Validate both with your harness before publishing.

Plain Agent Skills folder, with no plugin system:

```
cp -r skills/francais-simple ~/.claude/skills/
```

Harnesses without Agent Skills, such as `AGENTS.md`, `.cursorrules`, or custom instructions, use [`prompts/system-prompt.md`](prompts/system-prompt.md). That file ends with a compact version that fits in a system prompt.

Output style for a whole session: [`output-styles/francais-simple.md`](output-styles/francais-simple.md).

## Rules

| Section | Title | Rules |
| --- | --- | --- |
| FR-1 | Words | 10 |
| FR-2 | Noun groups | 6 |
| FR-3 | Verbs | 8 |
| FR-4 | Sentences | 10 |
| FR-5 | Procedural writing | 8 |
| FR-6 | Descriptive writing | 8 |
| FR-7 | Safety notices | 5 |
| FR-8 | Typography, numbers, word count | 10 |
| FR-9 | Writing practice | 8 |

That is 73 rules in 9 sections, numbered `FR-1.1` to `FR-9.8`. The project uses its own numbering, for three reasons: no French rule such as "no conditional" has a slot in an English catalogue, copying the official sequence would approach a derivative work, and the section order stays readable for people who know controlled-language catalogues.

The linter defines 35 violation classes, each mapped to a rule. `evals/check_rules.py` fails when a cited number is undefined, when a defined rule is never cited, or when a class has no rule.

## Linter

Standard library only, no installation:

```
python3 evals/fr_lint.py document.md
python3 evals/fr_lint.py document.md --json
python3 evals/fr_lint.py --self-test
```

Every finding carries a class, a rule number, a line, a confidence level (`certain` or `faible`), and a rewrite suggestion when the rewrite is mechanical. The self-test asserts that the clean fixture scores exactly zero and that every trap case is caught.

## Benchmark

Three measurements: linter violations per 100 words on eight writing tasks, visible defects on eight technical questions, and blind pairwise judging in both orders.

Honest status: the grid has not been run for this release. `evals/run_bench.py` and the full task grid are shipped, and `evals/results/raw/` is empty. No effect size is published, because one generation per cell measures a draw, not an effect. [`evals/results/RESULTS.md`](evals/results/RESULTS.md) states the same thing, and `evals/check_numbers.py` fails the build when a published number cannot be recomputed from raw files.

Sample size, judge-family bias, and the gap between lint score and human readability are documented in the results file as mandatory limitations.

## Provenance

This project is the French port of [`AminBlg/SimpleEnglish`](https://github.com/AminBlg/SimpleEnglish) (MIT). It also builds on [`quantumsheep/simple-french`](https://github.com/quantumsheep/simple-french) (MIT), an earlier French port.

Three layers: ISO 24495-1:2023 for plain-language principles, ASD-STE100 Issue 9 for the structure of the catalogue, and the GIFAS Français Rationalisé for the verbal doctrine, including its documented limits (proprietary, last known version 1999).

The catalogue paraphrases writing rules and claims a lineage. It reproduces no normative text and no dictionary content. Its numbering, section order, and examples are its own.

> Projet non officiel, sans affiliation ni approbation de l'ASD, du STEMG ou du GIFAS. Aucun texte normatif ni contenu de dictionnaire n'est reproduit ici. Les règles sont des reformulations pédagogiques avec des exemples propres au projet. `ASD-STE100` est une marque déposée de l'ASD.

## FAQ

**Is the output certified?**
No. No tool certifies compliance with a controlled-language standard, and this project does not claim that its outputs are compliant.

**Is this affiliated with the ASD, the STEMG, or the GIFAS?**
No. The project is independent. `ASD-STE100` is a trademark of the ASD, the STEMG publishes the standard, and the GIFAS distributed the Français Rationalisé. None of them endorse this work.

**Does the project reproduce normative text?**
No. It reproduces no ASD-STE100 text, no GIFAS text, and no dictionary. The rules are pedagogical rewrites with project-owned examples.

**Why is there no approved word list?**
No French approved-word dictionary exists under a usable licence. The skill applies the principle of controlled vocabulary, the simplest word that says the exact thing, without a closed list.

**Why keep the English word limits of 20 and 25 words?**
French runs about 20 percent longer than English at equal content. Keeping the limits makes the constraint mechanically stricter, and the only way to fit is to remove nominalizations.

**Does the linter write well?**
No. It measures mechanical rules. Word choice, terminology quality, factual accuracy, and real human readability stay outside its reach. A text can score zero and remain bad.

**Is the tool free of dependencies?**
Yes. The skill ships as a folder with no install. The linter, the rule checker, the number checker, and the benchmark runner use the Python standard library only.

## Status

Version 0.1.0. The skill, the five references, the linter, the self-test, the cross-check, the number check, the system prompt, the output style, the plugin manifests, and the examples are complete. The benchmark grid is shipped empty, with the runner and the evaluation grid ready to run.

## License

MIT. See [`LICENSE`](LICENSE). The copyright notices of `AminBlg/SimpleEnglish` and `quantumsheep/simple-french` are kept in the licence file, and the derivative headers live in the files adapted from them.
