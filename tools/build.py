from PIL import Image
import html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape

def ratio(path):
    with Image.open(os.path.join(ROOT, path)) as im:
        return round(im.size[0] / im.size[1], 3)

def head(title, desc, prefix):
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%2316140f'/%3E%3Ctext x='32' y='43' font-family='Arial' font-weight='800' font-size='28' text-anchor='middle' fill='%23f4f1ea'%3EAM%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}css/style.css">
</head>
'''

def header(prefix, current, dark=False):
    def cur(n): return ' aria-current="page"' if n == current else ''
    return f'''<header class="site-header{' on-dark' if dark else ''}">
  <div class="wrap">
    <a class="brand" href="{prefix}index.html">Anthony Madrigal</a>
    <nav class="nav" aria-label="Main">
      <a href="{prefix}index.html#projects"{cur('projects')}>Projects</a>
      <a href="{prefix}index.html#experience">Experience</a>
      <a href="{prefix}index.html#contact">Contact</a>
    </nav>
  </div>
</header>
'''

def contact(prefix):
    return f'''<footer class="contact" id="contact">
  <div class="wrap">
    <p class="mono" style="color:var(--on-dark-2)">Contact</p>
    <h2 class="reveal">Let's build<br>something <em>real.</em></h2>
    <p class="lede reveal">Questions about a project, internships, or anything else — I'd love to hear from you.</p>
    <div class="links reveal">
      <a class="btn" href="mailto:anthony.madrigal@usc.edu">anthony.madrigal@usc.edu <span class="arrow">→</span></a>
      <a class="btn ghost" href="https://www.linkedin.com/in/madrigalanthony" target="_blank" rel="noopener">LinkedIn ↗</a>
    </div>
    <div class="foot mono">
      <span>© <span id="yr">2026</span> Anthony Madrigal</span>
      <a href="#top" style="text-decoration:none">Back to top ↑</a>
    </div>
  </div>
</footer>
<script>document.getElementById('yr').textContent = new Date().getFullYear();</script>
<script src="{prefix}js/main.js"></script>
</body>
</html>
'''

def gallery(items, prefix, cls=''):
    if len(items) == 1: cls += ' single'
    out = [f'<div class="gallery {cls} reveal">']
    for path, cap in items:
        r = ratio(path)
        out.append(f'  <figure style="--r:{r}"><img src="{prefix}{path}" alt="{E(cap)}" loading="lazy" decoding="async"><figcaption>{E(cap)}</figcaption></figure>')
    out.append('</div>')
    return '\n'.join(out)

# ---------------------------------------------------------------------------
# Projects data
# ---------------------------------------------------------------------------
PROJECTS = [
    dict(slug='dr-pepper-can', title='Automated Dr. Pepper Can', short='43" Self-Opening Soda Can',
         cover='images/can/final.jpg',
         blurb='A 43-inch tall, self-opening Dr. Pepper can — designed, wired, coded, fabricated and filmed in 20 days for a scholarship application.',
         tags=['SolidWorks', 'Arduino', '3D printing', 'Laser cutting']),
    dict(slug='filament-recycler', title='3D Print Filament Recycler', short='3D Print Recycler',
         cover='images/recycler/shredder-assembled.jpg',
         blurb='The project that started it all: a machine to recycle failed 3D prints, designed from scratch and now carried on by the STEMbassadors makerspace.',
         tags=['SolidWorks', 'Fiber laser', 'Design for manufacturing']),
    dict(slug='nerf-turret', title='Arduino Nerf Turret', short='Arduino Nerf Turret',
         cover='images/turret/turret.jpg',
         blurb='A high school build: a Bluetooth Nerf turret, aimed and fired from a phone app I made in MIT App Inventor.',
         tags=['Arduino', 'Bluetooth', 'MIT App Inventor', 'Prototyping']),
]

# ---------------------------------------------------------------------------
# Home page
# ---------------------------------------------------------------------------
def build_home():
    p = ''
    can, rec, tur = PROJECTS
    rows = []
    for i, pr in enumerate(PROJECTS[1:], start=2):
        chips = ''.join(f'<span class="chip">{E(t)}</span>' for t in pr['tags'])
        rows.append(f'''      <a class="project-row reveal" href="projects/{pr['slug']}.html">
        <span class="num mono">0{i}</span>
        <div>
          <h3>{E(pr['title'])}</h3>
          <p>{E(pr['blurb'])}</p>
          <div class="chip-list">{chips}</div>
        </div>
        <div class="thumb"><img src="{pr['cover']}" alt="{E(pr['title'])}" loading="lazy"></div>
      </a>''')
    logos = [(None, 'Deepshard Inc.'), ('idea-center', 'IDEA Center'), ('evolvent-design', 'Evolvent Design'), ('navfac-exwc', 'NAVFAC EXWC'),
             ('usc-arc', 'USC ARC'), ('terra-labs', 'Terra Labs'), ('usc', 'USC'),
             ('oxnard-college', 'Oxnard College'), ('namru-sa', 'NAMRU San Antonio')]
    # f=None means no logo file yet: show the name as a plain wordmark instead
    logo_html = '\n'.join(
        (f'        <figure><img src="images/logos/{f}.png" alt="{E(n)} logo" loading="lazy"><figcaption class="mono">{E(n)}</figcaption></figure>' if f else
         f'        <figure><span class="wordmark">{E(n.replace(" Inc.", ""))}</span><figcaption class="mono">{E(n)}</figcaption></figure>')
        for f, n in logos)

    page = head('Anthony Madrigal — Engineering Portfolio',
                'Engineering student at USC. Projects in mechanical design, electronics and rapid prototyping.', p)
    page += '<body id="top">\n' + header(p, 'home') + f'''
