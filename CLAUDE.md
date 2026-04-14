# CLAUDE.md — AI Automation Playwright Project Guide

## Project Overview

This repo is a **Playwright UI automation testing practice app** based on the [Bondar Academy](https://www.bondaracademy.com) "Playwright UI Testing Mastery" course.

- **App Under Test (AUT):** Angular 14 admin dashboard (`ngx-admin`) running at `http://localhost:4200`
- **Purpose:** Provides a rich, realistic UI for writing E2E tests — forms, modals, tables, charts, authentication flows
- **Origin:** Forked from https://github.com/Bondar-Academy/playwright-practice-app.git

---

## Repository Layout

```
AI_Automation _playwright/
├── backend/                  # Angular application (the AUT)
│   ├── src/app/
│   │   ├── @core/            # Core module: services, mock data, utilities
│   │   ├── @theme/           # Theme module: layouts, header, footer, styles
│   │   └── pages/            # Feature pages (dashboard, forms, tables, charts...)
│   ├── angular.json          # Angular CLI config (build, serve, lint, e2e)
│   ├── package.json          # Dependencies and npm scripts
│   └── tsconfig.json         # TypeScript config (es2020 target)
├── CLAUDE.md                 # This file
└── README.md
```

> Note the directory name has a space: `AI_Automation _playwright`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Angular 14 (TypeScript ~4.6.4) |
| UI Library | Nebular 10 (theme, auth, security, eva-icons) |
| CSS | SCSS + Bootstrap 4.3.1 |
| Charts | ECharts 4.x via ngx-echarts |
| Tables | ng2-smart-table |
| Maps | Leaflet via @asymmetrik/ngx-leaflet |
| Reactive | RxJS 6.6.2 |
| Unit Tests | Karma + Jasmine |
| E2E (legacy) | Protractor (configured but outdated) |
| Component prefix | `ngx-` |

---

## Running the App

```bash
cd backend
npm install --force    # --force required for peer dependency conflicts
npm start              # Serves at http://localhost:4200
```

Production build: `ng build --configuration production` → output in `dist/`

---

## Application Pages & Routes

| Route | Page | Key Testable Elements |
|---|---|---|
| `/pages/iot-dashboard` | IoT Dashboard (default) | Status cards, solar data, room controls, media player |
| `/pages/forms/layouts` | Form Layouts | Text inputs, checkboxes, radio buttons, selects |
| `/pages/forms/datepicker` | Datepicker | Calendar widget, date input |
| `/pages/modal-overlays/dialog` | Dialogs | Modal open/close, confirm/cancel |
| `/pages/modal-overlays/window` | Windows | Draggable overlays |
| `/pages/modal-overlays/popover` | Popovers | Popover triggers and content |
| `/pages/modal-overlays/toastr` | Toastr | Success/error/warning toast notifications |
| `/pages/modal-overlays/tooltip` | Tooltips | Hover tooltip behavior |
| `/pages/extra-components/calendar` | Calendar | Full calendar navigation |
| `/pages/charts/echarts` | ECharts | Area, bar, line, pie, radar charts |
| `/pages/tables/smart-table` | Smart Table | Sort, filter, paginate, inline edit |
| `/pages/tables/tree-grid` | Tree Grid | Hierarchical row expansion |
| `/auth/login` | Login | Credential form, submit, error handling |
| `/auth/register` | Register | Registration form |
| `/auth/request-password` | Request Password | Password recovery form |
| `/auth/reset-password` | Reset Password | Password reset form |

---

## Architecture Notes

- **Lazy Loading:** All feature modules (forms, charts, tables, etc.) are lazy-loaded.
- **Mock Data:** All data comes from mock services in `@core/mock/`. No real backend — easy to test predictable states.
- **Theme System:** 4 switchable themes (Default, Cosmic, Corporate, Dark) via `NbThemeService`. Tests may need to account for active theme when matching styles.
- **Auth:** Uses Nebular `NbDummyAuthStrategy` — any credentials work; no real auth backend.
- **RBAC:** NbSecurityModule with guest role. Access control lists defined for create/edit/remove.
- **Layouts:** 3 layout templates (`one-column`, `two-columns`, `three-columns`).
- **Lifecycle Pattern:** Components use `alive: boolean` flag + `takeWhile(() => this.alive)` for subscription teardown.

---

## Core Data Services (in @core/mock/)

There are 19 mock data providers. Key ones relevant to testing:

- `SmartTableData` → powers the Smart Table page
- `UserData` → user info throughout the app
- `SolarData` / `ElectricityData` → dashboard widgets
- `SecurityCamerasData` → camera feed widget
- `TemperatureHumidityData` → temperature control widget

---

## Key Files

| File | Why it matters |
|---|---|
| `backend/src/app/app-routing.module.ts` | Top-level routes |
| `backend/src/app/pages/pages-menu.ts` | Sidebar navigation structure |
| `backend/src/app/@core/core.module.ts` | All service providers registered here |
| `backend/src/app/@theme/theme.module.ts` | Theme config + layout declarations |
| `backend/angular.json` | Build config, global styles/scripts |

---

## Common Enhancements & Where to Make Them

| Task | Where to look |
|---|---|
| Add a new page/route | `pages/` + `app-routing.module.ts` + `pages-menu.ts` |
| Add new mock data | `@core/data/` (interface) + `@core/mock/` (implementation) + `core.module.ts` |
| Change navigation menu | `pages/pages-menu.ts` |
| Modify themes | `@theme/styles/` + `theme.module.ts` |
| Add chart type | `pages/charts/` + register in `ChartsModule` |
| Add table feature | `pages/tables/` + `ng2-smart-table` config |
| Add form | `pages/forms/` + register in `FormsModule` |
| Add modal/overlay | `pages/modal-overlays/` + register in `ModalOverlaysModule` |

---

## Gotchas

- Install with `--force` due to peer dependency conflicts between Angular 14 and some packages.
- The project folder has a trailing space in its name (`AI_Automation _playwright`) — quote paths when using shell commands.
- "playwright" in the project name refers to the testing course, not a Playwright test suite in this repo. Actual Playwright test files may live elsewhere or need to be created.
- ECharts is v4 (not v5); API differs from current ECharts docs.
- `tslint` is used (not `eslint`) — this is an older Angular 14 project.
