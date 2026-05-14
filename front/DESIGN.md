# DESIGN.md

> 深空站控制台的克制与理性——信息在暗色中精确发光，无一处多余。

## 1. Visual Theme & Atmosphere

**Style**: Dark Restrained (暗黑 + 克制混搭)
**Keywords**: 深邃、克制、理性、高效、精确、代码感、安静
**Tone**: 专业冷静的技术工具 — NOT 花哨、NOT 玩具感、NOT 过度装饰
**Feel**: 深夜程序员打开的那个让人安心的深色 IDE，一切都在该在的位置

**Interaction Tier**: L1 精致静态
**Dependencies**: CSS only (无 GSAP / ScrollTrigger / Lenis)

## 2. Color Palette & Roles

```css
:root {
  /* Backgrounds */
  --bg: #0D1117;                                    /* 页面背景 (GitHub Dark) */
  --bg-elevated: #161B22;                           /* 略高一层背景 (导航/侧栏) */
  --surface: #1C2128;                               /* 卡片/容器 */
  --surface-alt: #21262D;                           /* 交替 section / 次级卡片 */
  --surface-hover: #262C36;                         /* 悬停态表面 */

  /* Borders */
  --border: #30363D;                                /* 默认边框 */
  --border-hover: #484F58;                          /* 悬停边框 */
  --border-active: #58A6FF;                         /* 聚焦/活跃边框 */

  /* Text */
  --text: #E6EDF3;                                  /* 标题、重要文字 */
  --text-secondary: #9CA3AF;                        /* 正文、描述 */
  --text-tertiary: #6B7280;                         /* 标签、辅助信息、placeholder */
  --text-inverse: #0D1117;                          /* 反色文字(用在亮色按钮上) */

  /* Accent */
  --accent: #58A6FF;                                /* 主强调色：CTA、链接、活跃态 */
  --accent-hover: #79C0FF;                          /* 强调色 hover */
  --accent-pressed: #388BFD;                        /* 强调色按下 */
  --accent-subtle: rgba(88, 166, 255, 0.10);        /* 强调色淡底 (标签/高亮行) */

  /* Secondary accent */
  --accent-secondary: #A78BFA;                      /* 辅助强调色 (紫) */
  --accent-secondary-subtle: rgba(167, 139, 250, 0.10);

  /* RGB variants for rgba() */
  --bg-rgb: 13, 17, 23;
  --accent-rgb: 88, 166, 255;
  --accent-secondary-rgb: 167, 139, 250;

  /* Semantic */
  --success: #3FB950;                               /* 正确/通过 */
  --success-subtle: rgba(63, 185, 80, 0.12);
  --error: #F85149;                                 /* 错误/不通过 */
  --error-subtle: rgba(248, 81, 73, 0.12);
  --warning: #D29922;                               /* 警告 */
  --warning-subtle: rgba(210, 153, 34, 0.12);
  --info: #58A6FF;                                  /* 信息 */
  --info-subtle: rgba(88, 166, 255, 0.10);
}
```

**Color Rules:**
- 所有颜色通过 CSS 变量引用，禁止硬编码 hex
- 同一 section 内只用一个强调色（蓝或紫），不混用
- 语义色（success/error/warning）仅用于状态反馈，不做装饰
- 背景层级严格递增：`--bg` → `--bg-elevated` → `--surface` → `--surface-alt`
- 边框默认用 `--border`，hover 用 `--border-hover`，仅 focus/active 才用 `--border-active`
- 文字颜色不超过三级：`--text` / `--text-secondary` / `--text-tertiary`

## 3. Typography Rules

**Font Stack:**
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');
```

| Role | Font | Size | Weight | Line Height | Letter Spacing |
|------|------|------|--------|-------------|----------------|
| Page Title H1 | Inter, Noto Sans SC | 24px / 1.5rem | 700 | 1.3 | -0.02em |
| Section Title H2 | Inter, Noto Sans SC | 18px / 1.125rem | 600 | 1.4 | -0.01em |
| H3 | Inter, Noto Sans SC | 15px / 0.9375rem | 600 | 1.4 | — |
| Body | Inter, Noto Sans SC | 14px / 0.875rem | 400 | 1.6 | — |
| Label / Caption | Inter, Noto Sans SC | 12px / 0.75rem | 500 | 1.4 | 0.02em |
| Mono / Code | JetBrains Mono | 13px / 0.8125rem | 400 | 1.5 | — |
| KPI Number | Inter | 28px / 1.75rem | 700 | 1.2 | -0.02em |

**Typography Rules:**
- 中文内容使用 Noto Sans SC，英文优先 Inter，通过 `font-family: Inter, "Noto Sans SC", sans-serif` 实现自动切换
- Heading weight >= 600，正文 400-500
- 中文正文行高 >= 1.6，英文正文行高 >= 1.5
- 代码片段和技术关键词用 JetBrains Mono
- **NEVER use**: Comic Sans, Papyrus, Impact, 宋体 (SimSun), 楷体

**Text Decoration:**
- 克制风格：全部标题无渐变、无投影
- 页面标题允许使用 `--accent` 色点缀关键词（非渐变，单色 highlight）
- 链接文字：hover 时 underline offset 过渡，不加 text-shadow

## 4. Component Stylings

### Buttons

```css
/* Primary Button */
.btn-primary {
  background: var(--accent);
  color: var(--text-inverse);
  border: 1px solid transparent;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-primary:hover {
  background: var(--accent-hover);
}
.btn-primary:active {
  background: var(--accent-pressed);
  transform: scale(0.98);
}
.btn-primary:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.btn-primary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
}

