# Software Docs Validation

Use the normal prompt validation first. For docs-heavy software work, also
check:

- Referenced files and commands exist.
- Docs describe current behavior, not planned behavior, unless clearly labeled.
- Optional workflows remain optional in wording and navigation.
- Local links and index entries are coherent after adding new docs.
- Examples are modest and do not become hidden requirements.

Relevant commands:

```sh
python3 scripts/ahl.py domain-pack check
python3 scripts/ahl.py docs check
python3 scripts/ahl.py doctor
```

The pack checker validates manifest structure and referenced files. It does not
prove that prose claims are correct.
