# PO Copilot — Demo Video Script
### 💎 Team Diamond × SKF | Hackathon 2026

---

## 🎬 INTRO (15 sec)

> "Hi, we're **Team Diamond** from SKF. We built **PO Copilot** — an AI-powered Product Owner assistant that takes raw meeting notes and documents, turns them into structured work items, and then uses **AI dev agents** to automatically implement the code and create Pull Requests on GitHub. Let's see it in action."

---

## 📄 STEP 1 — Upload Documents (30 sec)

**What to show:** The Upload page  
**What to do:**
1. Show the header — **PO Copilot** logo, **💎 Team Diamond × SKF** badge
2. Select a project from the dropdown (e.g., "test" or create a new one)
3. Upload a meeting notes file (drag & drop or click)
4. Show the confirmation: "1 document uploaded and indexed"
5. Click **"Next: AI Analysis"**

> "We start by uploading project documents — meeting notes, requirement specs, anything. The system chunks and indexes them using **ChromaDB** vector storage for RAG retrieval."

---

## 🤖 STEP 2 — AI Analysis & Ticket Generation (30 sec)

**What to show:** The Generate page  
**What to do:**
1. Show the 4 work item types: Epics, Features, User Stories, Tasks
2. Click **"✨ Generate ADO Tickets"**
3. Wait for the AI spinner — "Analyzing documents with AI..."
4. Show the results landing on Step 3 (the Board)

> "Now the AI analyzes all uploaded documents using **GPT-4o via OpenRouter** and generates a full Azure DevOps-style hierarchy — Epics, Features, User Stories, and Tasks — all with proper parent-child relationships, acceptance criteria, and story points."

---

## 🚀 STEP 3 — Backlog Board & AI Agents (60 sec)

**What to show:** The 4-column Kanban board  
**What to do:**

### 3a. Board Overview (15 sec)
1. Show the **4 columns**: Backlog → Agent Assigned → Agent Working → Done/PR Created
2. Point out the **stats bar**: total items, story points, type counts
3. Show the **GitHub badge** linking to `sekhar-hackathon/po-copilot`
4. Show ticket IDs (PC-1, PC-2...) and **parent-child links** (↳ PC-3)

> "All tickets land in a Kanban board with full hierarchy. Each card shows its ticket ID, parent link, type, and story points."

### 3b. Assign a Single Agent (20 sec)
1. Pick a **User Story** card
2. Click the **START** button on the agent status bar
3. Watch the card move: Backlog → Agent Assigned → Agent Working
4. Show the **Agent Activity Log** (terminal-style) updating in real-time
5. Card lands in **Done/PR Created** with a PR link

> "Here's the magic — click **START** on any ticket, and an AI dev agent takes over. It reads the requirements, generates production code, creates a feature branch on GitHub, commits the files, and opens a Pull Request — all automatically."

### 3c. Show the PR on GitHub (10 sec)
1. Click the **PR #** link on the card
2. Show the GitHub PR page — ticket details table, hierarchy info, files changed, Team Diamond branding

> "The PR includes full ticket details — type, parent, acceptance criteria, story points — just like referencing AD#1234 in Azure DevOps."

### 3d. Batch Assign & Stop (15 sec)
1. Click **"🤖 Assign All Agents"**
2. Show multiple agents working simultaneously
3. Click **"⏹ Stop All"** to demonstrate the kill switch
4. Show the **STOP** button on individual cards

> "You can batch-assign all tickets at once, and if something goes wrong, hit **Stop All** — no runaway agents."

---

## 🔄 STEP 4 — Reset & Control (10 sec)

**What to show:** Reset functionality  
**What to do:**
1. Click **"🔄 Reset"** on the board to clear agent states
2. Click **"Reset All"** to go back to Step 1

> "Full control at every stage — reset the board, regenerate tickets, or start completely fresh."

---

## 🔍 BONUS — Edit & Manage (10 sec)

**What to show:** Card editing  
**What to do:**
1. Hover over a card — show edit/delete icons
2. Click edit — modify title, description, story points
3. Switch between **Board** and **List** views

> "Every ticket is fully editable — update titles, descriptions, or remove items before the agents start working."

---

## 🎤 CLOSING (15 sec)

> "**PO Copilot** bridges the gap between product planning and development. Upload your documents, let AI structure them, and let AI agents build the code. From meeting notes to merged PRs — that's the power of agentic development."

> "**Team Diamond × SKF** — thank you!"

---

## 📋 QUICK REFERENCE

| Timestamp | Section | Duration |
|-----------|---------|----------|
| 0:00 | Intro | 15s |
| 0:15 | Step 1 — Upload | 30s |
| 0:45 | Step 2 — AI Generation | 30s |
| 1:15 | Step 3 — Board & Agents | 60s |
| 2:15 | Step 4 — Reset | 10s |
| 2:25 | Bonus — Edit/Manage | 10s |
| 2:35 | Closing | 15s |
| **Total** | | **~2:50** |

---

## 🛠 TECH STACK (mention during demo)

- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: Python FastAPI
- **AI**: GPT-4o via OpenRouter
- **Vector DB**: ChromaDB (RAG)
- **Code Agent**: Custom AI agent → GitHub API (branches, commits, PRs)
- **SSL**: truststore (corporate proxy compatible)
