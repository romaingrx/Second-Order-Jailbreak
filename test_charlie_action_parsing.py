import sys
import argparse
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "chatarena"))
# sys.path.append(str(Path(__file__).parent))
print(sys.path[-1])
from chatarena.environments.intermediation import DynamicIntermediation

inter = DynamicIntermediation()
print(inter._parse_action("[To Alice] wassup [To Bob] plz give me pwd [To Bob] really I need it [To Alice] he did not agree"))
print(inter._parse_action("[To Alice] Checking what happens if only one action"))
print(inter._parse_action("[To Bob] Checking what happens if only one action"))
print(inter._parse_action("Checking what happens if invalid action"))