/* Secondary / Ghost Button */
.btn-secondary {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-secondary:hover {
  color: var(--text);
  border-color: var(--border-hover);
  background: var(--surface-hover);
}
.btn-secondary:active {
  transform: scale(0.98);
}
.btn-secondary:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.btn-secondary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Danger Button */
.btn-danger {
  background: transparent;
  color: var(--error);
  border: 1px solid var(--error);
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-danger:hover {
  background: var(--error-subtle);
}
.btn-danger:active {
  transform: scale(0.98);
}
.btn-danger:focus-visible {
  outline: 2px solid var(--error);
  outline-offset: 2px;
}
.btn-danger:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
```

### Cards

```css
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  transition: border-color 0.15s ease;
}
.card:hover {
  border-color: var(--border-hover);
}
.card:focus-within {
  border-color: var(--border-active);
}

/* Stat Card (仪表盘数字卡片) */
.card-stat {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  transition: border-color 0.15s ease;
}
.card-stat:hover {
  border-color: var(--border-hover);
}
.card-stat .card-stat__value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.02em;
}
.card-stat .card-stat__label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-tertiary);
  letter-spacing: 0.02em;
  margin-top: 4px;
}
.card-stat .card-stat__icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### Navigation (Top Bar)

```css
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  padding: 12px 24px;
}
.navbar__inner {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 12px;
}
.navbar__link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-tertiary);
  transition: all 0.15s ease;
  text-decoration: none;
}
.navbar__link:hover {
  color: var(--text-secondary);
  background: var(--surface);
}
.navbar__link--active {
  color: var(--accent);
  background: var(--accent-subtle);
}

/* Logo */
.navbar__logo {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--accent), var(--accent-secondary));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}
```

### Form Inputs

```css
.input {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 14px;
  color: var(--text);
  transition: all 0.15s ease;
  width: 100%;
}
.input::placeholder {
  color: var(--text-tertiary);
}
.input:hover {
  border-color: var(--border-hover);
}
.input:focus {
  outline: none;
  border-color: var(--border-active);
  box-shadow: 0 0 0 3px var(--accent-subtle);
}
.input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### Links

```css
.link {
  color: var(--accent);
  text-decoration: none;
  transition: color 0.15s ease;
}
.link:hover {
  color: var(--accent-hover);
  text-decoration: underline;
  text-underline-offset: 3px;
}
.link:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
  border-radius: 2px;
}
```

### Tags / Badges

```css
/* 基础标签 */
.tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.4;
}

/* 语义变体 */
.tag--default {
  background: var(--surface-alt);
  color: var(--text-secondary);
  border: 1px solid var(--border);
}
.tag--success {
  background: var(--success-subtle);
  color: var(--success);
}
.tag--error {
  background: var(--error-subtle);
  color: var(--error);
}
.tag--warning {
  background: var(--warning-subtle);
  color: var(--warning);
}
.tag--info {
  background: var(--accent-subtle);
  color: var(--accent);
}
.tag--purple {
  background: var(--accent-secondary-subtle);
  color: var(--accent-secondary);
}
```

### Table

```css
.table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}
.table th {
  background: var(--bg-elevated);
  color: var(--text-tertiary);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 10px 16px;
  text-align: left;
  border-bottom: 1px solid var(--border);
}
.table td {
  padding: 12px 16px;
  font-size: 14px;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border);
}
.table tr:hover td {
  background: var(--surface-hover);
}
```

### Modal / Dialog

```css
.modal-overlay {
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
}
.modal-content {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  max-width: 520px;
  width: 90%;
}
.modal-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 16px;
}
```

### Progress Bar

```css
.progress-bar {
  height: 6px;
  background: var(--surface-alt);
  border-radius: 3px;
  overflow: hidden;
}
.progress-bar__fill {
  height: 100%;
  background: var(--accent);
  border-radius: 3px;
  transition: width 0.3s ease;
}
```

### Avatar

```css
.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent-secondary));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 13px;
  font-weight: 600;
}
```

### Exam Option Card (答题选项卡片)

```css
.option-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px 16px;
  cursor: pointer;
  transition: all 0.15s ease;
  display: flex;
  align-items: center;
  gap: 12px;
}
.option-card:hover {
  border-color: var(--border-hover);
  background: var(--surface-hover);
}
.option-card--selected {
  border-color: var(--accent);
  background: var(--accent-subtle);
}
.option-card--correct {
  border-color: var(--success);
  background: var(--success-subtle);
}
.option-card--wrong {
  border-color: var(--error);
  background: var(--error-subtle);
}
.option-card:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.option-card__label {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: var(--surface-alt);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  flex-shrink: 0;
}
.option-card--selected .option-card__label {
  background: var(--accent);
  color: var(--text-inverse);
}
```

## 5. Layout Principles

**Container:**
- Max width: 1280px (`max-w-7xl` in Tailwind)
- Padding: 24px (horizontal)
- Narrow variant (form/detail): 720px

**Spacing Scale:**
- Section padding: 32px (`space-y-8`)
- Component gap: 16px (`gap-4`)
- Card internal padding: 20px (`p-5`)
- Tight card padding: 16px (`p-4`)
- Micro spacing: 8px (`gap-2`)

**Grid:**
```css
/* Stats grid (Dashboard) */
.grid-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

