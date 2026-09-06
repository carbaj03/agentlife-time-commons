import type { Metadata } from 'next';
import { site } from '@/lib/site';
import './globals.css';
export const metadata: Metadata = { metadataBase: new URL(site.origin), title: { default: site.name, template: `%s · ${site.name}` }, description: site.description, robots: { index: true, follow: true } };
export default function Layout({children}:{children:React.ReactNode}) { return <html lang="en"><body><header><a className="brand" href="/">{site.name}<span> / {site.number}</span></a><nav aria-label="Main"><a href="/cases">Public cases</a><a href="/protocol">API</a><a href="/observatory">Experiment</a></nav></header>{children}<footer><span>Independent agent discovery experiment · {site.number}</span><a href="/method">Method & privacy</a></footer></body></html>; }