<main>
  <section class="home-hero">
    <div class="wrap">
      <div>
        <p class="kicker mono reveal">Engineering student · USC</p>
        <h1 class="reveal">Anthony<span>Madrigal</span></h1>
        <p class="lede reveal">I design, build and code physical things — from CAD to the final bolt. Each project here is told as a story: the idea, the build, and what came out the other side.</p>
        <div class="actions reveal">
          <a class="btn" href="#projects">See the projects <span class="arrow">↓</span></a>
          <a class="btn ghost" href="#contact">Get in touch</a>
        </div>
      </div>
      <div class="hero-stack reveal">
        <figure class="a"><img src="images/home/workbench.jpg" alt="Workbench covered in wires, Arduino boards and tools"></figure>
        <figure class="b"><img src="images/can/final.jpg" alt="The finished 43-inch Dr. Pepper can"><span class="tag mono">43" tall</span></figure>
      </div>
    </div>
    <div class="scroll-cue mono">Scroll</div>
  </section>

  <section class="section" id="projects" style="padding-top:2rem">
    <div class="wrap">
      <div class="section-head reveal">
        <h2>Projects</h2>
        <span class="mono">{len(PROJECTS)} builds · newest first</span>
      </div>

      <a class="featured reveal" href="projects/{can['slug']}.html">
        <div class="media"><img src="images/can/hero.jpg" alt="The finished Dr. Pepper can in the makerspace"></div>
        <div class="body">
          <div>
            <p class="label mono">01 · Featured build</p>
            <h3>{E(can['title'])}</h3>
            <p>{E(can['blurb'])}</p>
          </div>
          <div>
            <div class="stats">
              <div><b>43"</b><span>tall</span></div>
              <div><b>20</b><span>days, start to finish</span></div>
              <div><b>9 V</b><span>single power supply</span></div>
            </div>
            <p class="go" style="margin:2rem 0 0;color:var(--on-dark)">Read the story <span class="arrow">→</span></p>
          </div>
        </div>
      </a>

      <div style="margin-top:2rem">
{chr(10).join(rows)}
      </div>
    </div>
  </section>

  <section class="band" aria-label="Workbench">
    <img src="images/home/workbench.jpg" alt="" loading="lazy">
    <div class="wrap"><blockquote class="reveal">Years in a makerspace taught me one thing: the fastest way to learn is to build it.</blockquote></div>
  </section>

  <section class="section" id="experience">
    <div class="wrap">
      <div class="section-head reveal">
        <h2>Where I've learned &amp; worked</h2>
        <span class="mono">Schools · labs · teams</span>
      </div>
      <div class="logos reveal">
{logo_html}
      </div>
    </div>
  </section>
