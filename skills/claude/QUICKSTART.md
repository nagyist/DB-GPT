# Claude SKILL 机制 - 快速入门指南

## ✅ 已实现的功能

| 功能 | 状态 | 文件位置 |
|------|--------|----------|
| SKILL 文件解析 | ✅ | `packages/dbgpt-core/src/dbgpt/agent/claude_skill/__init__.py` |
| Agent 集成 | ✅ | `packages/dbgpt-core/src/dbgpt/agent/claude_skill/agent.py` |
| 自动匹配技能 | ✅ | `FileBasedSkill.matches()` |
| 手动选择技能 | ✅ | `ClaudeSkillAgent.set_skill()` |
| 示例 SKILL 文件 | ✅ | `skills/claude/*/SKILL.md` |
| 完整示例 | ✅ | `examples/agents/claude_skill_example.py` |

## 📦 文件结构

```
packages/dbgpt-core/src/dbgpt/agent/claude_skill/
├── __init__.py         # 核心类：ClaudeSkill, FileBasedSkill, SkillRegistry
└── agent.py           # ClaudeSkillAgent - 集成到 DB-GPT Agent

examples/
├── agents/
│   └── claude_skill_example.py     # 完整使用示例
└── skills/claude/
    ├── explain-code/SKILL.md         # 代码解释技能
    ├── debug-code/SKILL.md           # 代码调试技能
    ├── write-code/SKILL.md           # 代码编写技能
    ├── simplify-code/SKILL.md        # 代码简化技能
    └── README.md                    # 详细文档
```

## 🚀 5 分钟快速开始

### 1. 创建 SKILL 文件

创建 `my-skill/SKILL.md`：

```markdown
---
name: my-custom-skill
description: Custom skill for specific task. Use when user asks about this topic.
---

When handling this task:

1. **First step**: What to do first
2. **Second step**: What to do next
3. **Final step**: How to complete

Additional guidelines and best practices...
```

### 2. 加载技能

```python
from dbgpt.agent.claude_skill import load_skills_from_dir

load_skills_from_dir("skills/claude/", recursive=True)
```

### 3. 创建 Agent

```python
from dbgpt.agent.claude_skill import ClaudeSkillAgent

agent = ClaudeSkillAgent()
await agent.bind(context).bind(llm_config).bind(memory).build()
```

### 4. 自动匹配技能

```python
user_input = "Can you explain this code?"
agent.detect_and_apply_skill(user_input)

if agent.current_skill:
    print(f"Using skill: {agent.current_skill.metadata.name}")
```

## 📝 SKILL 文件格式

标准格式：

```markdown
---
name: skill-name
description: Description with trigger conditions. Use when user asks...
---

Instructions for the AI...
```

### 元数据字段

| 字段 | 必需 | 说明 |
|------|--------|------|
| `name` | ✅ | 技能的唯一标识符 |
| `description` | ✅ | 描述和触发条件 |

### 触发条件示例

在 `description` 中包含这些短语以触发技能：

- `"Use when user asks to..."`
- `"Use when the user wants..."`
- `"Use when explaining how code works"`
- `"when user asks 'how does this work?'"`

## 🎯 自动匹配机制

SKILL 系统通过以下方式匹配：

1. **提取关键词**：从 description 中提取关键词
2. **匹配用户输入**：检查用户输入是否包含关键词
3. **技能名称匹配**：直接匹配技能名称

### 匹配优先级

当多个技能匹配时：
- 选择指令更详细的技能
- 选择第一个匹配的技能

## 🎮 完整示例

```python
import asyncio
import os
from dbgpt.agent import AgentContext, AgentMemory, LLMConfig
from dbgpt.agent.claude_skill import (
    ClaudeSkillAgent,
    load_skills_from_dir,
)
from dbgpt.model.proxy.llms.siliconflow import SiliconFlowLLMClient

async def main():
    # 1. 加载技能
    load_skills_from_dir("skills/claude/", recursive=True)

    # 2. 创建 LLM 配置
    llm_client = SiliconFlowLLMClient(
        model_alias="Qwen/Qwen2.5-Coder-32B-Instruct",
    )

    # 3. 创建 Agent
    agent = ClaudeSkillAgent()
    agent_memory = AgentMemory()
    context = AgentContext(conv_id="test_conv")

    await agent.bind(context).bind(LLMConfig(llm_client=llm_client)).bind(agent_memory).build()

    # 4. 使用技能
    user_input = "Can you explain how this function works?"
    agent.detect_and_apply_skill(user_input)

    if agent.current_skill:
        print(f"激活技能: {agent.current_skill.metadata.name}")
        print(f"描述: {agent.current_skill.metadata.description}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🛠️ 核心 API

### ClaudeSkillAgent

```python
# 自动匹配技能
agent.detect_and_apply_skill(user_input)

