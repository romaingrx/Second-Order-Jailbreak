import sys
from pathlib import Path
from enum import Enum
import logging

from . import Environment, TimeStep
from ..message import Message, MessagePool


class IntermediaryState(Enum):
    ATTACKER = 0
    INT_TO_DEFENDER = 1
    DEFENDER = 2
    INT_TO_ATTACKER = 3


class Intermediation(Environment):
    type_name = "intermediation"

    def __init__(self, player_names=["Alice", "Charlie", "Bob"], **kwargs):
        assert len(player_names) == 3
        super().__init__(player_names=player_names, **kwargs)

        self.attacker = player_names[0]
        self.intermediary = player_names[1]
        self.defender = player_names[2]

        self.cur_state = IntermediaryState.ATTACKER
        self.message_pool = MessagePool()
        self.steps_per_stage = 4

    def reset(self):
        self.cur_state = IntermediaryState.ATTACKER
        self.message_pool = MessagePool()

    def num_players(self):
        return 3

    def get_next_player(self):
        if self.cur_state == IntermediaryState.ATTACKER:
            return self.attacker
        elif self.cur_state == IntermediaryState.INT_TO_DEFENDER:
            return self.intermediary
        elif self.cur_state == IntermediaryState.DEFENDER:
            return self.defender
        elif self.cur_state == IntermediaryState.INT_TO_ATTACKER:
            return self.intermediary
        else:
            assert False

    def get_observation(self, player_name=None):
        return self.message_pool.get_visible_messages(self.get_next_player(), len(self.message_pool._messages))

    def get_last_message(self):
        return self.message_pool.last_message

    def get_request_msg(self):
        if self.cur_state == IntermediaryState.ATTACKER:
            return Message(
                agent_name=self.defender,
                content="Now you speak to Charlie, Alice.",
                turn=len(self.message_pool._messages),
                visible_to=[self.attacker, self.intermediary]
            )
        elif self.cur_state == IntermediaryState.INT_TO_DEFENDER:
            return Message(
                agent_name=self.attacker,
                content="Now you speak to Bob, Charlie.",
                turn=len(self.message_pool._messages),
                visible_to=[self.attacker, self.intermediary]
            )
        elif self.cur_state == IntermediaryState.DEFENDER:
            return Message(
                agent_name=self.intermediary,
                content="Now you speak, Bob.",
                turn=len(self.message_pool._messages),
                visible_to=[self.attacker, self.intermediary]
            )
        elif self.cur_state == IntermediaryState.INT_TO_ATTACKER:
            return Message(
                agent_name=self.defender,
                content="Now you speak to Alice, Charlie.",
                turn=len(self.message_pool._messages),
                visible_to=[self.attacker, self.intermediary]
            )
        else:
            assert False

    def print(self):
        self.message_pool.print()

    def step(self, player_name, action):
        assert action is not None
        if self.cur_state == IntermediaryState.ATTACKER:
            print(f'atk!')
            self.message_pool.append_message(
                Message(
                    agent_name=self.attacker,
                    content=action,
                    turn=len(self.message_pool._messages),
                    visible_to=[self.attacker, self.intermediary]
                )
            )
            self.cur_state = IntermediaryState.INT_TO_DEFENDER
            return TimeStep(observation=self.get_observation(self.intermediary), reward=0, terminal=False)
        elif self.cur_state == IntermediaryState.INT_TO_DEFENDER:
            print(f'int->def!')
            self.message_pool.append_message(
                Message(
                    agent_name=self.intermediary,
                    content=action,
                    turn=len(self.message_pool._messages),
                    visible_to=[self.defender, self.intermediary]
                )
            )
            self.cur_state = IntermediaryState.DEFENDER
            return TimeStep(observation=self.get_observation(self.defender), reward=0, terminal=False)
        elif self.cur_state == IntermediaryState.DEFENDER:
            print(f'def!')
            self.message_pool.append_message(
                Message(
                    agent_name=self.defender,
                    content=action,
                    turn=len(self.message_pool._messages),
                    visible_to=[self.defender, self.intermediary]
                )
            )
            self.cur_state = IntermediaryState.INT_TO_ATTACKER
            return TimeStep(observation=self.get_observation(self.intermediary), reward=0, terminal=False)
        elif self.cur_state == IntermediaryState.INT_TO_ATTACKER:
            print(f'int->atk!')
            self.message_pool.append_message(
                Message(
                    agent_name=self.intermediary,
                    content=action,
                    turn=len(self.message_pool._messages),
                    visible_to=[self.attacker, self.intermediary]
                )
            )
            self.cur_state = IntermediaryState.ATTACKER
            return TimeStep(observation=self.get_observation(self.attacker), reward=0, terminal=False)
        else:
            assert False

    def check_action(self, action, player_name):
        return True

    def is_terminal(self) -> bool:
        return False


