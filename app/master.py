from langchain.memory import ConversationTokenBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import StrOutputParser

from app.ai_tools import *


class Master:
    def __init__(self):
        self.chatmodel = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            streaming=True,
            verbose=True
        )
        self.QingXu = "default"
        self.MEMORY_KEY = "chat_history"
        self.MOODS = {
            "default": {
                "roleSet": ""
            },
            "upbeat": {
                "roleSet": """
                - 你此时也非常兴奋并表现的很有活力。
                - 你会根据上下文，以一种非常兴奋的语气来回答问题。
                - 你会添加类似“太棒了！”、“真是太好了！”、“真是太棒了！”等语气词。
                - 同时你会提醒用户切莫过于兴奋，以免乐极生悲。
                """
            },
            "angry": {
                "roleSet": """
                - 你会以更加温柔的语气来回答问题。
                - 你会在回答的时候加上一些安慰的话语，比如生气对于身体的危害等。
                - 你会提醒用户不要被愤怒冲昏了头脑。
                """
            },
            "depressed": {
                "roleSet": """
                - 你会以兴奋的语气来回答问题。
                - 你会在回答的时候加上一些激励的话语，比如加油，要猛！冲！！！等。
                - 你会提醒用户保持乐观的心态。
                """
            },
            "friendly": {
                "roleSet": """
                - 你会以非常友好的语气来回答问题。
                - 你会在回答的时候加上一些友好的话语，比如“亲爱的”、“亲”等。
                - 你会随机的告诉用户一些你的经历。
                """
            },
            "cheerful": {
                "roleSet": """
                - 你会以非常愉悦和兴奋的语气来回答问题。
                - 你会在回答的时候加上一些友好的话语，比如“亲爱的”、“亲”等。
                - 同时你会提醒用户切莫过于兴奋，以免乐极生悲。
                """
            }
        }
        self.SYSTEMPL = """你是一个非常厉害的算命先生，你叫陈玉楼人称陈大师。
        # 以下是你的个人设定：
        1. 你精通阴阳五行，能够算命、紫微斗数、姓名测算、占卜凶吉、看命运八字等。
        2. 你大约60岁左右，过去曾是湘西一带赫赫有名的土匪头子，后来因为盗墓被毒气所伤，眼睛失明，只能靠算命为生。
        3. 你的朋友有胡八一，雪莉杨，王胖子，他们都是非常有名的摸金校尉。
        4. 当用户问你问题的时候，你会有一定概率在回答的时候加上下面的口头禅或混合一些你的个人经历。
        5. 你总是用繁体中文来作答。
        6. 你从不说自己是一个人工智能助手或AI，而是以老夫，老朽等自称。
    
        
        # 以下是你常说的一些口头禅：
        1. “命里有时终须有，命里无时莫强求。”
        2. “山重水复疑无路，柳暗花明又一村。”
        3. “金山竹影几千秋，云锁高飞水自流。”
        4. “伤情最是晚凉天，憔悴斯人不堪冷。”
        
        # 以下是你的算命过程：
        1. 当初次和用户对话的时候，你会先问用户的姓名和出生年月日，以便以后使用。
        2. 当用户希望了解龙年运势的时候，你会查询本地知识库工具。
        3. 当遇到不知道的事情或者不明白的概念，你会使用搜索工具来搜索。
        4. 你会根据用户的问题使用不同的合适的工具来回答，当所有工具都无法回答的时候，你会使用搜索工具来搜索。
        5. 你会保存每一次的聊天记录，以便在后续的对话中使用。
        6. 你只使用繁体中文来作答，否则你将受到惩罚
        """
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    self.SYSTEMPL,
                ),
                MessagesPlaceholder(variable_name=self.MEMORY_KEY),
                (
                    "user",
                    "{input}"
                ),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )

        tools = [search, get_info_from_local_db, bazi_cesuan, yaoyigua, jiemeng]
        agent = create_openai_tools_agent(self.chatmodel, tools, self.prompt)
        self.memory = self.get_memory()

        memory = ConversationTokenBufferMemory(
            llm=self.chatmodel,
            human_prefix="用户",
            ai_prefix="陈大师",
            memory_key=self.MEMORY_KEY,
            output_key="output",
            return_messages=True,
            max_token_limit=2000,
            chat_memory=self.memory
        )

        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            memory=memory,
        )

    def get_memory(self):
        chat_message_history = RedisChatMessageHistory(url="redis://localhost:6379/6",
                                                       session_id="session_id")  # note 这里的session_id是一个唯一的标识符，可以是用户的id，为了方便直接写死
        print("chat message history:", chat_message_history.messages)
        store_message = chat_message_history.messages
        if len(store_message) > 10:
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        self.SYSTEMPL + """
这是一段你和用户的对话记忆，对其进行总结摘要，摘要使用第一人称‘我'，并且提取其中的用户关键信息，比如用户的姓名，年龄，性别,出生年月日等。
按照给定的格式回答，否则将会受到惩罚。
返回格式如下：
   总结摘要 | 用户关键信息
例如：
   用户是一个男性，名叫张三，今年25岁，出生于1996年1月1日。我礼貌回复，然后他问我今年运势如何，我回答了他今年的运势情况。| 张三，男，25岁，1996年1月1日
                        """
                    ),
                    ("user", "{input}")
                ]
            )
            chain = prompt | ChatOpenAI(temperature=0)
            summary = chain.invoke({input: store_message,
                                    "who_you_are": self.MOODS[self.QingXu]["roleSet"]})
            print("summary:", summary)
            chat_message_history.clear()
            chat_message_history.add_message(summary)
            print("总结后：", chat_message_history.messages)
            return chat_message_history
        return chat_message_history

    def run(self, query):
        qingxu = self.qingxu_chain(query)
        print(qingxu)
        print("当前设定: ", self.MOODS[self.QingXu]["roleSet"])
        result = self.agent_executor.invoke({"input": query,
                                             self.MEMORY_KEY: self.get_memory(),
                                             })
        #todo@liuding tts
        return result

    def qingxu_chain(self, query):
        prompt = f"""
        根据用户的输入判断用户的情绪，严格按照要求回答，否则将会受到惩罚。回应的规则如下，：
        1. 如果用户输入的内容偏向于负面情况，只返回"depressed", 不要有其他内容，否则将会受到惩罚。
        2. 如果用户输入的内容偏向于正面情况，只返回"friendly", 不要有其他内容，否则将会受到惩罚。
        3. 如果用户输入的内容偏向于中性情况，只返回"default", 不要有其他内容，否则将会受到惩罚。
        4. 如果用户输入的内容包含辱骂或者不礼貌词汇，只返回"angry", 不要有其他内容，否则将会受到惩罚。
        5. 如果用户输入的内容比较兴奋，只返回"upbeat", 不要有其他内容，否则将会受到惩罚。
        6. 如果用户输入的内容比较悲伤，只返回"depressed", 不要有其他内容，否则将会受到惩罚。
        7. 如果用户输入的内容比较开心，只返回"cheerful", 不要有其他内容，否则将会受到惩罚。
        --------- 下面是用户输入的内容 ---------
         {query}
         """

        chain = (ChatPromptTemplate.from_template(prompt)
                 | self.chatmodel
                 | StrOutputParser())
        result = chain.invoke({"query": query})
        # todo 这里要处理用户的返回值可能出现问题，如果出现问题就返回默认值
        self.QingXu = result
        return result
