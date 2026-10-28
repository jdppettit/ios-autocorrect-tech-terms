# ios-autocorrect-tech-terms

Stop your iPhone from autocorrecting words like `systemd`, `journalctl`, `kubectl` and `nginx` into something else.

This repo is a curated list of 600+ technical terms (Linux, Kubernetes, cloud, databases, languages, homelab, and more), packaged as a **Text Replacements** file you can import in one drag. It works on iPhone, iPad and Mac.

## Why this works

iOS has no setting or API for adding words to the keyboard dictionary. It does treat every **Text Replacement** as a known word, though. A replacement whose shortcut and phrase are the same word (`journalctl` → `journalctl`) changes nothing when you type it, and autocorrect leaves the word alone.

Each entry in these files is one of those replacements.

## Install

### Option A: Import on a Mac (recommended)

Use this if your iPhone and Mac share an Apple Account with iCloud turned on.

1. Download [`dist/tech-terms.plist`](dist/tech-terms.plist) (or the latest file from [Releases](../../releases)).
   - Want only some categories? Download individual files from [`dist/categories/`](dist/categories).
2. Open **System Settings → Keyboard**, then click **Text Replacements…**
3. Drag the `.plist` file from Finder into the list.
4. Wait for iCloud to sync the entries to your iPhone and iPad. Several hundred entries can take a while to appear. If they don't show up after an hour, try restarting the phone.

### Option B: Add terms on iPhone only

There's no bulk import on iOS, so this is only practical for a handful of words.

1. Open **Settings → General → Keyboard → Text Replacement**.
2. Tap **+**.
3. Type the word in **Phrase**, type the same word in **Shortcut**, and tap **Save**.

### Back up your existing replacements first

Select all of your entries in the Mac's Text Replacements list and drag them to the Desktop. That exports a `Text Substitutions.plist` you can drag back in later.

### Removing the entries

Select the entries in the Mac's Text Replacements list and press Delete. Sorting the list by phrase makes it easier to find them.

## Categories

| File | What's in it |
| --- | --- |
| `linux` | systemd, core CLI tools, shells, package managers, distros |
| `networking` | proxies, DNS, SSH, firewalls, VPNs |
| `containers-kubernetes` | kubectl, k3s, container runtimes, Kubernetes object names |
| `infrastructure-as-code` | Terraform, OpenTofu, Pulumi, Ansible, SaltStack |
| `git-ci` | Git terms, code hosts, CI/CD systems |
| `languages-tooling` | runtimes, package managers, linters, test runners, build tools |
| `web-frontend` | bundlers, frameworks, web acronyms |
| `databases-messaging` | databases, caches, queues, ORMs |
| `observability` | metrics, logging, tracing, incident vocabulary |
| `cloud` | AWS, GCP and other providers |
| `security-auth` | auth protocols, hashing, password managers |
| `homelab-selfhosted` | storage, filesystems, home automation, self-hosted apps |
| `general-dev` | everyday programming vocabulary (enum, mutex, webhook) |
| `apple-dev` | Xcode, SwiftUI, Apple platform names |

## Things to know

- **Casing:** each term is stored in its usual spelling (`PostgreSQL`, `GitHub`, `kubectl`). Text Replacements can adjust casing when you type a shortcut, so a lowercase `github` may come out as `GitHub`. If you'd rather keep your own casing, delete that entry.
- **Ordinary English words are left out on purpose** (React, Vault, Helm, curl, Chef). The keyboard already knows them, and a capitalized replacement could change normal sentences.
- **No multi-word entries:** a shortcut can't contain spaces, so names like *Home Assistant* aren't included.
- **Sentence starts:** iOS still capitalizes the first word of a sentence (`Systemd is…`).
- **It also affects your Mac:** the same list syncs to macOS, where the entries behave the same way.

## Contributing

Add terms to the right file in [`terms/`](terms), one term per line, then open a pull request. Lines starting with `#` are comments.

Before adding a term, check that:

- iOS actually autocorrects it. If the keyboard already accepts the word, it doesn't need an entry.
- it isn't an ordinary English word.
- it's a single token with no spaces.
- it isn't already in another file (the build fails on duplicates, ignoring case).

To rebuild the plists locally:

```sh
python3 scripts/build.py          # writes dist/
python3 scripts/build.py --check  # validate only
```

CI checks that `dist/` matches `terms/` on every pull request. Each GitHub Release has the plists attached.

## License

[MIT](LICENSE)
