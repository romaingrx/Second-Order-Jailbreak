import re
from typing import List
from tenacity import retry, stop_after_attempt, wait_random_exponential

from .base import IntelligenceBackend
from ..message import Message, SYSTEM_NAME as SYSTEM

# Try to import the transformers package
try:
    from transformers import pipeline
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from auto_gptq.utils.exllama_utils import exllama_set_max_input_length
except ImportError:
    is_transformers_available = False
else:
    is_transformers_available = True


class PromptTemplate:
    def __init__(self, system_prompt=None):
        self.system_prompt = system_prompt
        self.user_messages = []
        self.model_replies = []
        self.model_starts = False

    def add_user_message(self, message: str, return_prompt=True):
        self.user_messages.append(message)
        if return_prompt:
            return self.build_prompt()

    def add_model_reply(self, reply: str, includes_history=False, return_reply=True):
        reply_ = reply.replace(self.build_prompt(), "") if includes_history else reply
        self.model_replies.append(reply_)
        if len(self.user_messages) != len(self.model_replies):
            print(self.user_messages, self.model_replies)
            raise ValueError(
                "Number of user messages does not equal number of system replies."
            )
        if return_reply:
            return reply_

    def get_user_messages(self, strip=True):
        return [x.strip() for x in self.user_messages] if strip else self.user_messages

    def get_model_replies(self, strip=True):
        return [x.strip() for x in self.model_replies] if strip else self.model_replies

    def build_prompt(self):
        if len(self.user_messages) != len(self.model_replies) + 1:
            raise ValueError(
                "Error: Expected len(user_messages) = len(model_replies) + 1. Add a new user message!"
            )

        if self.system_prompt is not None:
            SYS = f"[INST] <<SYS>>\n{self.system_prompt}\n<</SYS>>"
        else:
            SYS = ""

        CONVO = ""
        SYS = "<s>" + SYS
        for i in range(len(self.user_messages) - 1):
            user_message, model_reply = self.user_messages[i], self.model_replies[i]
            conversation_ = f"{user_message} [/INST] {model_reply} </s>"
            if i != 0:
                conversation_ = "[INST] " + conversation_
            CONVO += conversation_

        CONVO += f"[INST] {self.user_messages[-1]} [/INST]"

        return SYS + CONVO

    def build_prompt(self):
        if self.system_prompt is not None:
            SYS = f"[INST] <<SYS>>\n{self.system_prompt}\n<</SYS>>"
        else:
            SYS = ""
        SYS = "<s>" + SYS

        if len(self.user_messages) == 0 and len(self.model_replies) == 0:
            return SYS

        if len(self.user_messages) != len(self.model_replies) + 1:
            raise ValueError(
                "Error: Expected len(user_messages) = len(model_replies) + 1. Add a new user message!"
            )

        CONVO = ""
        for i in range(len(self.user_messages) - 1):
            user_message, model_reply = self.user_messages[i], self.model_replies[i]
            conversation_ = f"{user_message} [/INST] {model_reply} </s>"
            if i != 0:
                conversation_ = "[INST] " + conversation_
            CONVO += conversation_

        if not self.model_starts:
            CONVO += f"[INST] {self.user_messages[-1]} [/INST]"

        return SYS + CONVO


END_OF_MESSAGE = "<EOS>"  # End of message token specified by us not Llama
STOP = ("<|endoftext|>", END_OF_MESSAGE)  # End of sentence token
BASE_PROMPT = f"The messages always end with the token {END_OF_MESSAGE}."
BASE_PROMPT += "The last message from the user will contain a reminder in square brackets like this : {}"


