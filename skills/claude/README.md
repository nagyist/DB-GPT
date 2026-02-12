# Claude-Style SKILL 机制 for DB-GPT

这是 Claude 风格的 SKILL 机制在 DB-GPT 中的实现，允许使用简单的 Markdown 文件定义 Agent 的技能和行为。

## 概述

Claude SKILL 机制是一种简单而强大的方式来定义 AI 助手的行为：

- **简单的 Markdown 文件**：每项技能是一个 `SKILL.md` 文件
- **声明式元数据**：在文件顶部定义名称和描述
- **行为指令**：描述 AI 应该如何响应
- **自动匹配**：基于用户输入自动选择合适的技能

## SKILL 文件格式

```markdown
---
name: skill-name
description: Skill description with triggers. Use when user asks specific questions.
---

When doing this task, always include:

1. **Step 1**: Instruction
2. **Step 2**: Instruction
3. **Step 3**: Instruction

Additional guidelines and best practices...
```

### 元数据部分

- `name`: 技能的唯一标识符
- `description`: 技能描述，包含触发条件（如 "Use when user asks..."）

### 指令部分

分隔线 `---` 之后是实际的指令，告诉 AI 如何响应特定类型的请求。

## 快速开始

### 1. 创建 SKILL 文件

创建 `~/.claude/skills/my-skill/SKILL.md`：

```markdown
---
name: summarize-text
description: Summarizes text concisely. Use when the user asks to summarize content.
---

When summarizing text:

1. **Identify key points**: Extract the main ideas
2. **Maintain meaning**: Keep the core message intact
3. **Be concise**: Use fewer words than the original
4. **Use bullet points**: Organize information clearly

Create summaries that are easy to scan and understand quickly.
```

### 2. 加载技能

```python
from dbgpt.agent.claude_skill import load_skills_from_dir

load_skills_from_dir("~/.claude/skills/", recursive=True)
```

### 3. 创建 Agent

```python
from dbgpt.agent.claude_skill import ClaudeSkillAgent

agent = ClaudeSkillAgent()
await agent.bind(context).bind(llm_config).bind(memory).build()
```

### 4. 自动匹配技能

Agent 会根据用户输入自动选择技能：

```python
user_input = "Can you summarize this text?"
agent.detect_and_apply_skill(user_input)

if agent.current_skill:
    print(f"Using skill: {agent.current_skill.metadata.name}")
```

## 核心 API

### ClaudeSkillAgent

```python
agent = ClaudeSkillAgent(skill_registry=registry)

# 自动匹配技能
agent.detect_and_apply_skill(user_input)

# 手动设置技能
agent.set_skill("explain-code")

# 清除当前技能
agent.clear_skill()

# 获取可用技能列表
skills = agent.get_available_skills()
```

### SkillRegistry

```python
from dbgpt.agent.claude_skill import get_registry

registry = get_registry()

# 从目录加载技能
registry.load_from_directory("skills/", recursive=True)

# 获取特定技能
skill = registry.get_skill("explain-code")

# 匹配技能
matching_skill = registry.match_skill(user_input)

# 列出所有技能
skills = registry.list_skills()
```

## 示例 SKILL 文件

### explain-code

```markdown
---
name: explain-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---

When explaining code, always include:

1. **Start with an analogy**: Compare the code to something from everyday life
2. **Draw a diagram**: Use ASCII art to show the flow, structure, or relationships
3. **Walk through the code**: Explain step-by-step what happens
4. **Highlight a gotcha**: What's a common mistake or misconception?

Keep explanations conversational. For complex concepts, use multiple analogies.
```

### debug-code

```markdown
---
name: debug-code
description: Helps debug code by identifying issues, suggesting fixes, and explaining why the bug occurred. Use when the user has code that isn't working as expected.
---

When debugging code:

1. **Identify the issue**: Clearly state what's going wrong
2. **Explain the cause**: Why is this happening? (refer to the specific line or logic)
3. **Show the fix**: Provide corrected code with clear changes
4. **Prevent recurrence**: Explain how to avoid this issue in the future
5. **Test the fix**: Describe how to verify the solution works

Be specific with line numbers and variable names.
```

