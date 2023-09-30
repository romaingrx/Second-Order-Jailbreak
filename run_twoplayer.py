import re
import sys
import argparse
import json
from pathlib import Path
import gradio as gr
from glob import glob
import tqdm
from datetime import datetime

sys.path.append(str(Path(__file__).parent / "chatarena"))
print(sys.path[-1])
from chatarena.arena import Arena, TooManyInvalidActions
from chatarena.backends import BACKEND_REGISTRY
from chatarena.backends.human import HumanBackendError
from chatarena.config import ArenaConfig
from chatarena.environments import ENV_REGISTRY
from chatarena.database import log_arena, log_messages, SupabaseDB, supabase_available
from chatarena.message import Message


parser = argparse.ArgumentParser()
parser.add_argument("config", type=Path)
parser.add_argument("--num_steps", type=int, default=20)
args = parser.parse_args()

out_dir = Path(f"output/{datetime.now().strftime('%Y%m%d_%H%M%S')}")
Path("output").mkdir(exist_ok=True)
out_dir.mkdir(exist_ok=True)

conf = json.load(args.config.open())
arena_conf = ArenaConfig(**conf)
# print(conf)
arena = Arena.from_config(arena_conf)

for _ in tqdm.trange(args.num_steps, desc="Conversation"):
    arena.step()

arena.save_history(str(out_dir / "history.json"))


