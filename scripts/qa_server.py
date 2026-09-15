"""Local browser audit server. Injects axe and lab probes without changing dist.

Never used by deployment. Bind only to loopback. Application scripts can be omitted
with ?nojs=1 for a progressive-enhancement check; the audit probe still runs.
"""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
from bs4 import BeautifulSoup
import argparse,json,re
ROOT=Path(__file__).resolve().parent.parent
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT/'dist'),**kwargs)
    def log_message(self,*args):pass
    def do_GET(self):
        parsed=urlsplit(self.path)
        special={'/__qa/axe.js':ROOT/'node_modules/axe-core/axe.min.js','/__qa/probe.js':ROOT/'scripts/qa_probe.js'}
        if parsed.path in special:
            body=special[parsed.path].read_bytes();self.send_response(200);self.send_header('Content-Type','text/javascript');self.end_headers();self.wfile.write(body);return
        file=ROOT/'dist'/parsed.path.lstrip('/')
        if file.is_dir():file=file/'index.html'
        if file.suffix!='.html' or not file.exists():return super().do_GET()
        soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
        if parse_qs(parsed.query).get('nojs')==['1']:
            for script in soup.find_all('script'):script.decompose()
            for noscript in soup.find_all('noscript'):
                noscript.replace_with(BeautifulSoup(noscript.decode_contents(),'html.parser'))
        observer=soup.new_tag('script',src='/__qa/probe.js');soup.head.insert(0,observer)
        axe=soup.new_tag('script',src='/__qa/axe.js');soup.body.append(axe)
        body=str(soup).encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(body)
    def do_POST(self):
        if self.path!='/__qa/report' or self.headers.get('Origin')!=f'http://127.0.0.1:{self.server.server_port}':self.send_error(403);return
        length=int(self.headers.get('Content-Length','0'))
        if length>1000000:self.send_error(413);return
        report=json.loads(self.rfile.read(length));name=re.sub(r'[^a-z0-9-]+','-',report['path'].lower()).strip('-') or 'home'
        out=ROOT/'.qa/browser';out.mkdir(exist_ok=True,parents=True)
        (out/f'{name}-{report["width"]}-{report["theme"]}{"-nojs" if report["nojs"] else ""}.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        self.send_response(204);self.end_headers()
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=4322);args=parser.parse_args();print(f'Local audit server: http://127.0.0.1:{args.port}',flush=True);ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