</main>
''' + contact(p)
    open(f'{ROOT}/index.html', 'w').write(page)

# ---------------------------------------------------------------------------
# Project page template
# ---------------------------------------------------------------------------
def build_project(pr, hero_img, lede, stats, chapters, finale, nxt):
    p = '../'
    rail = '\n'.join(f'        <li><a href="#{c["id"]}"><small>{i:02d}</small>{E(c["nav"])}</a></li>' for i, c in enumerate(chapters, 1))
    stat_html = ''.join(f'<div><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in stats)
    body = '\n'.join(c['html'] for c in chapters)
    fin = ''
    if finale:
        fin = f'''
      <section class="finale reveal" aria-label="Final result">
        <img src="{p}{finale['img']}" alt="{E(finale['alt'])}" loading="lazy">
        <div class="body">
          <p class="mono" style="color:var(--accent-2)">The result</p>
          <h2>{E(finale['title'])}</h2>
          <p>{finale['text']}</p>
        </div>
      </section>'''
    page = head(f"{pr['title']} — Anthony Madrigal", pr['blurb'], p)
    page += '<body id="top">\n' + header(p, 'projects', dark=True) + f'''
<main>
  <section class="p-hero">
    <div class="wrap">
      <div>
        <p class="crumbs mono reveal"><a href="{p}index.html#projects">← All projects</a></p>
        <h1 class="reveal">{E(pr['title'])}</h1>
        <p class="lede reveal">{lede}</p>
        <div class="stats reveal">{stat_html}</div>
      </div>
      <div class="media reveal"><img src="{p}{hero_img}" alt="{E(pr['title'])}"></div>
    </div>
    <div class="scroll-cue mono">The story</div>
  </section>

  <div class="wrap">
    <div class="story">
      <aside class="rail" aria-label="Chapters">
        <ol>
          <span class="progress" aria-hidden="true"></span>
{rail}
        </ol>
      </aside>
      <div>
{body}
{fin}
      </div>
    </div>

    <a class="next" href="{nxt['slug']}.html">
      <div><p class="mono">Next project</p><h3>{E(nxt['title'])}</h3></div>
      <span class="circle" aria-hidden="true">→</span>
    </a>
  </div>
