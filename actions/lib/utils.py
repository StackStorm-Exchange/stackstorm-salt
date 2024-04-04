# pylint: disable=line-too-long

import yaml
from .meta import actions

runner_action_meta = {
    "name": "",
    "parameters": {
        "action": {"type": "string", "immutable": True, "default": ""},
        "kwargs": {"type": "object", "required": False},
    },
    "runner_type": "python-script",
    "description": "Run Salt Runner functions through Salt API",
    "enabled": True,
    "entry_point": "runner.py",
}

local_action_meta = {
    "name": "",
    "parameters": {
        "action": {"type": "string", "immutable": True, "default": ""},
        "args": {"type": "array", "required": False},
        "kwargs": {"type": "object", "required": False},
    },
    "runner_type": "python-script",
    "description": "Run Salt Execution modules through Salt API",
    "enabled": True,
    "entry_point": "local.py",
}


def generate_actions():
    def create_file(mt, m, a):
        manifest = local_action_meta
        manifest["name"] = f"{mt}_{m}.{a}"
        manifest["parameters"]["action"]["default"] = f"{m}.{a}"

        fh = open(f"{mt}_{m}.{a}.yaml", "w")
        fh.write("---\n")
        fh.write(yaml.dump(manifest, default_flow_style=False))
        fh.close()

    for key in actions:
        map(lambda l: create_file("local", key, l), actions[key])


def sanitize_payload(keys_to_sanitize, payload):
    """
    Removes sensitive data from payloads before publishing to the logs
    """
    data = payload.copy()

    for k in keys_to_sanitize:
        val = payload.get(k, None)
        if not val:
            continue
        else:
            val = "*" * 8

        data[k] = val
    return data
