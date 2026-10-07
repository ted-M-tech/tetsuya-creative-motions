# Make a film with this workflow

**English** · [日本語](VIDEO-WORKFLOW.ja.md)

This repository shares both finished films and the workflow behind them. The reusable agent skill is [tetsuya-creative-motions](../skills/tetsuya-creative-motions/SKILL.md). It guides the brief, revisions, evidence, and production records. It is not a one-click video generator or a bundle of third-party tools.

## Three layers

| Layer | Responsibility | Where it lives |
|---|---|---|
| Production tools | Rendering, animation, media sourcing, audio mixing | Your installed engine/tool skills |
| This workflow | Story continuity, feedback scope, clear claims, reusable records | `skills/tetsuya-creative-motions/` |
| Each film | Brand, script, voice choices, research, assets, source | `films/<project>/` and `styles/` |

The Lanclo example uses HyperFrames with its product-film, animation, audio, and media skills. Those dependencies are not redistributed here. Install the framework through its supported setup instructions before rendering. Existing composition versions are pinned in their package files. Voice services need your own API access and may incur costs. Planning and documentation can be done without those services.

## Install the skill

Clone the repository, then copy the **whole skill folder** into the user-skill directory recognized by your agent. Check the destination first; do not overwrite a custom skill with the same name.

For an environment that discovers skills under `~/.agents/skills/`:

```sh
git clone https://github.com/ted-M-tech/tetsuya-creative-motions.git
cd tetsuya-creative-motions
mkdir -p ~/.agents/skills
# Run only if this destination does not already exist:
cp -R skills/tetsuya-creative-motions ~/.agents/skills/
```

For Codex installations using `CODEX_HOME/skills` or `~/.codex/skills`, use that destination instead. Reload skill discovery or start a new session as required by your agent. You can also give the agent the repository's `SKILL.md` path directly; merely storing it in Git does not automatically install it for everyone.

If you maintain this repository locally, a symlink avoids a second copy:

```sh
# From the repository root; destination must be absent.
ln -s "$PWD/skills/tetsuya-creative-motions" ~/.agents/skills/tetsuya-creative-motions
```

The instruction files are portable Markdown. Tool execution still depends on your agent and installed renderer. This package has been structurally validated; it has not been tested across every agent or provider.

## Try it

**Plan a new film:**

> Use $tetsuya-creative-motions. Plan a 45-second film for my appointment-booking app, aimed at independent salons. Show how it reduces scheduling work. Propose the story and narration first; do not generate media or render yet.

**Revise an existing film:**

> Use $tetsuya-creative-motions. In the active project, make the transition from analysis to the next lesson clearer. Keep the accepted opening, research claim, voice, and closing. Tell me what changes, then implement the agreed edit.

**Save and teach the process:**

> Use $tetsuya-creative-motions. Package this accepted film with its script, consolidated prompt, actual voice inputs, timeline, credits, and editable source. Put an alternate narration under extras. Prepare the portfolio entry locally; do not publish yet.

Adapt these prompts to your own authorized scope. Invoking the skill does not itself authorize purchases, generation charges, or publication.

## Learn from Lanclo

1. [Watch the film and making of](https://videos.maepace.com/en/films/lanclo-daily/).
2. Read the [project overview](../films/lanclo/README.md) and [final prompt](../films/lanclo/PROMPT.md).
3. Compare the [early version](../films/lanclo/history/r18/) with the final source.
4. Read [creative decisions](../skills/tetsuya-creative-motions/references/creative-decisions.md): accurate chart claims, user-action sequences, and transitions.
5. Use your own brand, permitted assets, voice, and facts. Do not inherit Lanclo's research claims for another product.

## Keep it useful

Maintain the skill here in Git. Record a reason when changing it; promote repeated, transferable lessons rather than every comment from one film. Keep upstream skills separate, and record production versions per project. The [recordkeeping contract](../skills/tetsuya-creative-motions/references/project-records.md) explains what to preserve.

The skill and original documentation use this repository's [MIT license](../LICENSE). Third-party skills, assets, brands, and voices retain their own conditions.
