import lzma, struct, pathlib, requests, datetime as dt
out=[]
for d in [dt.date(2023,6,15), dt.date(2020,8,3)]:
    u=f'https://datafeed.dukascopy.com/datafeed/XAUUSD/{d.year}/{d.month-1:02d}/{d.day:02d}/BID_candles_min_1.bi5'
    r=requests.get(u, timeout=90, headers={'User-Agent':'Mozilla/5.0'})
    out.append(f'{u} statut={r.status_code} octets={len(r.content)}')
    if r.status_code==200 and len(r.content)>100:
        dec=lzma.decompress(r.content); out.append(f'decompresse={len(dec)} reste24={len(dec)%24}')
        recs=[struct.unpack_from('>5if', dec, i*24) for i in range(min(5, len(dec)//24))]
        out.append(f'premiers: {recs}')
        ts=[struct.unpack_from('>i', dec, i*24)[0] for i in range(len(dec)//24)]
        out.append(f't min={min(ts)} max={max(ts)} n={len(ts)} ecarts_tete={[ts[i+1]-ts[i] for i in range(5)]}')
pathlib.Path('reports/meta_alpha/nr/S3_PROBE.txt').write_text('\n'.join(out))
print('\n'.join(out))