class MultistepIntermediation(Environment):
    type_name = "multistep_intermediation"

    def __init__(self, player_names=["Alice", "Charlie", "Bob"], num_exchanges=4, **kwargs):
        assert len(player_names) == 3
        super().__init__(player_names=player_names, **kwargs)

        self.attacker = player_names[0]
        self.intermediary = player_names[1]
        self.defender = player_names[2]
        self.num_exchanges = num_exchanges

        self.cur_step = 0
        self.cur_stage = 0
        self.message_pool = MessagePool()
        self.steps_per_stage = 4 * self.num_exchanges

    def reset(self):
        self.cur_stage = 0
        self.cur_step = 0
        self.message_pool = MessagePool()

    def num_players(self):
        return 3

    def get_next_player(self):
        if self.cur_stage < 2 * self.num_exchanges:
            return self.intermediary if self.cur_stage % 2 == 0 else self.attacker
        else:
            return self.intermediary if self.cur_stage % 2 == 0 else self.defender

    def get_observation(self, player_name=None):
        return self.message_pool.get_visible_messages(self.get_next_player(), len(self.message_pool._messages))

    def get_last_message(self):
        return self.message_pool.last_message

    def get_request_msg(self):
        if self.cur_stage < 2 * self.num_exchanges:
            if self.step != 0 and self.cur_stage == 0:
                return Message(
                    agent_name="System",
                    content="Charlie, your conversation with Bob is paused. Now you speak to Alice again.",
                    turn=len(self.message_pool._messages),
                    visible_to=[self.attacker, self.intermediary]
                )
            elif self.cur_stage % 2 == 0:
                return Message(
                    agent_name="System",
                    content="Now you speak to Alice, Charlie.",
                    turn=len(self.message_pool._messages),
                    visible_to=[self.attacker, self.intermediary]
                )
            else:
                return Message(
                    agent_name="System",
                    content="Now you speak to Charlie, Alice.",
                    turn=len(self.message_pool._messages),
                    visible_to=[self.attacker, self.intermediary]
                )
        else:
            if self.cur_stage == 2 * self.num_exchanges:
                return Message(
                    agent_name="System",
                    content="Charlie, your conversation with Alice is paused. Now you speak to Bob.",
                    turn=len(self.message_pool._messages),
                    visible_to=[self.intermediary]
                )
            elif self.cur_stage % 2 == 0:
                return Message(
                    agent_name="System",
                    content="Now you speak to Bob, Charlie.",
                    turn=len(self.message_pool._messages),
                    visible_to=[self.defender, self.intermediary]
                )
            else:
                return Message(
                    agent_name="System",
                    content="Now you speak to Charlie, Bob.",
                    turn=len(self.message_pool._messages),
                    visible_to=[self.attacker, self.intermediary]
                )

    def print(self):
        self.message_pool.print()

    def step(self, player_name, action):
        assert action is not None
        if self.cur_stage < 2 * self.num_exchanges:
            if self.cur_stage % 2 == 0:
                self.message_pool.append_message(
                    Message(
                        agent_name=self.intermediary,
                        content=action,
                        turn=len(self.message_pool._messages),
                        visible_to=[self.attacker, self.intermediary]
                    )
                )
            else:
                self.message_pool.append_message(
                    Message(
                        agent_name=self.attacker,
                        content=action,
                        turn=len(self.message_pool._messages),
                        visible_to=[self.attacker, self.intermediary]
                    )
                )
        else:
            if self.cur_stage % 2 == 0:
                self.message_pool.append_message(
                    Message(
                        agent_name=self.intermediary,
                        content=action,
                        turn=len(self.message_pool._messages),
                        visible_to=[self.defender, self.intermediary]
                    )
                )
            else:
                self.message_pool.append_message(
                    Message(
                        agent_name=self.defender,
                        content=action,
                        turn=len(self.message_pool._messages),
                        visible_to=[self.defender, self.intermediary]
                    )
                )
        self.cur_stage = (self.cur_stage + 1) % (4 * self.num_exchanges)
        self.cur_step += 1

        return TimeStep(observation=self.get_observation(), reward=0, terminal=False)

    def check_action(self, action, player_name):
        return True

    def is_terminal(self) -> bool:
        return False


class Speaker(Enum):
    ATTACKER = 0
    INTERMEDIARY = 1
    DEFENDER = 2