# 手动设置技能
agent.set_skill("explain-code")

# 清除当前技能
agent.clear_skill()

# 获取可用技能列表
skills = agent.get_available_skills()

# 获取当前技能
current = agent.current_skill
```

### FileBasedSkill

```python
from dbgpt.agent.claude_skill import FileBasedSkill

skill = FileBasedSkill("path/to/SKILL.md")

# 获取元数据
print(skill.metadata.name)
print(skill.metadata.description)

# 获取指令
print(skill.instructions)

# 检查是否匹配
if skill.matches(user_input):
    print("匹配成功!")

# 获取提示词模板
prompt = skill.get_prompt()
```

### SkillRegistry

```python
from dbgpt.agent.claude_skill import get_registry

registry = get_registry()

# 注册技能
registry.register_skill(skill)

# 获取技能
skill = registry.get_skill("explain-code")

# 匹配技能
matching = registry.match_skill(user_input)

# 列出所有技能
all_skills = registry.list_skills()

# 从目录加载
registry.load_from_directory("skills/", recursive=True)
```

## 📚 预设 SKILL 示例

### explain-code

用于解释代码的工作原理，包含：

- 类比（将代码比作日常事物）
- ASCII 图表（显示流程、结构或关系）
- 逐步解释
- 常见陷阱提示

### debug-code

用于调试代码，包含：

- 识别问题
- 解释原因
- 显示修复方案
- 预防未来问题
- 测试修复方法

### write-code

用于编写新代码，包含：

- 理解需求
- 规划结构
- 编写整洁代码
- 包含导入
- 添加错误处理
- 提供使用示例

### simplify-code

用于简化代码，包含：

- 识别复杂性
- 逐步重构
- 移除重复
- 提高可读性
- 保持功能不变

## 🔧 高级用法

### 自定义匹配逻辑

```python
from dbgpt.agent.claude_skill import ClaudeSkill

class MyCustomSkill(ClaudeSkill):
    @classmethod
    def name(cls) -> str:
        return "my-skill"

    @classmethod
    def description(cls) -> str:
        return "Custom skill description"

    @classmethod
    def instructions(cls) -> str:
        return "Custom instructions..."

    @classmethod
    def matches(cls, user_input: str) -> bool:
        # 自定义匹配逻辑
        return "magic" in user_input.lower()
```

### 动态技能加载

```python
from dbgpt.agent.claude_skill import ClaudeSkillAgent, get_registry

registry = get_registry()
registry.load_from_directory("~/.claude/skills/", recursive=True)

agent = ClaudeSkillAgent(skill_registry=registry)
```

## 🎓 最佳实践

1. **清晰的描述**：在 description 中明确说明何时使用该技能
2. **具体的指令**：提供清晰的步骤和指南
3. **使用触发词**：在描述中包含 "Use when..." 或 "when user asks..."
4. **保持简单**：每个技能专注于单一任务
5. **版本控制**：使用 Git 跟踪 SKILL 文件的变更

## 🐛 故障排除

### 技能不匹配

**原因**：描述中的关键词不清晰

**解决**：在描述中添加明确的 "Use when..." 语句

### 加载失败

**原因**：文件格式不正确

**解决**：确保文件以 `---` 开头，格式为：
```markdown
---
name: skill-name
description: Description
---

Instructions...
```

### 错误的技能被选中

**原因**：多个技能包含相同的关键词

**解决**：
1. 使描述更具体
2. 使用手动选择：`agent.set_skill("specific-skill")`

## 📚 参考资源

- **完整示例**：`examples/agents/claude_skill_example.py`
- **详细文档**：`skills/claude/README.md`
- **SKILL 文件示例**：`skills/claude/*/SKILL.md`

## 🎉 开始使用

运行示例：

```bash
cd /Users/chenketing.ckt/Desktop/project/DB-GPT
python examples/agents/claude_skill_example.py
```

创建你自己的 SKILL：

1. 创建目录和 `SKILL.md` 文件
2. 定义 name 和 description
3. 编写指令
4. 运行 Agent 测试

祝使用愉快！ 🚀
