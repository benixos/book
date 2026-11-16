#!/usr/bin/env python3
"""Generate assets/benixos-system-architecture.svg (the layered architecture diagram).

Usage:  python3 -I tools/make_diagram.py [output.svg]      (standard library only)

Edit the rows in this file, run it, then run tools/build.py. Status colours:
live / pre-release, alpha, draft / not shipped, host.
"""
import sys
from xml.sax.saxutils import escape
out = sys.argv[1] if len(sys.argv) > 1 else str(__import__('pathlib').Path(__file__).resolve().parent.parent / 'assets' / 'benixos-system-architecture.svg')
W = 1100
LABELW = 150
X0 = LABELW + 20          # content left
CW = W - X0 - 20          # content width
ST = {  # fill, stroke, dash
 'live':   ('#c8e6c9', '#2e7d32', ''),
 'alpha':  ('#bbdefb', '#1a56db', ''),
 'draft':  ('#ffe0b2', '#c77700', '5,4'),
 'banked': ('#e0e0e0', '#8a8a8a', ''),
 'host':   ('#ede7f6', '#5e35b1', ''),
 'hw':     ('#f5f5f5', '#616161', ''),
}
parts = []
def rect(x,y,w,h,fill,stroke,dash='',rx=6,sw=1.2):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
def text(x,y,s,size=12,weight='normal',fill='#222',anchor='middle'):
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')
def box(x,y,w,h,title,sub,st):
    f,s,d = ST[st]
    rect(x,y,w,h,f,s,d)
    if sub:
        text(x+w/2,y+h/2-3,title,12,'bold')
        text(x+w/2,y+h/2+12,sub,10,'normal','#444')
    else:
        text(x+w/2,y+h/2+4,title,12,'bold')
def row(x,y,w,h,items,gap=8):
    n=len(items); bw=(w-gap*(n-1))/n
    for i,(t,s,st) in enumerate(items):
        box(x+i*(bw+gap),y,bw,h,t,s,st)
def layer(y,h,label,sub,band,edge):
    rect(10,y,W-20,h,band,edge,'',8,1.5)
    rect(10,y,LABELW,h,edge,edge,'',8,0)
    # label text, wrapped manually
    lines = label.split('\n')
    ty = y+h/2-(len(lines)-1)*8-(8 if sub else 0)
    for i,l in enumerate(lines):
        text(10+LABELW/2,ty+i*16,l,14,'bold','#fff')
    if sub:
        for i,l in enumerate(sub.split('\n')):
            text(10+LABELW/2,ty+len(lines)*16+i*12,l,10,'normal','#fff')

y=60
title_y=34
BH=44
# 1 Applications
h1=84
layer(y,h1,'Applications','what people and\nagents use','#f1f8e9','#558b2f')
row(X0,y+20,CW,BH+8,[
 ('Hearth clients','apps and agents','live'),
 ('Household services','media, home automation, DNS','live'),
 ('Apps','Wasm components','draft'),
 ('Automation','scheduled agent jobs','alpha'),
 ('Operator tools','CLI, lease keeper','draft'),
])
y+=h1+10
# 2 Kits
kit_rows=[
 [('Message Kit','pre-release','live'),('Fabric Kit','pre-release + stream','live'),('Spec Kit','alpha','alpha'),('Storage Kit','alpha','alpha'),('Identity Kit','alpha + claim','alpha')],
 [('Venue Kit','alpha','alpha'),('Errand Kit','alpha','alpha'),('Substrate Kit','alpha + host','alpha'),('Service Kit','alpha','alpha'),('App Context Kit','alpha','alpha')],
 [('Interface Kit','alpha + mold','alpha'),('Work Strip Kit','alpha + dispatcher','alpha'),('Inference Kit','alpha','alpha'),('Manifest Kit','alpha, build time','alpha')],
]
h2=3*(BH+8)+6
layer(y,h2,'Kits','framework layer,\none Kit per domain\n(no Kit is stable yet)','#e3f2fd','#1565c0')
for i,r in enumerate(kit_rows):
    row(X0,y+14+i*(BH+8),CW,BH,r)
y+=h2+10
# 3 Servers
h3=3*(BH+8)+28
layer(y,h3,'System servers','long-running\nservices','#fff8e1','#ef8f00')
row(X0,y+14,CW,BH,[
 ('venued','registry + planner','alpha'),
 ('Venue node agent','executor + enforcer','draft'),
 ('gateway','router, consent, grants','live'),
 ('Service glues','loopback-bound adapters','live'),
])
row(X0,y+14+BH+8,CW,BH,[
 ('hub local mode','presence, roster','draft'),
 ('claim-agent + mDNS','device claim, discovery','live'),
 ('inference service','model router, ledger','alpha'),
 ('identity provider','OIDC, hosted','live'),
])
row(X0,y+14+2*(BH+8),CW,BH,[
 ('Casement','window-class presenter','draft'),
 ('Wasm loader','one process per app','draft'),
 ('Signer','issues grants after consent','draft'),
])
y+=h3+10
# 4 Node contract / wire
h4=BH+28
layer(y,h4,'Node contract\nand wire','the HAL equivalent','#fce4ec','#ad1457')
row(X0,y+14,CW,BH,[
 ('Hearth','wire contract, public spec','live'),
 ('Namespace ops','walk read write invoke watch','draft'),
 ('Node contract v0','16 clauses, draft','draft'),
 ('Capability grants','typed-address enforcement','draft'),
])
y+=h4+10
# 5 Node runtime
h5=BH+28
layer(y,h5,'Node runtime','the "kernel"\nBenixOS leans on','#ede7f6','#4527a0')
row(X0,y+14,CW,BH,[
 ('libbenix','portable primitives','alpha'),
 ('dockerd + containers','cgroups, mounts, networks','live'),
 ('Volume driver','FUSE, proof of concept','draft'),
 ('Local bus','AF_UNIX SEQPACKET','alpha'),
])
y+=h5+10
# 6 Hosts
h6=BH+28
layer(y,h6,'Hosts','any host meeting\nthe node contract','#eceff1','#37474f')
row(X0,y+14,CW,BH,[
 ('DeviceNix','native distro: Yocto, Mender','host'),
 ('Ubuntu / Debian','what runs today','host'),
 ('macOS','local transport gap','draft'),
 ('Windows / containers','not Linux Docker nodes','draft'),
])
y+=h6+10
# 7 Hardware
h7=BH+28
layer(y,h7,'Hardware','','#fafafa','#616161')
row(X0,y+14,CW,BH,[
 ('Single-board class','Pi 5 / CM5','hw'),
 ('AMD64 class','micro-ATX workstation','hw'),
 ('Generic PC / VM','virtual machine or PC','hw'),
])
y+=h7+14
# legend
lx=X0
for name,st in [('live / pre-release','live'),('alpha','alpha'),('draft / not shipped','draft'),('host','host')]:
    f,s,d=ST[st]; rect(lx,y,16,12,f,s,d,3)
    text(lx+22,y+10,name,11,'normal','#333','start'); lx+=170
y+=26
text(W/2,y,'Status as of 16 November 2026.',10,'normal','#666')
y+=16
head=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {y}" width="{W}" height="{y}" font-family="Helvetica, Arial, sans-serif"><rect width="100%" height="100%" fill="#fff"/>'
title=f'<text x="{W/2}" y="{title_y}" font-size="22" font-weight="bold" text-anchor="middle" fill="#111">BenixOS system architecture</text>'
open(out,'w').write(head+title+''.join(parts)+'</svg>')
print(y)
