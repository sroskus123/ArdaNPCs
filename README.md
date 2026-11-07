# ArdaNPCs Wiki

Practical documentation for **ArdaNPCs 1.1.0**, Minecraft 1.21.8 / Fabric.

- [Česká příručka](https://sroskus123.github.io/ArdaNPCs/cs/index.html)
- [English guide](https://sroskus123.github.io/ArdaNPCs/en/index.html)
- [Download ArdaNPCs on CurseForge](https://www.curseforge.com/minecraft/mc-mods/ardanpcs)

This repository contains the documentation website. Topics cover installation, NPC controls, appearances and modded models, dialogues and quests, JavaScript events and examples, scripted items and blocks, services, mail, companions, and troubleshooting.

## Editing and building

Edit the bilingual chapter files in `content/`. Each JSON file has a `slug` and `cs` / `en` objects with `title`, `description`, and an HTML `body`. Use an ASCII `id` on each second-level heading. Relative chapter links use `slug.html`.

Run with Python 3 (standard library only):

```sh
python build.py
python validate.py
python -m http.server 8765
```

Open `http://localhost:8765/`. Commit the generated `cs/`, `en/`, root redirects, and assets together with source changes. The existing GitHub Pages workflow publishes the static files on pushes to `main`.

Search runs locally in the visitor's browser. No analytics, accounts or external JavaScript dependencies are required. Both languages have direct page URLs; core documentation remains readable without JavaScript.

The previous standalone Czech quest manual URL redirects to the updated quest chapter. Older versions remain available in Git history. Documentation was checked against the 1.1.0 source and released artifact; this does not imply every modpack or custom entity renderer has been tested in-game.
