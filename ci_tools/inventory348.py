"""Inventaire complet des 348 partitions via footers Parquet en requetes Range.
Aucun fichier Parquet entier n'est telecharge : seuls pied + metadonnees transitent.
En cas d'echec sur une partition, l'erreur est consignée, jamais masquee."""
import io, json, re, sys, hashlib, pathlib
import requests
import pyarrow.parquet as pq

FOLDER = "1gQc_VjKSTDLzRZZa6B8mO071nf8XG28e"
CERTS = {
 "P1": "1lIe3sUSfXpKVwjLiN3mIBesIY9mFJiCT",
 "P2": "1NeCMJfiiGtOj8CIvif9vJOpgaL2kHJe6",
}
S = requests.Session(); S.headers.update({"User-Agent":"Mozilla/5.0"})

def listing():
    url = f"https://drive.google.com/embeddedfolderview?id={FOLDER}#list"
    html = S.get(url, timeout=60).text
    # HTML reel : l'ancre contient l'ID puis le nom du fichier dans la meme balise.
    pairs = [(num, fid) for fid, num in re.findall(
        r'href="https://drive\.google\.com/file/d/([A-Za-z0-9_-]+)[^"]*"[^>]*>(?:(?!</a>).)*?part_(\d{6})\.parquet',
        html, re.S)]
    if len(pairs) < 300: raise RuntimeError(f"parseur de liste: {len(pairs)} paires seulement - structure Drive inattendue")
    out = {}
    for num, fid in pairs:
        out[f"part_{num}.parquet"] = fid
    return dict(sorted(out.items()))

class RangeFile(io.RawIOBase):
    def __init__(self, fid):
        self.url = f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"
        self.pos = 0; self._size = None; self._cache = {}
    @property
    def size(self):
        if self._size is None:
            r = S.get(self.url, headers={"Range":"bytes=0-0"}, timeout=60)
            cr = r.headers.get("Content-Range","")
            if "/" in cr: self._size = int(cr.rsplit("/",1)[1])
            else: raise RuntimeError(f"range non supporte (status {r.status_code}, pas de Content-Range)")
        return self._size
    def readable(self): return True
    def seekable(self): return True
    def tell(self): return self.pos
    def seek(self, off, whence=0):
        self.pos = off if whence==0 else self.pos+off if whence==1 else self.size+off
        return self.pos
    def read(self, n=-1):
        if n is None or n<0: n = self.size-self.pos
        if n==0: return b""
        key=(self.pos,n)
        if key not in self._cache:
            end=self.pos+n-1
            r=S.get(self.url, headers={"Range":f"bytes={self.pos}-{end}"}, timeout=120)
            if r.status_code not in (206,200): raise RuntimeError(f"range HTTP {r.status_code} @{self.pos}")
            data=r.content[:n] if r.status_code==206 else r.content[self.pos:self.pos+n]
            self._cache[key]=data
        data=self._cache[key]; self.pos+=len(data); return data

def canon_hash(raw: bytes):
    obj=json.loads(raw.decode("utf-8"))
    canon=json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest(), obj

def main():
    out={"folder_id":FOLDER,"certificates":{},"partitions":[],"errors":[]}
    for code,fid in CERTS.items():
        r=S.get(f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t",timeout=60)
        ch,obj=canon_hash(r.content)
        out["certificates"][code]={"drive_id":fid,"file_sha256":hashlib.sha256(r.content).hexdigest(),
            "sha256_canonical":ch,"status":obj.get("status"),"doc":obj}
    lst=listing(); out["partitions_found"]=len(lst)
    print(f"listing: {len(lst)} partitions", flush=True)
    total=0; sigs={}
    for name,fid in lst.items():
        try:
            rf=RangeFile(fid); pf=pq.ParquetFile(rf); md=pf.metadata
            cols=[(pf.schema_arrow.names[i],str(pf.schema_arrow.types[i])) for i in range(len(pf.schema_arrow.names))]
            sig=hashlib.sha256("|".join(f"{a}:{b}" for a,b in cols).encode()).hexdigest()[:16]
            sigs.setdefault(sig,{"columns":cols,"count":0,"rows":0}); sigs[sig]["count"]+=1; sigs[sig]["rows"]+=md.num_rows
            total+=md.num_rows
            out["partitions"].append({"name":name,"drive_id":fid,"rows":md.num_rows,"row_groups":md.num_row_groups,"schema_signature":sig})
        except Exception as e:
            out["errors"].append({"name":name,"drive_id":fid,"error":f"{type(e).__name__}: {e}"})
        if len(out["partitions"])%50==0: print(f"  {len(out['partitions'])} ok, total provisoire {total:,}", flush=True)
    out["total_rows_footers"]=total; out["schema_signatures"]=sigs
    names=sorted(lst)
    out["partitions_listing_sha256"]="sha256:"+hashlib.sha256("|".join(names).encode()).hexdigest()
    pathlib.Path("reports/meta_alpha/INVENTORY_348.json").write_text(json.dumps(out,indent=2,ensure_ascii=False))
    print(json.dumps({"found":len(lst),"ok":len(out["partitions"]),"errors":len(out["errors"]),"total_rows":total,"signatures":len(sigs)},indent=2))
if __name__=="__main__": main()
