"""O24 replay worker: runs in a separate Python process."""
from __future__ import annotations
import json, sys, platform
from .replay_harness import replay_compilation

def main() -> int:
    payload=json.load(sys.stdin)
    receipt=replay_compilation(payload["seed"],payload["prior_node"])
    out={"worker_version":"O24.1","environment":{"python":platform.python_version(),"implementation":platform.python_implementation(),"platform":platform.platform()},"replay":receipt}
    json.dump(out,sys.stdout,sort_keys=True,separators=(",",":")); return 0

if __name__ == "__main__":
    raise SystemExit(main())