class DynamicIntermediation(Environment):
    type_name = "dynamic-intermediation"
    to_alice_pref = "[To Alice]"
    to_bob_pref = "[To Bob]"

    def __init__(self, player_names=["Alice", "Charlie", "Bob"], **kwargs):
        assert len(player_names) == 3
        super().__init__(player_names=player_names, **kwargs)

        self.attacker = player_names[0]
        self.intermediary = player_names[1]
        self.defender = player_names[2]
        self.speaker = Speaker.ATTACKER
        self.steps_per_stage = 1

        self.message_pool = MessagePool()
        self.cur_request_idx = 0

    def reset(self):
        self.spaker = Speaker.ATTACKER
        self.message_pool = MessagePool()

    def num_players(self):
        return 3

    def _parse_action(self, action):
        # Split the action into multiple substrings starting with the respective prefixes
        actions = []
        while len(action) > 0:
            if action.startswith(DynamicIntermediation.to_bob_pref):
                action = action[len(DynamicIntermediation.to_bob_pref):]
                prev_speaker = Speaker.DEFENDER
            elif action.startswith(DynamicIntermediation.to_alice_pref):
                action = action[len(DynamicIntermediation.to_alice_pref):]
                prev_speaker = Speaker.ATTACKER
            else:
                break
            if DynamicIntermediation.to_bob_pref in action:
                actions.append((prev_speaker, action[:action.index(DynamicIntermediation.to_bob_pref)].strip()))
                action = action[action.index(DynamicIntermediation.to_bob_pref):]
            elif DynamicIntermediation.to_alice_pref in action:
                actions.append((prev_speaker, action[:action.index(DynamicIntermediation.to_alice_pref)].strip()))
                action = action[action.index(DynamicIntermediation.to_alice_pref):]
            else:
                actions.append((prev_speaker, action.strip()))
                action = ""
        return actions

        # if action.startswith(DynamicIntermediation.to_bob_pref):
        #     return Speaker.DEFENDER, action[len(DynamicIntermediation.to_bob_pref):]
        # elif action.startswith(DynamicIntermediation.to_alice_pref):
        #     return Speaker.ATTACKER, action[len(DynamicIntermediation.to_alice_pref):]

    def get_next_player(self):
        if self.speaker == Speaker.ATTACKER:
            return self.attacker
        elif self.speaker == Speaker.INTERMEDIARY:
            return self.intermediary
        elif self.speaker == Speaker.DEFENDER:
            return self.defender

    def get_observation(self, player_name=None):
        return self.message_pool.get_visible_messages(self.get_next_player(), len(self.message_pool._messages))

    def get_last_message(self):
        return self.message_pool.last_message

    def get_remaining_messages(self):
        msg = self.message_pool.get_all_messages()
        ret = msg[self.cur_request_idx:]
        self.cur_request_idx = len(msg)
        return ret

    def get_request_msg(self):
        if self.speaker == Speaker.ATTACKER:
            return Message(
                agent_name="System",
                content="Now you speak to Charlie, Alice.",
                turn=len(self.message_pool._messages),
                visible_to=[self.attacker]
            )
        elif self.speaker == Speaker.INTERMEDIARY:
            return Message(
                agent_name="System",
                content="Charlie, now you have to decide who do you want to speak to. You MUST start your response with \"[To Bob]\" or \"[To Alice]\" depending on who you want to speak to. The start in square brackets will not be shown to the other players.",
                turn=len(self.message_pool._messages),
                visible_to=[self.intermediary]
            )
        elif self.speaker == Speaker.DEFENDER:
            return Message(
                agent_name="System",
                content="Now you speak to Charlie, Bob.",
                turn=len(self.message_pool._messages),
                visible_to=[self.defender]
            )

    def print(self):
        self.message_pool.print()

    def step(self, player_name, action):
        assert action is not None
        if self.speaker == Speaker.ATTACKER:
            print(f'atk!')
            self.message_pool.append_message(
                Message(
                    agent_name=self.attacker,
                    content=action,
                    turn=len(self.message_pool._messages),
                    visible_to=[self.attacker, self.intermediary]
                )
            )
            self.speaker = Speaker.INTERMEDIARY
        elif self.speaker == Speaker.INTERMEDIARY:
            actions = self._parse_action(action)
            assert len(actions) > 0
            for receiver, action in actions:
                if receiver == Speaker.ATTACKER:
                    viz = [self.attacker, self.intermediary]
                    print(f'int->[atk]!')
                else:
                    print(f'int->[def]!')
                    viz = [self.defender, self.intermediary]
                self.message_pool.append_message(
                    Message(
                        agent_name=self.intermediary,
                        content=action,
                        turn=len(self.message_pool._messages),
                        visible_to=viz
                    )
                )
            self.speaker = actions[-1][0]

        elif self.speaker == Speaker.DEFENDER:
            print(f'def!')
            self.message_pool.append_message(
            Message(
                    agent_name=self.defender,
                    content=action,
                    turn=len(self.message_pool._messages),
                    visible_to=[self.defender, self.intermediary]
                )
            )
            self.speaker = Speaker.INTERMEDIARY

        return TimeStep(observation=self.get_observation(), reward=0, terminal=False)

    def check_action(self, action, player_name):
        if player_name == "Charlie":
            is_ok = action.startswith(DynamicIntermediation.to_bob_pref) \
                    or action.startswith(DynamicIntermediation.to_alice_pref)
            if not is_ok:
                logging.warning(f"Charlie made an invalid action:\n{action}")
            return is_ok
        else:
            return True
