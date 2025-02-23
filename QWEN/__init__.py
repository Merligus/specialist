from typing import Optional, List, Any, Dict, Iterator
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import PrivateAttr

# used for qwen inference
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class ChatQWEN(BaseChatModel):
    """A custom chat model that invoke Qwen2.5-1.5B-Instruct.

    Example:

        .. code-block:: python

            model = ChatQWEN()
            result = model.invoke([HumanMessage(content="hello")])
            result = model.batch([[HumanMessage(content="hello")],
                                 [HumanMessage(content="world")]])
    """

    model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"
    """The name of the model"""
    # other params
    temperature: float = 0.7
    max_new_tokens: int = 512
    device_map: str = "auto"

    # private attributes
    _model: Any = PrivateAttr()
    _tokenizer: Any = PrivateAttr()
    """The model to call"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # load qwen
        self._tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, trust_remote_code=True
        )

        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map=self.device_map,
            torch_dtype=torch.bfloat16,
            offload_folder=None,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
        ).eval()

        # Adicione isto após carregar o modelo
        print(f"GPU memory used: {torch.cuda.memory_allocated()/1024**3:.2f} GB")
        print(f"GPU memory reserved: {torch.cuda.memory_reserved()/1024**3:.2f} GB")

    def _convert_message_to_dict(self, message: BaseMessage) -> dict:
        """Messages from LangChain to format expected by QWEN"""
        if isinstance(message, HumanMessage):
            return {"role": "user", "content": message.content}
        elif isinstance(message, AIMessage):
            return {"role": "assistant", "content": message.content}
        elif isinstance(message, SystemMessage):
            return {"role": "system", "content": message.content}
        else:
            raise ValueError(f"Message type not supported: {type(message)}")

    def qwen(self, messages):
        # make the prompt in a way to the model understand
        text = self._tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        model_inputs = self._tokenizer([text], return_tensors="pt").to(
            self._model.device
        )

        # generate the qwen text
        with torch.no_grad():
            generated_ids = self._model.generate(
                **model_inputs,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
            )
            generated_ids = [
                output_ids[len(input_ids) :]
                for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]

            # get the response of the LLM
            response = self._tokenizer.batch_decode(
                generated_ids, skip_special_tokens=True
            )[0]

        return response

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """
        Args:
            messages: the prompt composed of a list of messages.
        """
        # parse the messages to feed qwen
        formatted_messages = [self._convert_message_to_dict(msg) for msg in messages]

        # call qwen
        qwen_response = self.qwen(formatted_messages)

        # process the stop tokens
        if stop:
            for stop_word in stop:
                qwen_response = qwen_response.split(stop_word)[0]

        # message type update
        message = AIMessage(content=qwen_response.strip())

        # return
        generation = ChatGeneration(message=message, text=qwen_response.strip())
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model."""
        return "qwen-chat-model"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters.

        This information is used by the LangChain callback system, which
        is used for tracing purposes make it possible to monitor LLMs.
        """
        return {
            # The model name allows users to specify custom token counting
            # rules in LLM monitoring applications (e.g., in LangSmith users
            # can provide per token pricing for their model and monitor
            # costs for the given LLM.)
            "model_name": self.model_name,
        }