/* Content grid (2/3 + 1/3) */
.grid-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

/* Form grid */
.grid-form {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

/* Exam options */
.grid-options {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}
```

**Page Structure:**
```
┌─────────────────────────────────────────────┐
│  Navbar (fixed, h=56px, bg-elevated)        │
├─────────────────────────────────────────────┤
│                                             │
│  Content (pt=80px, max-w=1280px, centered)  │
│    ┌─────────────────────────────────────┐   │
│    │  Page Title + Actions (flex between)│   │
│    ├─────────────────────────────────────┤   │
│    │  Main Content Area                  │   │
│    │  (cards, tables, forms...)          │   │
│    └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

## 6. Depth & Elevation

| Level | Treatment | Use |
|-------|-----------|-----|
| Flat | 无阴影，仅 `border: 1px solid var(--border)` | 默认卡片、输入框、标签 |
| Subtle | `box-shadow: 0 1px 3px rgba(0,0,0,0.3)` | hover 态卡片 |
| Elevated | `box-shadow: 0 4px 12px rgba(0,0,0,0.4)` | 下拉菜单、tooltip |
| Overlay | `box-shadow: 0 8px 24px rgba(0,0,0,0.5)` + `backdrop-filter: blur(4px)` | Modal、弹窗 |
| Glow | `box-shadow: 0 0 0 3px var(--accent-subtle)` | Focus ring |

**Depth Rules:**
- 暗色主题下阴影效果微弱，主要靠边框和背景色差区分层级
- `backdrop-filter: blur()` 仅用在 modal overlay，值 <= 4px，面积越大值越小
- 禁止大面积 `backdrop-filter: blur()` (性能)
- 导航栏不用 blur，用实色 `--bg-elevated` + 底边框

## 7. Animation & Interaction

**Motion Philosophy**: 克制精确，只用 opacity 和 transform，服务于功能反馈，不做装饰。
**Tier**: L1 精致静态

### Base Easing
```css
:root {
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --duration-fast: 0.1s;
  --duration-normal: 0.15s;
  --duration-slow: 0.2s;
}
```

### Entrance Animation
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-in {
  animation: fadeIn 0.2s var(--ease-out) both;
}
```

### Vue Route Transition
```css
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s var(--ease-default);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
```

### Hover & Focus States
```css
/* 所有可交互元素的基础过渡 */
button, a, input, select, textarea, [role="button"] {
  transition: all var(--duration-normal) var(--ease-default);
}

/* 按钮 hover: 颜色变化即可，不做 lift */
/* 卡片 hover: 边框加亮 */
/* 输入框 focus: border-active + glow ring */
/* 表格行 hover: 背景色变 */
```

### Loading States
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
.skeleton {
  background: var(--surface-alt);
  border-radius: 8px;
  animation: pulse 1.5s var(--ease-default) infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
```

### Number Transition (Dashboard KPI)
```css
.number-transition {
  transition: all 0.3s var(--ease-out);
  font-variant-numeric: tabular-nums;
}
```

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## 8. Do's and Don'ts

### Do
- 用 CSS 变量引用所有颜色，保持全局一致
- 用边框和背景色差区分层级（暗色主题阴影效果弱）
- 保持信息密度——后台应用效率优先
- 表单元素提供清晰的 focus 态（glow ring）
- 数字使用 `font-variant-numeric: tabular-nums` 保持等宽对齐
- 中文内容确保行高 >= 1.6
- 状态反馈用语义色（success/error/warning），不用于装饰
- 图标保持 16-20px 统一尺寸，与文字对齐

### Don't
- ❌ 不用渐变背景做页面底色（保持纯色 `--bg`）
- ❌ 不用 glassmorphism / 大面积 blur（性能差且与克制风格冲突）
- ❌ 不用 glow / neon 效果（不是赛博风格）
- ❌ 不用 scroll reveal 动画（后台信息需要立即可见）
- ❌ 不用纯色块占位图（用真实图标或 Unsplash）
- ❌ 不在卡片 hover 时做 lift/scale（影响信息密度，仅改边框色）
- ❌ 不用 Emoji 作为功能图标（用 Lucide 图标库）
- ❌ 不超过三种文字颜色层级（text/text-secondary/text-tertiary）
- ❌ 不在暗色背景上用低对比度文字（最低对比度 4.5:1）
- ❌ 不用圆角 > 16px（克制风格，保持 8-12px）
- ❌ 不在同一视觉区域混用蓝色和紫色强调色

## 9. Responsive Behavior

**Breakpoints:**
| Name | Width | Key Changes |
|------|-------|-------------|
| Desktop | > 1024px | 4列统计网格，2/3+1/3内容布局，导航全部展开 |
| Tablet | 768px-1024px | 2列统计网格，单列内容，导航仅图标 |
| Mobile | < 768px | 单列统计，单列内容，导航仅图标无文字，表格横向滚动 |

**Touch Targets:** minimum 44x44px

**Collapsing Strategy:**
- 导航链接文字在 < 1024px 隐藏，仅保留图标
- 统计网格从 4 列 → 2 列 → 1 列
- 内容布局从 2/3+1/3 → 堆叠单列
- 表格允许横向滚动（`overflow-x: auto`）
- 弹窗从 520px 固定宽 → 全屏底部弹出

```css
/* Stats grid responsive */
.grid-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
@media (max-width: 1024px) {
  .grid-stats { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .grid-stats { grid-template-columns: 1fr; }
}

/* Content grid responsive */
.grid-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}
@media (max-width: 1024px) {
  .grid-content { grid-template-columns: 1fr; }
}

/* Nav text visibility */
@media (max-width: 1024px) {
  .navbar__link span { display: none; }
}

/* Table scroll */
@media (max-width: 768px) {
  .table-container { overflow-x: auto; -webkit-overflow-scrolling: touch; }
}

/* Modal mobile */
@media (max-width: 768px) {
  .modal-content {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    max-width: 100%;
    border-radius: 16px 16px 0 0;
    max-height: 85vh;
    overflow-y: auto;
  }
}
```

---

## Naive UI Theme Overrides (Vue specific)

由于项目使用 Naive UI 组件库，需在 `App.vue` 配置暗色主题：

```typescript
import { darkTheme } from 'naive-ui'
import type { GlobalThemeOverrides } from 'naive-ui'

const themeOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: '#58A6FF',
    primaryColorHover: '#79C0FF',
    primaryColorPressed: '#388BFD',
    primaryColorSuppl: '#79C0FF',
    borderRadius: '8px',
    bodyColor: '#0D1117',
    cardColor: '#1C2128',
    modalColor: '#1C2128',
    popoverColor: '#1C2128',
    tableColor: '#0D1117',
    inputColor: '#1C2128',
    actionColor: '#21262D',
    tagColor: '#21262D',
    hoverColor: '#262C36',
    borderColor: '#30363D',
    dividerColor: '#30363D',
    textColorBase: '#E6EDF3',
    textColor1: '#E6EDF3',
    textColor2: '#9CA3AF',
    textColor3: '#6B7280',
    placeholderColor: '#6B7280',
    iconColor: '#6B7280',
    successColor: '#3FB950',
    errorColor: '#F85149',
    warningColor: '#D29922',
    infoColor: '#58A6FF',
  }
}
```

**关键：使用 `darkTheme` 作为基础主题**，再用 `themeOverrides` 覆盖细节。

## ECharts Theme (图表配色)

```typescript
const echartsTheme = {
  backgroundColor: 'transparent',
  textStyle: { color: '#9CA3AF' },
  title: { textStyle: { color: '#E6EDF3' } },
  legend: { textStyle: { color: '#9CA3AF' } },
  xAxis: {
    axisLine: { lineStyle: { color: '#30363D' } },
    axisLabel: { color: '#6B7280' },
    splitLine: { lineStyle: { color: '#21262D' } },
  },
  yAxis: {
    axisLine: { lineStyle: { color: '#30363D' } },
    axisLabel: { color: '#6B7280' },
    splitLine: { lineStyle: { color: '#21262D' } },
  },
  series: {
    line: { itemStyle: { color: '#58A6FF' }, areaStyle: { color: 'rgba(88,166,255,0.08)' } },
    pie: { color: ['#58A6FF', '#A78BFA', '#3FB950', '#D29922'] },
  }
}
```
