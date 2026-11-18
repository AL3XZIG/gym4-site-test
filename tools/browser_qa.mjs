#!/usr/bin/env node
import { spawn } from "node:child_process";
import process from "node:process";
import { setTimeout as delay } from "node:timers/promises";
import { chromium } from "playwright";
import AxeBuilder from "@axe-core/playwright";

const routes = ["index.html","404.html","history.html","sveden.html","parents.html","students.html","news.html","news-editor.html","priem.html","contacts.html","school-life.html","election.html","admin.html"];
const widths = [320,360,390,768,1280,1440,1920];
const baseURL = process.env.BASE_URL || "http://127.0.0.1:4173";
const failures = [], warnings = [];
let server, browser;
const counts = { pages: 0, viewportChecks: 0, axePages: 0 };
const fail = (where, why) => failures.push("FAIL " + where + ": " + why);
const warn = (where, why) => warnings.push("WARN " + where + ": " + why);

async function waitForServer() {
  for (let i=0;i<40;i++) {
    try { const r=await fetch(baseURL); if (r.ok) return; } catch {}
    await delay(250);
  }
  throw new Error("Local HTTP server did not start: " + baseURL);
}
async function main() {
  if (!process.env.BASE_URL) {
    server = spawn("python3",["-m","http.server","4173","--bind","127.0.0.1"],{stdio:"ignore"});
    server.on("error",e=>fail("server",e.message));
  }
  await waitForServer();
  browser = await chromium.launch({headless:true});

  for (const route of routes) {
    for (const width of widths) {
      const page = await browser.newPage({viewport:{width,height:900},reducedMotion:"reduce"});
      const errors=[];
      page.on("pageerror",e=>errors.push(e.message));
      const response=await page.goto(baseURL+"/"+route,{waitUntil:"networkidle"});
      const label=route+" @ "+width+"px";
      if (!response || !response.ok()) fail(label,"HTTP "+(response ? response.status() : "no response"));
      else {
        const s=await page.evaluate(()=>({
          title:document.title.trim(),h1:document.querySelectorAll("h1").length,
          main:document.querySelectorAll("main").length,lang:document.documentElement.lang,
          viewport:!!document.querySelector('meta[name="viewport"]'),
          skip:!!document.querySelector("a.skip-link"),
          client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth
        }));
        if (!s.title) fail(label,"empty document title");
        if (s.h1!==1) fail(label,"expected one h1, found "+s.h1);
        if (s.main!==1) fail(label,"expected one main, found "+s.main);
        if (s.lang!=="ru") fail(label,"unexpected document language: "+s.lang);
        if (!s.viewport) fail(label,"missing viewport meta");
        if (!s.skip) fail(label,"missing skip link");
        if (s.scroll>s.client+1) fail(label,"horizontal overflow: "+s.scroll+" > "+s.client);
        for (const e of errors) fail(label,"uncaught JavaScript exception: "+e);
      }
      counts.viewportChecks++;
      await page.close();
    }
    counts.pages++;
  }

  const page=await browser.newPage({viewport:{width:390,height:844},reducedMotion:"reduce"});
  await page.goto(baseURL+"/index.html",{waitUntil:"networkidle"});
  const menu=page.locator("#menuToggle");
  if (await menu.count()) {
    await menu.click();
    if (await menu.getAttribute("aria-expanded")!=="true") fail("mobile menu","did not open");
    await page.keyboard.press("Escape");
    if (await menu.getAttribute("aria-expanded")!=="false") fail("mobile menu","Escape did not close");
  } else fail("mobile menu","toggle not found");

  const toggle=page.locator("#a11yToggle"), panel=page.locator("#a11yPanel");
  if (await toggle.count() && await panel.count()) {
    await toggle.click();
    if (await toggle.getAttribute("aria-expanded")!=="true") fail("a11y panel","did not open");
    await page.locator('[data-fs="200"]').click();
    const fs=await page.evaluate(()=>document.documentElement.dataset.fontScale);
    if (fs!=="200") fail("a11y panel","200 percent font size not applied");
    await page.locator('[data-motion="off"]').click();
    const motion=await page.evaluate(()=>document.documentElement.dataset.motion);
    if (motion!=="off") fail("a11y panel","motion setting not applied");
    await page.keyboard.press("Escape");
    if (await toggle.getAttribute("aria-expanded")!=="false") fail("a11y panel","Escape did not close");
  } else fail("a11y panel","shared controls not found");

  for (const route of routes) {
    const audit=await browser.newPage({viewport:{width:1365,height:900}});
    await audit.goto(baseURL+"/"+route,{waitUntil:"networkidle"});
    const result=await new AxeBuilder({page:audit}).withTags(["wcag2a","wcag2aa","wcag21a","wcag21aa"]).analyze();
    for (const v of result.violations) {
      const detail=v.id+" ("+v.impact+"): "+v.help+" ["+v.nodes.length+" node(s)]";
      if (v.impact==="critical") fail("axe "+route,detail); else warn("axe "+route,detail);
    }
    counts.axePages++;
    await audit.close();
  }
  await page.close();
  console.log(JSON.stringify(counts,null,2));
  warnings.forEach(console.warn); failures.forEach(console.error);
  if (failures.length) { console.error("Browser QA failed: "+failures.length+" blocking finding(s)."); process.exitCode=1; }
  else console.log("Browser QA passed with "+warnings.length+" non-blocking accessibility warning(s).");
}
try { await main(); } catch(e) { console.error(e); process.exitCode=1; }
finally { if(browser) await browser.close(); if(server) server.kill("SIGTERM"); }
