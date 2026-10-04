"""Pull knowledge base answers (articles) in full and save them for local profiling.

Articles migrate and hold no caller data (Ben Bolding, 2026-10-01), so this pulls rows, unlike
profile_data.py. Every query goes through OsvcClient.query_answers(), which refuses anything
that is not a single SELECT on answers.

    export OSVC_SITE_URL=https://nci--tst.cx.usg.oraclecloud.com
    export OSVC_USER=<the test account>
    python3 oracle/tools/profile_answers.py --probe      # five rows per query shape, nothing saved
    python3 oracle/tools/profile_answers.py --pull

Output: oracle/extracts/answers/<date>/ (gitignored): answers.parquet (one row per answer),
and one file per list (products, categories, siblings, related answers, attachments). Attachment files themselves are not downloaded; only their names, types and sizes.
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import date
from pathlib import Path

import polars as pl

sys.path.insert(0, str(Path(__file__).resolve().parent))

from osvc_client import OsvcClient, load_credentials, load_site_url  # noqa: E402

EXTRACTS = Path(__file__).resolve().parent.parent / "extracts" / "answers"
C = "customFields.c."
BODY = ["id", "summary", "question", "solution", "specialResponse", "keywords", f"{C}is_notes"]
META = [
    "id", "language.lookupName", "statusWithType.status.lookupName", "statusWithType.statusType.lookupName",
    "answerType.lookupName", f"{C}answer_types.lookupName", f"{C}answer_source.lookupName", f"{C}cig.lookupName",
    f"{C}referral_type.lookupName", "createdTime", "updatedTime", "expiresDate", "publishOnDate", "lastAccessTime",
    "uRL", "name", "accessLevels", "positionInList.lookupName", "versionDetail.state.lookupName",
    f"{C}cisimportid", f"{C}import_notes", f"{C}cisimportprodcats", f"{C}admin_import", f"{C}former_name",
    f"{C}former_name_2", f"{C}countyparishborough", f"{C}zip_cide", f"{C}referral_city", f"{C}referral_contact",
    f"{C}referral_contact_email", f"{C}referral_contact_phone", f"{C}nci_db", f"{C}quicklink",
    "customFields.Referrals.Country.lookupName", "customFields.Referrals.State.lookupName",
    "customFields.Referrals.Language1.lookupName", "customFields.Referrals.Language2.lookupName",
]
LISTS = {
    "products": ["id", "products.id", "products.lookupName"],
    "categories": ["id", "categories.id", "categories.lookupName"],
    "siblings": ["id", "siblingAnswers.id"],
    "related": ["id", "relatedAnswers.toAnswer.id", "relatedAnswers.manualStrength"],
    "attachments": ["id", "fileAttachments.id", "fileAttachments.fileName", "fileAttachments.contentType", "fileAttachments.size"],
    "common_attachments": ["id", "commonAttachments.id", "commonAttachments.fileName", "commonAttachments.contentType", "commonAttachments.size"],
}
ROW_CAP = 20000


def names(cols: list[str]) -> list[str]:
    return [c.replace(C, "").replace("customFields.Referrals.", "ref_").replace(".lookupName", "").replace(".", "_") for c in cols]


class Puller:
    def __init__(self, client: OsvcClient, pause: float) -> None:
        self.client, self.pause, self.sent = client, pause, 0

    def query(self, roql: str) -> list[list]:
        if self.sent:
            time.sleep(self.pause)
        self.sent += 1
        status, data = self.client.query_answers(roql)
        if status != 200:
            raise SystemExit(f"{status} on: {roql[:160]}\n{str(data)[:400]}")
        rows = (data.get("items") or [{}])[-1].get("rows") or []
        if len(rows) >= ROW_CAP:
            raise SystemExit(f"Row cap reached on: {roql[:160]}")
        return rows

    def keyset(self, cols: list[str], page: int, limit_pages: int | None = None) -> pl.DataFrame:
        out, last, pages = [], 0, 0
        while True:
            rows = self.query(f"SELECT {', '.join(cols)} FROM answers WHERE id > {last} ORDER BY id LIMIT {page}")
            out.extend(rows)
            pages += 1
            print(f"  {len(out)} rows", flush=True)
            if len(rows) < page or (limit_pages and pages >= limit_pages):
                break
            last = int(rows[-1][0])
        return pl.DataFrame(out, schema=names(cols), orient="row", infer_schema_length=None) if out else pl.DataFrame(schema=names(cols))

    def by_id_range(self, cols: list[str], lo: int, hi: int, step: int) -> pl.DataFrame:
        out = []
        for a in range(lo - 1, hi, step):
            out.extend(self.query(f"SELECT {', '.join(cols)} FROM answers WHERE id > {a} AND id <= {a + step} AND {cols[1]} IS NOT NULL"))
        return pl.DataFrame(out, schema=names(cols), orient="row", infer_schema_length=None) if out else pl.DataFrame(schema=names(cols))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--pull", action="store_true")
    ap.add_argument("--into", default=date.today().isoformat())
    ap.add_argument("--pause", type=float, default=2.0)
    ap.add_argument("--page", type=int, default=100)
    args = ap.parse_args(argv)
    out = EXTRACTS / args.into
    out.mkdir(parents=True, exist_ok=True)
    p = Puller(OsvcClient(load_site_url(), load_credentials(), out / "_manifest.jsonl", timeout=180.0), args.pause)

    if args.probe:
        for label, cols in {"body": BODY, "meta": META, **LISTS}.items():
            try:
                rows = p.query(f"SELECT {', '.join(cols)} FROM answers WHERE id > 0 ORDER BY id LIMIT 5") if label in ("body", "meta") \
                    else p.query(f"SELECT {', '.join(cols)} FROM answers WHERE {cols[1]} IS NOT NULL LIMIT 5")
                widths = [max((len(str(v)) for v in col if v is not None), default=0) for col in zip(*rows)] if rows else []
                print(f"OK   {label}: {len(rows)} rows, {len(cols)} columns, longest value per column {widths}")
            except SystemExit as e:
                print(f"FAIL {label}: {str(e)[:300]}")
        return 0

    if args.pull:
        print("body"); body = p.keyset(BODY, args.page)
        print("meta"); meta = p.keyset(META, 500)
        answers = meta.join(body, on="id", how="full", coalesce=True)
        answers.write_parquet(out / "answers.parquet")
        ids = answers["id"].cast(pl.Int64)
        lo, hi = int(ids.min()), int(ids.max())
        for label, cols in LISTS.items():
            print(label)
            df = p.by_id_range(cols, lo, hi, 2000)
            df.write_parquet(out / f"answer_{label}.parquet")
            print(f"  {df.height} rows")
        print(f"Requests sent: {p.sent}. Saved to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
