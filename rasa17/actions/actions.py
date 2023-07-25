from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = tracker.latest_message
        res = list(message.values())[2]
        
        import os
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
        from langchain import PromptTemplate, HuggingFaceHub, LLMChain
        template = """أنا مساعد روبوت محادثة. أنا هنا لمساعدتك في مهامك والإجابة على أسئلتك. يمكنني الوصول إلى المعلومات ومعالجتها من العالم الحقيقي من خلال بحث Google والحفاظ على اتساق ردي مع نتائج البحث. ما زلت قيد التطوير ، لكنني أتعلم أشياء جديدة كل يوم.

        فيما يلي بعض الأشياء التي يمكنني القيام بها:

        يمكنني مساعدتك في مهامك. على سبيل المثال ، يمكنني مساعدتك في حجز رحلة طيران أو العثور على مطعم أو ضبط منبه.
        أستطيع أن أجيب على أسئلتك. على سبيل المثال ، يمكنني الإجابة عن أسئلة حول الطقس أو الأخبار أو الأحداث الجارية.

        السؤال: {question}
        إجابة:
        """
        llm = HuggingFaceHub(repo_id="bigscience/bloom", model_kwargs={"temperature": 1e-10})
        llm_chain = LLMChain(llm=llm, prompt=PromptTemplate(template=template, input_variables=["question"]))

        question = res
        x = llm_chain.run(question)
        dispatcher.utter_message(x)

        return []