class TransformersLlamaConversational(IntelligenceBackend):
    """
    Interface to the Transformers ConversationalPipeline
    """

    stateful = False
    type_name = "transformers:llama:conversational"

    def __init__(
        self,
        model: str,
        device: int = "cuda",
        merge_other_agents_as_one_user: bool = True,
        prompt_prefix: str = "",
        exllama_max_input_length: int = 8192,
        **kwargs,
    ):
        super().__init__(
            model=model,
            device=device,
            merge_other_agents_as_one_user=merge_other_agents_as_one_user,
            prompt_prefix=prompt_prefix,
            exllama_set_max_input_length=exllama_max_input_length,
            **kwargs,
        )
        self.model = model
        self.device = device
        self.merge_other_agent_as_user = merge_other_agents_as_one_user
        self.prompt_prefix = prompt_prefix
        print(f"Loading model {model} on device {device}... with kwargs {kwargs}")

        assert is_transformers_available, "Transformers package is not installed"
        model = AutoModelForCausalLM.from_pretrained(
            self.model,
            device_map=self.device,
            trust_remote_code=False,
            revision="main",
        )
        model = exllama_set_max_input_length(model, exllama_max_input_length)
        tokenizer = AutoTokenizer.from_pretrained(
            self.model, device_map=self.device, use_fast=True
        )
        self.chatbot = pipeline(
            task="text-generation", model=model, tokenizer=tokenizer
        )

    def _conversation_to_llama_prompt(self, conversation):
        system_prompt = conversation["system_prompt"]
        messages = conversation["history"]
        prompt = PromptTemplate(system_prompt=system_prompt)
        for message in messages[1:]:
            role = message["role"]
            content = message["content"]
            if role == "assistant":
                prompt.add_model_reply(content)
            elif role == "user":
                prompt.add_user_message(content)
            else:
                raise ValueError(f"Unknown role: {role}")
        return prompt.build_prompt()

    @retry(stop=stop_after_attempt(6), wait=wait_random_exponential(min=1, max=60))
    def _get_response(self, conversation):
        input_prompt = self._conversation_to_llama_prompt(conversation)
        print(f"INPUT PROMPT: \n{input_prompt}")
        response = self.chatbot(
            input_prompt,
            max_length=self._config_dict.get("max_tokens", 256)
            + len(
                input_prompt
            ),  # max_tokens is the number of tokens to generate excluding the input prompt
            temperature=self._config_dict.get("temperature", 0.9),
            top_p=self._config_dict.get("top_p", 0.9),
            top_k=self._config_dict.get("top_k", 50),
        )
        return response[0]["generated_text"][len(input_prompt) :].strip()

    @staticmethod
    def _msg_template(agent_name, content):
        return f"[{agent_name}]: {content}"

    def query(
        self,
        agent_name: str,
        role_desc: str,
        history_messages: List[Message],
        global_prompt: str = None,
        request_msg: Message = None,
        *args,
        **kwargs,
    ) -> str:
        # Merge the role description and the global prompt as the system prompt for the agent
        request_msg = request_msg or Message("", f"Now you speak, {agent_name}", -1)
        base_prompt = BASE_PROMPT.format(f"[{request_msg.content}]")
        if global_prompt:  # Prepend the global prompt if it exists
            system_prompt = f"{self.prompt_prefix}{global_prompt.strip()}\n{base_prompt}\n\nYour name is {agent_name}.\n\nYour role:{role_desc}"
        else:
            system_prompt = f"{self.prompt_prefix}Your name is {agent_name}.\n\nYour role:{role_desc}\n\n{base_prompt}"

        messages = [(SYSTEM, system_prompt)]

        for idx, msg in enumerate(history_messages):
            if msg.agent_name == agent_name:
                if idx == 0:
                    messages.append({"role": "user", "content": ""})
                messages.append(
                    {"role": "assistant", "content": msg.content + END_OF_MESSAGE}
                )
            else:
                messages.append(
                    {
                        "role": "user",
                        "content": f"[{msg.agent_name}]: {msg.content+END_OF_MESSAGE}",
                    }
                )

        messages[-1]["content"] = (
            messages[-1]["content"].replace(END_OF_MESSAGE, "")
            + f"\n[{request_msg.content}]{END_OF_MESSAGE}"
        )

        conversation = {
            "system_prompt": system_prompt,
            "history": messages,
        }

        # Get the response
        response = self._get_response(conversation)

        # Remove the agent name if the response starts with it
        response = re.sub(rf"^\s*\[.*]:", "", response).strip()
        response = re.sub(rf"^\s*{re.escape(agent_name)}\s*:", "", response).strip()

        # Remove the tailing end of message token
        response = re.sub(rf"{END_OF_MESSAGE}$", "", response).strip()
        return response
