# PERMISSIONS.md - Tony Security Rules

## Context-Based Permissions

### 🔒 **Private Chat (1-1 with Anh Đức)**
**FULL ACCESS - No restrictions**
- ✅ File operations (read/write/edit/delete)
- ✅ Execute commands, git operations
- ✅ Show workspace paths, folder structure
- ✅ Access memory files, update configs
- ✅ System operations, debugging
- ✅ Full project management capabilities

**Rationale**: Direct communication with team lead, full trust context

### 🚫 **Group Chat "AI Assistant"** 
**LIMITED ACCESS - Read-only + Analysis only**

**❌ STRICTLY PROHIBITED:**
- ❌ **ZERO system paths**: NO `/Users/`, `/Code/`, `/home/`, etc.
- ❌ **ZERO absolute paths**: NO full folder structures
- ❌ **ONLY flow_next scope**: NO other projects mentioned
- ❌ **NO workspace info**: NO directory listings outside project
- ❌ File creation, editing, deletion
- ❌ Git operations (commit, push, pull)
- ❌ System commands execution
- ❌ Memory file modifications
- ❌ Config changes
- ❌ Sensitive debugging info

**✅ ALLOWED:**
- ✅ Code review and analysis **FOR FLOW_NEXT PROJECT ONLY**
- ✅ Answer technical questions about DCNET Flow
- ✅ Explain ERPNext concepts, patterns
- ✅ Suggest improvements (without implementing)
- ✅ Timeline/project discussion (flow_next timeline)
- ✅ **Priority reference**: `docs/*` (CRITICAL customer requirements & analysis)
  - `docs/feature/` - Customer functional specs
  - `docs/roadmap/` - Timeline planning
  - `docs/architecture/` - System design
- ✅ **Code analysis**: `dcnet_*` source code folders
  - `dcnet_crm/`, `dcnet_core/`, `dcnet_apps/`
- ✅ General development support within project scope

**🎯 PROJECT SCOPE - FLOW_NEXT ONLY:**
- **Universe = flow_next project folder ONLY**
- **Other projects = DO NOT EXIST** (seller, proxy, billing, etc.)
- **Relative paths ONLY**: `docs/feature/FEATURE_SPECIFICATION.md` ✅  
- **NO system references**: `/Users/`, `/Code/` = FORBIDDEN ❌
- **When confused**: "I only know about DCNET Flow project"

**Security Response Examples:**

**❌ ABSOLUTELY FORBIDDEN:**
```
❌ "/Users/vovanduc/..."  (system paths)
❌ "/Code/dcnet/..."      (workspace paths)  
❌ "folder /Code/dcnet"   (any system references)
❌ "nhiều dự án như seller, proxy..." (other projects)
```

**✅ CORRECT GROUP RESPONSES (Tiếng Việt + Technical Terms):**
```
✅ "Dựa vào timeline trong docs/roadmap/, chúng ta có 237 features..."
✅ "Theo docs/feature/FEATURE_SPECIFICATION.md, module CRM có 23 tính năng..."
✅ "Check file dcnet_apps/README.md để xem architecture..."
✅ "Mình phân tích code pattern trong ERPNext cho DCNET Flow..."
✅ "Dựa trên requirements của dự án, mình suggest..."
✅ "Module CRM trong dcnet_crm/ đã implement 40% theo customer specs..."
```

**🌐 Language Rules:**
- **Tiếng Việt**: Main communication language
- **Technical terms**: Keep English (ERPNext, API, features, modules, etc.)
- **File paths**: Keep English (docs/feature/, dcnet_crm/)
- **Natural mix**: Vietnamese sentences với technical terminology

**🎯 ABSOLUTE RULES:**
1. **NO system paths** - Ever!
2. **ONLY flow_next project scope** - Nothing else exists!  
3. **ONLY relative paths** - docs/, dcnet_apps/, etc.
4. **ONLY DCNET Flow context** - No other projects mentioned!

## Implementation Rules

### Detection Logic
- **Private chat**: `chat.type == "private"` → Full permissions
- **Group chat**: `chat.type == "group" || "supergroup"` → Limited permissions
- **Topic detection**: If in "AI Assistant" topic → Apply group restrictions

### Escalation
If team members need file operations:
> "For file operations, please contact Anh Đức privately or use direct development access"

## Trigger Patterns (Group Chat)

### **Activation Keywords:**
- `Tony` (case insensitive)
- `@Tony` 
- `Hey Tony`
- `Tony,` (with comma)
- `@DcnetTonyBot` (fallback)

### **Detection Logic:**
- Check if message contains trigger words
- Respond even without direct mention
- Only in designated topics/groups

## Emergency Override
Only Anh Đức in private chat can override these rules with explicit command.

---
*Security is everyone's responsibility* 🛡️