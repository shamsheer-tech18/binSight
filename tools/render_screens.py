import asyncio
from playwright.async_api import async_playwright
import pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
SITE=(ROOT/'prototype').as_uri()+'/'
OUT=str(ROOT/'docs'/'screens')+'/'

async def setsel(page, sel, val):
    await page.evaluate("([s,v])=>{const e=document.querySelector(s); e.value=v; e.dispatchEvent(new Event('change',{bubbles:true}));}", [sel, val])

async def shot(page, name, kind='page'):
    await page.wait_for_timeout(150)
    if kind == 'page':
        h = await page.evaluate("()=>{const m=document.querySelector('main'); const r=m.getBoundingClientRect(); return Math.ceil(r.bottom+window.scrollY)}")
        await page.screenshot(path=OUT+name+'.png', clip={'x':0,'y':0,'width':1280,'height':max(h,500)}, full_page=True)
    else:
        el = await page.query_selector('#dc-root > div')
        await el.screenshot(path=OUT+name+'.png')

async def load(page, f):
    await page.goto(SITE+f)
    await page.wait_for_function('window.__dcReady === true')

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--no-sandbox'])
        ctx = await b.new_context(viewport={'width':1280,'height':800}, device_scale_factor=2)
        await ctx.route('**/*', lambda r: r.abort() if r.request.url.startswith('http') else r.continue_())
        page = await ctx.new_page()
        errs=[]; page.on('pageerror', lambda e: errs.append(str(e)))
        await load(page,'Main.dc.html'); await shot(page,'01_overview')
        await page.get_by_role('button', name='Sun Nov 15').click(); await shot(page,'02_overview_picker')
        await load(page,'StationDetail.dc.html'); await shot(page,'03_station_a')
        await load(page,'Recommendation.dc.html'); await shot(page,'04_rec')
        await page.get_by_role('button', name='I disagree, choose another option').click(); await shot(page,'05_rec_disagree')
        await load(page,'Recommendation.dc.html'); await page.get_by_role('button', name="This can't be done").click(); await shot(page,'06_rec_cant')
        await load(page,'LogChange.dc.html'); await shot(page,'07_log_form')
        await setsel(page,'#dt','2026-11-30'); await page.get_by_role('button', name='Log change').click(); await shot(page,'08_log_error')
        await load(page,'LogChange.dc.html'); await setsel(page,'#st','C'); await page.get_by_role('button', name='Log change').click(); await shot(page,'09_log_warn')
        await load(page,'LogChange.dc.html'); await page.get_by_role('button', name='Log change').click(); await shot(page,'10_log_done')
        await load(page,'ResultImproved.dc.html'); await shot(page,'11_result_c')
        await load(page,'Summary.dc.html'); await shot(page,'12_summary')
        await page.get_by_role('button', name='Request cost data').click(); await shot(page,'13_summary_req')
        await load(page,'LowConfidence.dc.html'); await shot(page,'14_lowconf')
        await page.get_by_role('button', name='Request a quick audit check').click(); await shot(page,'15_lowconf_req')
        await load(page,'Offline.dc.html'); await shot(page,'16_offline')
        await load(page,'ResultNoChange.dc.html'); await shot(page,'17_result_b')
        await load(page,'InstallCheck.dc.html'); await shot(page,'18_install_fault')
        await page.get_by_role('button', name='I adjusted it · re-test').click(); await page.get_by_role('button', name='Send to privacy office').click(); await shot(page,'19_install_pass')
        await load(page,'HardwareModule.dc.html'); await shot(page,'20_hardware','el')
        await load(page,'StationNotice.dc.html'); await shot(page,'21_notice','el')
        print('errors:', errs)
        await b.close()
asyncio.run(main())
