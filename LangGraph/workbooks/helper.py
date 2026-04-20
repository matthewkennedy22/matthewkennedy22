"""Lesson 6: Essay Writer — Gradio UI and graph factory (`ewriter`, `writer_gui`)."""

from __future__ import annotations

import os
import sqlite3
import uuid
from typing import List, TypedDict

import gradio as gr
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field
from tavily import TavilyClient

load_dotenv()

PLAN_PROMPT = """You are an expert writer tasked with writing a high level outline of an essay. \
Write such an outline for the user provided topic. Give an outline of the essay along with any relevant notes \
or instructions for the sections."""

WRITER_PROMPT = """You are an essay assistant tasked with writing excellent 5-paragraph essays.\
Generate the best essay possible for the user's request and the initial outline. \
If the user provides critique, respond with a revised version of your previous attempts. \
Utilize all the information below as needed:

------

{content}"""

REFLECTION_PROMPT = """You are a teacher grading an essay submission. \
Generate critique and recommendations for the user's submission. \
Provide detailed recommendations, including requests for length, depth, style, etc."""

RESEARCH_PLAN_PROMPT = """You are a researcher charged with providing information that can \
be used when writing the following essay. Generate a list of search queries that will gather \
any relevant information. Only generate 3 queries max."""

RESEARCH_CRITIQUE_PROMPT = """You are a researcher charged with providing information that can \
be used when making any requested revisions (as outlined below). \
Generate a list of search queries that will gather any relevant information. Only generate 3 queries max."""


class AgentState(TypedDict, total=False):
    task: str
    plan: str
    draft: str
    critique: str
    content: List[str]
    revision_number: int
    max_revisions: int


class Queries(BaseModel):
    queries: List[str] = Field(default_factory=list)


def _build_graph(checkpointer: SqliteSaver):
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    def plan_node(state: AgentState):
        messages = [
            SystemMessage(content=PLAN_PROMPT),
            HumanMessage(content=state["task"]),
        ]
        response = model.invoke(messages)
        return {"plan": response.content}

    def research_plan_node(state: AgentState):
        queries = model.with_structured_output(Queries).invoke(
            [
                SystemMessage(content=RESEARCH_PLAN_PROMPT),
                HumanMessage(content=state["task"]),
            ]
        )
        content = state.get("content") or []
        for q in queries.queries:
            response = tavily.search(query=q, max_results=2)
            for r in response["results"]:
                content.append(r["content"])
        return {"content": content}

    def generation_node(state: AgentState):
        content = "\n\n".join(state.get("content") or [])
        user_message = HumanMessage(
            content=f"{state['task']}\n\nHere is my plan:\n\n{state.get('plan', '')}"
        )
        messages = [
            SystemMessage(content=WRITER_PROMPT.format(content=content)),
            user_message,
        ]
        response = model.invoke(messages)
        return {
            "draft": response.content,
            "revision_number": state.get("revision_number", 1) + 1,
        }

    def reflection_node(state: AgentState):
        messages = [
            SystemMessage(content=REFLECTION_PROMPT),
            HumanMessage(content=state.get("draft", "")),
        ]
        response = model.invoke(messages)
        return {"critique": response.content}

    def research_critique_node(state: AgentState):
        queries = model.with_structured_output(Queries).invoke(
            [
                SystemMessage(content=RESEARCH_CRITIQUE_PROMPT),
                HumanMessage(content=state.get("critique", "")),
            ]
        )
        content = state.get("content") or []
        for q in queries.queries:
            response = tavily.search(query=q, max_results=2)
            for r in response["results"]:
                content.append(r["content"])
        return {"content": content}

    def should_continue(state: AgentState):
        if state.get("revision_number", 0) > state.get("max_revisions", 2):
            return END
        return "reflect"

    builder = StateGraph(AgentState)
    builder.add_node("planner", plan_node)
    builder.add_node("generate", generation_node)
    builder.add_node("reflect", reflection_node)
    builder.add_node("research_plan", research_plan_node)
    builder.add_node("research_critique", research_critique_node)
    builder.set_entry_point("planner")
    builder.add_conditional_edges(
        "generate",
        should_continue,
        {END: END, "reflect": "reflect"},
    )
    builder.add_edge("planner", "research_plan")
    builder.add_edge("research_plan", "generate")
    builder.add_edge("reflect", "research_critique")
    builder.add_edge("research_critique", "generate")
    return builder.compile(checkpointer=checkpointer)


class EssayWriter:
    """Holds an open SQLite connection so the compiled graph stays valid (including from Gradio threads)."""

    def __init__(self) -> None:
        self._sqlite_conn = sqlite3.connect(":memory:", check_same_thread=False)
        memory = SqliteSaver(self._sqlite_conn)
        self.graph = _build_graph(memory)


def ewriter() -> EssayWriter:
    return EssayWriter()


def writer_gui(graph):
    def run(task: str, max_revisions: float):
        task = (task or "").strip()
        if not task:
            return "Enter an essay topic or question."
        thread = {"configurable": {"thread_id": str(uuid.uuid4())}}
        lines: List[str] = []
        initial: AgentState = {
            "task": task,
            "max_revisions": int(max_revisions),
            "revision_number": 1,
        }
        try:
            for step in graph.stream(initial, thread):
                lines.append(str(step))
            return "\n\n---\n\n".join(lines) if lines else "(no events)"
        except Exception as e:
            return f"Error: {e!s}"

    with gr.Blocks(title="Essay Writer") as app:
        gr.Markdown("# Essay writer (LangGraph + Tavily)")
        task_in = gr.Textbox(
            label="Topic / task",
            lines=3,
            placeholder="e.g. What is the difference between LangChain and LangSmith?",
        )
        max_rev = gr.Slider(1, 5, value=2, step=1, label="Max revisions")
        out = gr.Textbox(label="Streamed graph updates", lines=28)
        go = gr.Button("Run")
        go.click(run, inputs=[task_in, max_rev], outputs=out)
    return app
