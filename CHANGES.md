# Change Log

## 2.0.0

* Drop Python 2.7 support

## 1.0.1

* Add logging of HTTP Code response from Salt API

## 1.0.0

* Drop Python 2.7 support

## 0.8.4

- Pin salt < 3001 and jinja2 < 2.11.1 to support both Python 2 and 3

## 0.8.3

- Add explicit support for Python 2 and 3

## 0.8.2

- Fixed `sanitize_payload` function to avoid leaking the type and length of sensitive values #15

## 0.8.1

- Fixed a bug in Salt runs due to typo in processing logic for additional parameters #14 (@pengyao)

## 0.8.0

- Changed expr_form to tgt_type as SaltStack upstream has replaced the functionality.

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
