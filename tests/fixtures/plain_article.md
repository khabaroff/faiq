# Agent Orchestration Patterns

There are three common patterns for multi-agent systems:

1. Supervisor — one agent decides which sub-agent to call
2. Tool-use — agents expose capabilities as tools
3. Graph-based — agents are nodes in a directed graph

Each pattern has trade-offs. Supervisor is easiest to debug. Graph-based
is most flexible but requires careful state management.

## Key Takeaways

- Always validate agent output before passing to the next agent
- Use structured output (JSON) for inter-agent communication
- Monitor token usage per-agent

## References

LangGraph documentation covers the graph-based approach in detail.