</main>
''' + contact(p)
    os.makedirs(f'{ROOT}/projects', exist_ok=True)
    open(f'{ROOT}/projects/{pr["slug"]}.html', 'w').write(page)

def chapter(id, nav, eyebrow, title, inner):
    return dict(id=id, nav=nav, html=f'''        <section class="chapter" id="{id}">
          <p class="eyebrow mono reveal">{eyebrow}</p>
          <h2 class="reveal">{title}</h2>
{inner}
        </section>''')

P = '../'

# --- Dr Pepper can ---------------------------------------------------------
can_chapters = [
    chapter('why', 'The challenge', 'Chapter 01 — Why', 'A scholarship, a soda can, and 20 days.', f'''          <p class="text big reveal">As part of a scholarship application I made a 43-inch tall, self-opening Dr. Pepper can.</p>
          <div class="split" style="margin-top:2.5rem">
            <div class="text reveal">
              <p>Thanks to years I dedicated at a makerspace independently learning, rapidly prototyping and helping others start projects from scratch, I completed the project ideation, CAD, coding, wiring, fabrication, sourcing of materials and components, assembly and cosmetics — all within <strong>20 days</strong>.</p>
              <p>My initial idea was a fully refrigerated custom unit, but with 20 days on the line I had to make sure I had an MVP for my video — especially since you can't tell temperature from a video.</p>
            </div>
{gallery([('images/can/scale.jpg', 'For scale')], P)}
          </div>'''),
    chapter('how', 'How it works', 'Chapter 02 — How it works', 'Press the tab. The can does the rest.', f'''          <div class="split">
            <ol class="steps reveal">
              <li><div><b>Press the pull tab</b>Pressing the tab down clicks a limit switch, placed where a pushed-down tab would normally touch the lid.</div></li>
              <li><div><b>The servo opens the can</b>A servo mounted under the lid, with two arms linked to the opening tab, slowly pulls it open.</div></li>
              <li><div><b>The tab follows along</b>An elastic connector joins the pull tab to the opening tab, and the pull tab is hinged at the opening's edge — so it moves with it, just like a real can opening itself.</div></li>
              <li><div><b>The elevator rises</b>Once the servo reaches a set angle, an internal rack-and-pinion elevator driven by a DC motor lifts a can up and out of the opening.</div></li>
              <li><div><b>Reset</b>After a few seconds it lowers until it hits a second limit switch — only then does the servo return to its starting position.</div></li>
            </ol>
            <div class="sticky">
{gallery([('images/can/inside.jpg', 'Looking down into the mechanism')], P)}
            </div>
          </div>'''),
    chapter('video', 'The video', 'Chapter 03 — Video submission', 'See it in action.', f'''          <div class="video reveal">
            <button type="button" data-yt="c0I0LvTEppc" aria-label="Play the Dr. Pepper can video submission">
              <img src="{P}images/can/video-poster.jpg" alt="" loading="lazy">
              <span class="play" aria-hidden="true"></span>
            </button>
          </div>
          <p class="mono reveal" style="margin-top:1rem;color:var(--ink-3)"><a href="https://youtu.be/c0I0LvTEppc" target="_blank" rel="noopener">Watch on YouTube ↗</a></p>'''),
    chapter('planning', 'Planning & CAD', 'Chapter 04 — Planning', 'Measuring a real can, then modeling every part.', f'''          <div class="text reveal"><p>The first step was to take measurements from a real can and begin to model each part in SolidWorks — the lid and its mechanism, the shoulders, the laser-cut frame, and the brackets holding the motors.</p></div>
{gallery([('images/can/modeling.jpg', 'Modeling in SolidWorks'), ('images/can/cad-assembly.jpg', 'Frame assembly')], P)}
          <p class="gallery-label mono reveal">The lid</p>
{gallery([('images/can/cad-lid.jpg', 'Lid'), ('images/can/cad-lid-top.jpg', 'Lid, top'), ('images/can/cad-lid-opening.jpg', 'Lid opening'), ('images/can/cad-lid-underside.jpg', 'Lid underside mounts')], P, 'cad')}
          <p class="gallery-label mono reveal">Frame &amp; mechanism</p>
{gallery([('images/can/cad-frame.jpg', 'Frame'), ('images/can/cad-shoulder.jpg', 'Shoulder section'), ('images/can/cad-ring.jpg', 'Interlocking ring'), ('images/can/cad-rib.jpg', 'Rib'), ('images/can/cad-rod.jpg', 'Rod'), ('images/can/cad-servo-arm.jpg', 'Servo arm'), ('images/can/cad-bracket.jpg', 'Motor bracket')], P, 'cad')}'''),
    chapter('manufacturing', 'Manufacturing', 'Chapter 05 — Manufacturing', 'Print, putty, sand, paint. Repeat.', f'''          <div class="text reveal">
            <p>The complex geometry was 3D printed — namely the lid, shoulders and the bottom. To get rid of layer lines, red automotive putty was applied to the seams formed by gluing the printed parts together. The putty was then sanded down and sprayed with silver reflective spray paint.</p>
            <p>The frame of the can was made out of ¼" plywood that I cut on a CO₂ laser, with rings and ribs designed to interlock with each other.</p>
          </div>
          <p class="gallery-label mono reveal">The lid</p>
{gallery([('images/can/printed-parts.jpg', 'Printed parts'), ('images/can/putty.jpg', 'Automotive putty on the seams'), ('images/can/printed-lid.jpg', 'Printed lid'), ('images/can/painted-lid.jpg', 'Sanded and painted'), ('images/can/pull-tab.jpg', 'Pull tab'), ('images/can/lid-internals.jpg', 'Lid internals')], P)}
          <p class="gallery-label mono reveal">Finishing</p>
{gallery([('images/can/sanding-station.jpg', 'Outdoor sanding and painting station'), ('images/can/respirator.jpg', 'Suited up for spray paint')], P)}
          <p class="gallery-label mono reveal">The frame</p>
{gallery([('images/can/laser-ring.jpg', 'Laser-cut ring'), ('images/can/frame.jpg', 'Interlocking plywood frame'), ('images/can/frame-lid.jpg', 'Frame with lid'), ('images/can/frame-inside.jpg', 'Inside the frame'), ('images/can/wrapping-body.jpg', 'Fitting the sheet-metal body'), ('images/can/wrapped.jpg', 'Wrapping the body')], P)}'''),
    chapter('electronics', 'Electronics & code', 'Chapter 06 — Electronics, code & video', 'Built to survive a power cut.', f'''          <div class="split">
            <div class="text reveal">
              <p>The code was written so the entire system could be powered off at any point — it resets itself as soon as the Arduino receives power again.</p>
              <p>The outline of the video was written on a whiteboard the day of the shoot. The whole video was shot in one full day, and thanks to my friend Leo, editing took just one more.</p>
            </div>
            <div class="bom reveal" style="margin:0">
              <div><b>Arduino Uno</b><span>Controller</span></div>
              <div><b>L298N</b><span>Motor driver</span></div>
              <div><b>Buck converter</b><span>Power</span></div>
              <div><b>DC motor</b><span>Elevator</span></div>
              <div><b>Servo</b><span>Lid opener</span></div>
              <div><b>2× limit switch</b><span>Tab + home</span></div>
            </div>
          </div>
          <p class="mono reveal" style="color:var(--ink-3);margin-top:1rem">All powered from a single 9 V, 2.5 A supply.</p>
{gallery([('images/can/electronics.jpg', 'Electronics on the bench'), ('images/can/electronics-inside.jpg', 'Electronics mounted inside the can'), ('images/can/code.jpg', 'Arduino code'), ('images/can/whiteboard.jpg', 'Video outline on the whiteboard'), ('images/can/video-shoot.jpg', 'Shooting the video')], P)}'''),
]
build_project(PROJECTS[0], 'images/can/hero.jpg',
    'A 43-inch tall, self-opening soda can — from idea to finished video in 20 days.',
    [('43"', 'tall'), ('20', 'days'), ('9 V', 'single supply')], can_chapters,
    dict(img='images/can/final.jpg', alt='The finished Dr. Pepper can', title='Done in 20 days.',
         text='Ideation, CAD, coding, wiring, fabrication, sourcing, assembly and cosmetics — one person, one deadline, one very large can.'),
    PROJECTS[1])

# --- Recycler ----------------------------------------------------------------
rec_chapters = [
    chapter('why', 'The spark', 'Chapter 01 — The spark', '“Why not recycle it?”', f'''          <p class="text reveal">I was set on getting involved in every STEM opportunity I could find. I joined the clubs and went to the workshops, but none of them felt very impactful — so I decided to start a project of my own.</p>
          <p class="text big reveal" style="margin-top:1.5rem">Then one day I was 3D printing the frame for a DC motor I was designing. The print failed — and the people running the workshop threw it straight in the trash.</p>
          <div class="text reveal" style="margin-top:2rem">
            <p>That's when the lightbulb went off. After some digging, I found out you can't just put failed prints in the recycling bin. So that became my project: build a machine that recycles failed 3D prints. It would build my skills and help the environment at the same time.</p>
            <p>The catch: I was starting with <strong>zero practical engineering experience</strong>. It was a big thing to take on.</p>
          </div>'''),
    chapter('concept', 'Early iterations', 'Chapter 02 — Starting from zero', 'Learning by designing.', f'''          <div class="text reveal">
            <p>My first concept was modeled part by part — blades, spacers, walls and a base plate. Figuring out how to actually build it is what led me to the makerspace (STEMbassadors / IDEA Center), where I got heavily involved and picked up the skills I needed for this project and every one after it.</p>
          </div>''' + '\n' +
        '          <p class="gallery-label mono reveal">First concept</p>\n' +
        gallery([('images/recycler/early-iso.jpg', 'Isometric view'), ('images/recycler/early-front.jpg', 'Front view'), ('images/recycler/early-top.jpg', 'Top view'), ('images/recycler/early-right.jpg', 'Right view')], P, 'cad') + '\n' +
        '          <p class="gallery-label mono reveal">Parts</p>\n' +
        gallery([('images/recycler/early-blade.jpg', 'Blade'), ('images/recycler/early-spacer.jpg', 'Spacer'), ('images/recycler/early-wall-quarter.jpg', '1/4" wall'), ('images/recycler/early-wall-five-eighths.jpg', '5/8" wall'), ('images/recycler/early-baseplate.jpg', 'Base plate')], P, 'cad')),
    chapter('design', 'Final design', 'Chapter 03 — Final design', 'Every part, designed by me.', f'''          <div class="text reveal">
            <p>I did all of the design work myself in SolidWorks: a motor driving the shredder through a chain and sprockets, with the whole machine mounted on a single base plate.</p>
          </div>''' + '\n' +
        gallery([('images/recycler/cad-full-assembly.jpg', 'Full final assembly: motor, chain drive and shredder')], P, 'cad') + '\n' +
        '          <p class="gallery-label mono reveal">Along the way</p>\n' +
        gallery([('images/recycler/cad-final.jpg', 'Shredder assembly'), ('images/recycler/cad-shredder.jpg', 'Shredder with motor')], P, 'cad')),
    chapter('build', 'Making it', 'Chapter 04 — Making it', 'Make what you can. Outsource what you can\'t.', f'''          <div class="split">
            <div class="text reveal">
              <p>Most of the metalwork — cutting the sheet metal and welding the parts together — was outsourced, since I don't have metalworking equipment.</p>
              <p>The shims I cut myself on a <strong>fiber laser</strong>.</p>
            </div>
            <div class="bom reveal" style="margin:0;grid-template-columns:1fr 1fr">
              <div><b>Design</b><span>All me, in SolidWorks</span></div>
              <div><b>Shims</b><span>Fiber laser, by me</span></div>
              <div><b>Sheet metal</b><span>Outsourced cutting</span></div>
              <div><b>Welding</b><span>Outsourced</span></div>
            </div>
          </div>''' + '\n' +
        '          <p class="gallery-label mono reveal">Parts</p>\n' +
        gallery([('images/recycler/parts-blades.jpg', 'Shredder blades'), ('images/recycler/parts-gears.jpg', 'Gears and hardware'), ('images/recycler/parts-bearings.jpg', 'Bearings')], P) + '\n' +
        '          <p class="gallery-label mono reveal">Cutting shims</p>\n' +
        gallery([('images/recycler/laser-cut.jpg', 'Cutting on the fiber laser'), ('images/recycler/spacer.jpg', 'Laser-cut shim'), ('images/recycler/keyed-part.jpg', 'Keyed shim'), ('images/recycler/cut-parts.jpg', 'Cut parts')], P) + '\n' +
        '          <p class="gallery-label mono reveal">Welding &amp; assembly</p>\n' +
        gallery([('images/recycler/welding.jpg', 'Welding'), ('images/recycler/plywood-base.jpg', 'Plywood base'), ('images/recycler/assembly-plate.jpg', 'Assembling the blade housing'), ('images/recycler/shredder-assembled.jpg', 'Shredder assembled'), ('images/recycler/shredder-built.jpg', 'Shredder with drive')], P)),
    chapter('now', 'Where it is now', 'Chapter 05 — Where it is now', 'From one person to an organization.', f'''          <div class="split">
            <div class="text reveal">
              <p>The recycler has mostly lived on the back burner, worked on in bursts whenever I had time. But it did something bigger than shred plastic: it led me to the makerspace and pushed me to grow the skills that made every other project possible.</p>
              <p>Now that I'm at USC, I've handed the project off to <strong>STEMbassadors</strong>, the non-profit makerspace, so their space can become a beacon of recycling for the community. What started as just me is now part of an organization.</p>
            </div>
{gallery([('images/recycler/extruder.jpg', 'The extrusion stage')], P)}
          </div>'''),
]
build_project(PROJECTS[1], 'images/recycler/shredder-built.jpg',
    'The project that started it all: a machine to recycle failed 3D prints, now carried on by the STEMbassadors makerspace.',
    [('0', 'experience at the start'), ('100%', 'designed by me'), ('1', 'non-profit carrying it on')], rec_chapters,
    None, PROJECTS[2])

# --- Turret ----------------------------------------------------------------
tur_chapters = [
    chapter('why', 'The idea', 'Chapter 01 — Coming up with the idea', 'The guide gave me a parts list. Nothing else.', f'''          <p class="text big reveal">I started from an online Nerf turret guide — but it was outdated, covered the bare minimum, and had no information on how to program it.</p>
          <div class="text reveal" style="margin-top:2rem"><p>All it really provided was a materials list. Everything else — the mechanism, the wiring, the code and the app — I had to research and work out myself.</p></div>'''),
    chapter('design', 'Design', 'Chapter 02 — Creation', 'Planned on paper, built in cardboard.', f'''          <div class="split">
            <div class="text reveal">
              <p>Before building anything, I drew every part <strong>to scale</strong> so everything was planned out ahead of time — the base mount, the magazine, and the mounts for the DC motors, the continuous 360° servo and the 180° servo.</p>
              <p>The prototype was built from cardboard, which kept it fast and cheap to iterate on — even if cardboard doesn't always come out as intended.</p>
            </div>
            <ol class="steps reveal">
              <li><div><b>Spin up</b>Two DC motors spin in opposite directions to act as flywheels.</div></li>
              <li><div><b>Feed</b>A servo pushes a dart from the magazine into the spinning motors.</div></li>
              <li><div><b>Launch</b>The flywheels grip the dart and fire it out.</div></li>
            </ol>
          </div>
          <p class="gallery-label mono reveal">Plans &amp; first parts</p>
{gallery([('images/turret/creation.jpg', 'To-scale drawings and the planned model'), ('images/turret/base.jpg', 'Base'), ('images/turret/mount.jpg', 'Mount'), ('images/turret/magazine.jpg', 'Magazine (before DC motors)'), ('images/turret/flywheels.jpg', 'Servo feeding a dart into the flywheels')], P)}'''),
    chapter('problems', 'Problems & fixes', 'Chapter 03 — Problems', 'First version: it didn\'t work.', f'''          <div class="split">
            <div class="reveal">
              <p class="mono" style="color:var(--accent-2);margin-bottom:1rem">What went wrong</p>
              <ol class="steps">
                <li><div><b>Both servos on the same side</b>The layout put both servo motors next to each other.</div></li>
                <li><div><b>Blocked pusher</b>The motor that pushes out the darts was physically blocked.</div></li>
                <li><div><b>Weight &amp; stability</b>Poor weight distribution made the whole turret unstable.</div></li>
              </ol>
            </div>
            <div class="reveal">
              <p class="mono" style="color:var(--accent);margin-bottom:1rem">The fix</p>
              <ol class="steps">
                <li><div><b>Follow the arc</b>I redesigned the mount so it follows the arc of the magazine.</div></li>
                <li><div><b>Supported</b>The new layout successfully supports the mechanism and clears the pusher.</div></li>
              </ol>
            </div>
          </div>
{gallery([('images/turret/problem-2.jpg', 'The blocked pusher'), ('images/turret/solution-1.jpg', 'New piece cut to the magazine arc'), ('images/turret/solution-2.jpg', 'Redesigned mount')], P)}'''),
    chapter('wiring', 'Wiring', 'Chapter 04 — Put together', 'Wiring it up.', f'''          <div class="bom reveal">
              <div><b>Servo motor</b><span>3 wires — two for the circuit, one for communication</span></div>
              <div><b>DC motors</b><span>Power, speed and direction lines</span></div>
              <div><b>Bluetooth module</b><span>5 wires — two for communication, two for the circuit</span></div>
          </div>
{gallery([('images/turret/wiring-diagram.jpg', 'Wiring diagram'), ('images/turret/wiring.jpg', 'Breadboard wiring'), ('images/turret/put-together.jpg', 'Put together'), ('images/turret/turret.jpg', 'Electronics mounted')], P)}'''),
    chapter('app', 'The app', 'Chapter 05 — Programming the app', 'A phone app, built with blocks.', f'''          <div class="split">
            <div class="text reveal">
              <p>I built the controller app in <strong>MIT App Inventor</strong> using block code. It was easy to use, though getting the alignment and sizing right was a little difficult.</p>
            </div>
            <ol class="steps reveal">
              <li><div><b>Connect</b>Lists available Bluetooth devices and connects to the turret.</div></li>
              <li><div><b>Status</b>Updates on a timer and shows whether Bluetooth is connected.</div></li>
              <li><div><b>Control</b>Sends strings that are converted to ASCII characters on button pushed, released and clicked.</div></li>
            </ol>
          </div>
{gallery([('images/turret/app-designer.jpg', 'The app in MIT App Inventor'), ('images/turret/app-blocks.jpg', 'Bluetooth block code')], P)}'''),
    chapter('code', 'Arduino code', 'Chapter 06 — Programming the Arduino', 'Every movement at once.', f'''          <div class="text reveal">
            <p>The Arduino side uses <strong>Servo.h</strong> for servo commands and <strong>SoftwareSerial.h</strong> to send bytes back and forth with the app. Pins and motor speeds are all set in variables at the top, so the whole program can be tuned from one place.</p>
            <p>On startup it sets up every pin, opens serial communication and moves all the motors to their starting positions. In the loop, <code>Serial.available</code> checks for a link and <code>Serial.read</code> takes in commands. Each command flips a set of booleans, and because everything runs through independent <code>if</code> statements, the turret can make multiple movements simultaneously — stepping in 1° increments with microsecond delays.</p>
          </div>'''),
    chapter('learned', 'What I learned', 'Chapter 07 — Final thoughts', 'Difficulty 7/10. Fun 9/10.', f'''          <div class="split">
            <div class="text reveal">
              <p>The hardest part was the design — there are so many factors to keep in mind, all while working in cardboard. The research was tedious, and sometimes there was no answer to find, so I had to use my best judgement.</p>
              <p>The whole process was fun, especially the small wins: getting a motor to work, finishing each part, and figuring out fixes within my limitations. The best part is when everything finally comes together — which is also the worst part, because then there's nothing left to work on.</p>
            </div>
            <ol class="steps reveal">
              <li><div><b>Circuits</b>Building circuits and working with DC and servo motors.</div></li>
              <li><div><b>Power</b>Keeping components from being overloaded, and reading power resistors.</div></li>
              <li><div><b>3D design &amp; apps</b>Designing parts virtually, and what it takes to make an app.</div></li>
              <li><div><b>Research</b>Greatly improved research skills.</div></li>
            </ol>
          </div>'''),
]
build_project(PROJECTS[2], 'images/turret/turret.jpg',
    'A Bluetooth Nerf turret controlled from a phone app — designed in cardboard, wired on an Arduino, and programmed from scratch.',
    [('7/10', 'difficulty'), ('9/10', 'fun'), ('BT', 'phone control')], tur_chapters,
    None, PROJECTS[0])

build_home()
print('built')
