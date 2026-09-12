# Zaitoon Studio — Official Public Website & TikTok Review Hub

This repository contains the public-facing static landing site, Terms of Service, Privacy Policy, and TikTok App Review demonstration documentation for **Zaitoon Studio** (TikTok App ID `7684433488619276306`).

---

## 1. Directory Structure

```
zaitoon-studio-website/
├── index.html            # Main product overview & creator review workflow
├── privacy.html          # Official Privacy Policy (clean URL: /privacy)
├── privacy/
│   └── index.html        # Directory index fallback for /privacy
├── terms.html            # Official Terms of Service (clean URL: /terms)
├── terms/
│   └── index.html        # Directory index fallback for /terms
├── review.html           # Official TikTok App Reviewer Guide & Demo Walkthrough
├── review/
│   └── index.html        # Directory index fallback for /review
├── css/
│   └── style.css         # Dark/light responsive studio styling
├── js/
│   └── main.js           # Responsive navigation & interaction handlers
├── assets/
│   └── zaitoon_studio_app_icon_1024.png # 1024×1024 brand mark
├── vercel.json           # Vercel deployment configuration with clean URLs
├── _headers              # Cloudflare Pages security & cache headers
└── _routes.json          # Cloudflare Pages routing rules
```

---

## 2. Zero-Cost, No-Credit-Card Deployment Guide

You can deploy this site in under 2 minutes completely free on either **Cloudflare Pages** or **Vercel**. Neither service requires a credit card.

### Option A: Cloudflare Pages (Recommended — Unlimited Bandwidth & Free SSL)
1. **Push to GitHub**:
   Create a new GitHub repository (e.g., `https://github.com/Refayatul/zaitoon-studio-site` or `zaitoon-studio-website`) and push this folder.
2. **Open Cloudflare Dashboard**:
   Go to [dash.cloudflare.com](https://dash.cloudflare.com) (sign up for free with your email if you haven't already).
3. **Connect GitHub**:
   - Go to **Workers & Pages** → **Create Application** → **Pages** tab → **Connect to Git**.
   - Select your GitHub account and choose `zaitoon-studio-website`.
4. **Configure Build Settings**:
   - **Project name**: `zaitoon-studio`
   - **Production branch**: `main` (or `dev`)
   - **Framework preset**: `None`
   - **Build command**: *(Leave blank)*
   - **Build output directory**: `.` (or `/`)
5. **Click Save and Deploy**:
   - Cloudflare will deploy the site in ~10 seconds.
   - You will receive an instant public URL:
     **`https://zaitoon-studio.pages.dev`**

---

### Option B: Vercel (Alternative Free Tier)
1. **Open Vercel Dashboard**:
   Go to [vercel.com](https://vercel.com) and log in with your GitHub account.
2. **Import Project**:
   - Click **Add New...** → **Project**.
   - Import your `zaitoon-studio-website` repository.
3. **Configure Settings**:
   - **Framework Preset**: `Other`
   - **Root Directory**: `./`
   - **Build & Output Settings**: Default (no build command needed).
4. **Click Deploy**:
   - Vercel deploys immediately.
   - You will receive an instant public URL:
     **`https://zaitoon-studio.vercel.app`**

---

## 3. TikTok Developer Portal URL Mapping

Once deployed to Cloudflare Pages (e.g. `zaitoon-studio.pages.dev`), fill the pending fields in the [TikTok Developer Portal](https://developers.tiktok.com/app/7684433488619276306/pending):

| Field in TikTok Portal | Value to Enter |
| :--- | :--- |
| **Website URL** | `https://zaitoon-studio.pages.dev/` |
| **Terms of Service URL** | `https://zaitoon-studio.pages.dev/terms` |
| **Privacy Policy URL** | `https://zaitoon-studio.pages.dev/privacy` |
| **App Review Demo** | `https://zaitoon-studio.pages.dev/review` |

---

## 4. Local Testing & Verification

To preview the website locally before deploying:
```bash
python3 -m http.server 8000
```
Open `http://127.0.0.1:8000` in your web browser.