### write-code

```markdown
---
name: write-code
description: Writes new code based on requirements. Use when the user asks to create, implement, or write code.
---

When writing code:

1. **Understand requirements**: Clarify what needs to be built before coding
2. **Plan the structure**: Briefly describe the architecture or approach
3. **Write clean code**: Follow best practices, add necessary comments
4. **Include imports**: Show all required imports
5. **Add error handling**: Include try-except blocks where appropriate
6. **Provide examples**: Show how to use the code

Write production-ready code that's readable and maintainable.
```

### simplify-code

```markdown
---
name: simplify-code
description: Simplifies complex code by refactoring, removing redundancy, and making it more readable. Use when the user asks to simplify, clean up, or refactor code.
---

When simplifying code:

1. **Identify complexity**: Point out what makes the code hard to understand
2. **Refactor step by step**: Show each simplification with explanation
3. **Remove duplication**: Combine repeated logic
4. **Improve readability**: Use better variable names and structure
5. **Preserve functionality**: Ensure the code still does the same thing
6. **Test mentally**: Walk through the simplified code to verify correctness

Keep the code's original intent. If simplification requires trade-offs, explain them.
```

## 技能匹配机制

SKILL 机制通过以下方式匹配技能：

1. **描述中的关键词**：从 `description` 中提取触发词
2. **技能名称**：直接匹配技能名称
3. **用户输入**：检查用户输入是否包含这些关键词

### 匹配优先级

当多个技能匹配时，选择：
- 指令更详细的技能
- 第一个匹配的技能

## 文件结构

```
~/.claude/skills/
├── explain-code/
│   └── SKILL.md
├── debug-code/
│   └── SKILL.md
├── write-code/
│   └── SKILL.md
└── simplify-code/
    └── SKILL.md
```

每个技能都有自己的目录，其中包含 `SKILL.md` 文件。

## 完整示例

查看 `examples/agents/claude_skill_example.py` 获取完整的使用示例。

## 高级用法

### 自定义匹配逻辑

通过子类化 `ClaudeSkill` 实现自定义匹配：

```python
from dbgpt.agent.claude_skill import ClaudeSkill

class CustomSkill(ClaudeSkill):
    @classmethod
    def name(cls) -> str:
        return "my-custom-skill"

    @classmethod
    def description(cls) -> str:
        return "A custom skill"

    @classmethod
    def instructions(cls) -> str:
        return "Custom instructions..."

    @classmethod
    def matches(cls, user_input: str) -> bool:
        return "magic" in user_input.lower()
```

### 动态技能加载

```python
from dbgpt.agent.claude_skill import ClaudeSkillAgent, create_skill_agent

async def main():
    skill_dir = "~/.claude/skills/"
    context = AgentContext(conv_id="test")

    agent = await create_skill_agent(skill_dir, context)
```

## 与其他 Agent 类型集成

可以与任何 DB-GPT Agent 集成：

```python
class MyCustomAgent(ClaudeSkillAgent, ConversableAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Your custom implementation...
```

## 最佳实践

1. **明确的描述**：在 `description` 中清楚地说明何时使用该技能
2. **具体的指令**：提供清晰的步骤和指南
3. **使用触发词**：在描述中包含 "Use when..." 或 "when the user asks..."
4. **保持简单**：每个技能专注于单一任务
5. **版本控制**：使用 Git 跟踪 SKILL 文件的变更

## 故障排除

### 问题：技能不匹配

**原因**：描述中的关键词不清晰或不包含触发词

**解决**：在描述中添加明确的 "Use when..." 语句

### 问题：加载失败

**原因**：文件格式不正确

**解决**：确保文件以 `---` 开头，格式为：
```markdown
---
name: skill-name
description: Description
---

Instructions...
```

### 问题：错误的技能被选中

**原因**：多个技能包含相同的关键词

**解决**：
1. 使描述更具体
2. 使用手动技能选择：`agent.set_skill("specific-skill")`

## 贡献

欢迎贡献新的 SKILL 文件！请遵循格式规范，并确保描述清晰。

## 许可证

MIT License
