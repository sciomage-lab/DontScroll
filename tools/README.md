
# Setting environment variables

This project uses several environment variables. There are several reasons for this. This is to safely use tokens and keys and share them as open source. Also used for Docker builds and github actions.

Basically, important tokens and keys are stored locally as toml files(`.config/dont_scroll/config.toml`).

In order to develop and contribute to this project, you need to load the settings saved in toml as environment variables in the shell.

```bash
. tools/set_env.sh
```

