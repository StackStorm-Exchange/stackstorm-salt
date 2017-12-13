# Change Log

## 0.7.2

- Do not send `args=None` for client actions. This was breaking on modules like `test.ping`.

## 0.7.0

- Set `args=None` for `test.ping` and `test.version`
- This is so action works with ChatOps and newer ST2 versions that will
  provide default value even for non-required parameters.

## 0.6.0

- Updated action `runner_type` from `run-python` to `python-script`

## 0.5.1

- Hide only valid (non-empty) payload values sent to salt CLI

## 0.5.0

- Rename `config.yaml` to `config.schema.yaml` and update to use schema.
