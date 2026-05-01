"""
tools/build_hub_image.py — EduNode hub image builder
=====================================================
Generates a per-region configuration package for zero-config Pi deployment.

Usage:
    python tools/build_hub_image.py --hub sarawak
    python tools/build_hub_image.py --list
    python tools/build_hub_image.py --all

Output: builds/edunode_<hub_id>/   (and a .tar.gz alongside it)
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import tarfile
import textwrap
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Hub definitions (single source of truth for the builder)
# ---------------------------------------------------------------------------

HUB_CONFIGS: dict[str, dict] = {
    "singapore": {
        "region":       "Singapore",
        "tier1":        ["English"],
        "tier2":        [],
        "ssid":         "EduNode_Singapore",
        "ip":           "192.168.1.1",
        "kolibri_lang": "en",
        "kolibri_channel": "7765d6abe4f5413b9bb35a03b4bcea63",
        "deploy_lang":  "English",
    },
    "vietnam": {
        "region":       "Vietnam",
        "tier1":        ["English", "Vietnamese"],
        "tier2":        ["Hmong"],
        "ssid":         "EduNode_Vietnam",
        "ip":           "192.168.1.1",
        "kolibri_lang": "vi",
        "kolibri_channel": "7765d6abe4f5413b9bb35a03b4bcea63",
        "deploy_lang":  "English",
    },
    "sarawak": {
        "region":       "Sarawak, Malaysia",
        "tier1":        ["English", "Bahasa Melayu"],
        "tier2":        ["Iban", "Kedayan"],
        "ssid":         "EduNode_Sarawak",
        "ip":           "192.168.1.1",
        "kolibri_lang": "en",
        "kolibri_channel": "7765d6abe4f5413b9bb35a03b4bcea63",
        "deploy_lang":  "English",
    },
    "west_java": {
        "region":       "West Java, Indonesia",
        "tier1":        ["English", "Bahasa Indonesia"],
        "tier2":        ["Sundanese"],
        "ssid":         "EduNode_WestJava",
        "ip":           "192.168.1.1",
        "kolibri_lang": "id",
        "kolibri_channel": "7765d6abe4f5413b9bb35a03b4bcea63",
        "deploy_lang":  "English",
    },
    "visayas": {
        "region":       "Visayas, Philippines",
        "tier1":        ["English", "Filipino"],
        "tier2":        ["Cebuano"],
        "ssid":         "EduNode_Visayas",
        "ip":           "192.168.1.1",
        "kolibri_lang": "en",
        "kolibri_channel": "7765d6abe4f5413b9bb35a03b4bcea63",
        "deploy_lang":  "English",
    },
    "isan": {
        "region":       "Isan, Thailand",
        "tier1":        ["English", "Thai"],
        "tier2":        ["Isan"],
        "ssid":         "EduNode_Isan",
        "ip":           "192.168.1.1",
        "kolibri_lang": "th",
        "kolibri_channel": "7765d6abe4f5413b9bb35a03b4bcea63",
        "deploy_lang":  "English",
    },
    "cambodia": {
        "region":       "Rural Cambodia",
        "tier1":        ["English", "Khmer"],
        "tier2":        [],
        "ssid":         "EduNode_Cambodia",
        "ip":           "192.168.1.1",
        "kolibri_lang": "km",
        "kolibri_channel": "7765d6abe4f5413b9bb35a03b4bcea63",
        "deploy_lang":  "English",
    },
    "laos": {
        "region":       "Rural Laos",
        "tier1":        ["English", "Lao"],
        "tier2":        [],
        "ssid":         "EduNode_Laos",
        "ip":           "192.168.1.1",
        "kolibri_lang": "lo",
        "kolibri_channel": "7765d6abe4f5413b9bb35a03b4bcea63",
        "deploy_lang":  "English",
    },
    "shan": {
        "region":       "Shan State, Myanmar",
        "tier1":        ["English"],
        "tier2":        ["Shan"],
        "ssid":         "EduNode_Shan",
        "ip":           "192.168.1.1",
        "kolibri_lang": "en",
        "kolibri_channel": "7765d6abe4f5413b9bb35a03b4bcea63",
        "deploy_lang":  "English",
    },
    "timor_leste": {
        "region":       "Timor-Leste",
        "tier1":        ["English"],
        "tier2":        ["Tetum"],
        "ssid":         "EduNode_TimorLeste",
        "ip":           "192.168.1.1",
        "kolibri_lang": "en",
        "kolibri_channel": "7765d6abe4f5413b9bb35a03b4bcea63",
        "deploy_lang":  "English",
    },
    "brunei": {
        "region":       "Brunei Darussalam",
        "tier1":        ["English", "Bahasa Melayu"],
        "tier2":        ["Kedayan"],
        "ssid":         "EduNode_Brunei",
        "ip":           "192.168.1.1",
        "kolibri_lang": "en",
        "kolibri_channel": "7765d6abe4f5413b9bb35a03b4bcea63",
        "deploy_lang":  "English",
    },
    "kalimantan": {
        "region":       "Kalimantan, Indonesia",
        "tier1":        ["English", "Bahasa Indonesia"],
        "tier2":        ["Dayak"],
        "ssid":         "EduNode_Kalimantan",
        "ip":           "192.168.1.1",
        "kolibri_lang": "id",
        "kolibri_channel": "7765d6abe4f5413b9bb35a03b4bcea63",
        "deploy_lang":  "English",
    },
    "peninsular_malaysia": {
        "region":       "Peninsular Malaysia",
        "tier1":        ["English", "Bahasa Melayu"],
        "tier2":        [],
        "ssid":         "EduNode_Malaysia",
        "ip":           "192.168.1.1",
        "kolibri_lang": "ms",
        "kolibri_channel": "7765d6abe4f5413b9bb35a03b4bcea63",
        "deploy_lang":  "English",
    },
}

# ---------------------------------------------------------------------------
# File generators
# ---------------------------------------------------------------------------

def _gen_config_py(hub_id: str, cfg: dict) -> str:
    """Generate config.py with only this hub active."""
    tier1_repr = repr(cfg["tier1"])
    tier2_repr = repr(cfg["tier2"])
    all_langs  = cfg["tier1"] + [l for l in cfg["tier2"] if l not in cfg["tier1"]]
    return textwrap.dedent(f"""\
        # config.py — auto-generated for hub: {hub_id}
        # Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}

        HUB_ID         = "{hub_id}"
        HUB_REGION     = "{cfg['region']}"
        HUB_LANGUAGES  = {repr(all_langs)}
        TIER_1_LANGS   = {tier1_repr}
        TIER_2_LANGS   = {tier2_repr}

        WIFI_SSID      = "{cfg['ssid']}"
        HUB_IP         = "{cfg['ip']}"

        KOLIBRI_PORT    = 8080
        KOLIBRI_CHANNEL = "{cfg['kolibri_channel']}"

        SLM_MODEL = "llama3.2:3b-instruct-q4_K_M"

        GLOSSARY_DATASETS = {{
            "cebuano": "filbench/cebuano-readability",
            "iban":    "VynerCK/Iban-language-data",
        }}

        AVAILABLE_SUBJECTS = [
            "Mathematics",
            "Science",
            "English Language",
            "Environmental Studies",
            "Digital Literacy",
        ]
    """)


def _gen_wifi_setup_sh(hub_id: str, cfg: dict) -> str:
    ssid     = cfg["ssid"]
    password = "edunode2026"
    ip       = cfg["ip"]
    return textwrap.dedent(f"""\
        #!/usr/bin/env bash
        # wifi_setup.sh — auto-generated for hub: {hub_id}
        # Run as root on Raspberry Pi OS Bookworm

        set -euo pipefail

        SSID="{ssid}"
        PASSWORD="{password}"
        IP="{ip}/24"

        echo "[EduNode] Configuring WiFi hotspot..."

        # Create hotspot
        nmcli dev wifi hotspot ifname wlan0 ssid "$SSID" password "$PASSWORD"

        # Set static IP
        nmcli connection modify "$SSID" \\
            ipv4.method shared \\
            ipv4.addresses "$IP" \\
            ipv4.gateway "" \\
            connection.autoconnect yes

        nmcli connection up "$SSID"

        echo "[EduNode] Hotspot '$SSID' active at $IP"
    """)


def _gen_kolibri_setup_sh(hub_id: str, cfg: dict) -> str:
    lang    = cfg["kolibri_lang"]
    channel = cfg["kolibri_channel"]
    return textwrap.dedent(f"""\
        #!/usr/bin/env bash
        # kolibri_setup.sh — auto-generated for hub: {hub_id}
        # Run once after 'pip install kolibri'

        set -euo pipefail

        CHANNEL="{channel}"
        LANG="{lang}"

        echo "[EduNode] Installing Kolibri and importing Khan Academy channel..."

        # Start Kolibri (creates default database)
        python -m kolibri start &
        sleep 8

        # Import the channel (metadata only first, then resources)
        python -m kolibri manage importchannel -- network "$CHANNEL"
        python -m kolibri manage importcontent -- network "$CHANNEL"

        echo "[EduNode] Kolibri channel $CHANNEL imported (lang: $LANG)"
        echo "[EduNode] Kolibri available at http://localhost:8080"
    """)


def _gen_deploy_md(hub_id: str, cfg: dict) -> str:
    tier2_note = ""
    if cfg["tier2"]:
        langs = ", ".join(cfg["tier2"])
        tier2_note = f"\n> **Tier-2 languages** ({langs}) use bridge-mode translation via glossary files.\n"
    return textwrap.dedent(f"""\
        # EduNode — Deploy Guide ({cfg['region']})

        Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}

        ## Quick Start

        1. Flash Raspberry Pi OS Bookworm (64-bit) to a 64 GB SD card / SSD.
        2. `ssh pi@raspberrypi.local`
        3. `git clone https://github.com/YOUR_ORG/EduNode.git && cd EduNode`
        4. Copy the files from this bundle into the repo root:
           ```
           cp edunode_{hub_id}/config.py .
           cp edunode_{hub_id}/wifi_setup.sh .
           cp edunode_{hub_id}/kolibri_setup.sh .
           cp -r edunode_{hub_id}/data/glossaries/ data/
           ```
        5. Run setup: `bash setup.sh`
        6. Set admin token: `export ADMIN_TOKEN=your_secret`
        7. Start services:
           ```bash
           ollama serve &
           python -m kolibri start &
           gunicorn -w 2 -b 0.0.0.0:5000 'app:app'
           ```
        8. Connect a device to WiFi SSID **{cfg['ssid']}** (password: `edunode2026`)
        9. Open browser → `http://{cfg['ip']}`

        ## Hub Details

        | Field       | Value |
        |-------------|-------|
        | Hub ID      | `{hub_id}` |
        | Region      | {cfg['region']} |
        | WiFi SSID   | `{cfg['ssid']}` |
        | IP Address  | `{cfg['ip']}` |
        | Tier-1 Languages | {', '.join(cfg['tier1'])} |
        | Tier-2 Languages | {', '.join(cfg['tier2']) or '—'} |
        | Kolibri Language | `{cfg['kolibri_lang']}` |
        {tier2_note}
        ## Troubleshooting

        - **Ollama not responding**: run `ollama pull llama3.2:3b-instruct-q4_K_M`
        - **No quiz generated**: check `ollama serve` is running
        - **Kolibri 404**: wait 30s after `python -m kolibri start` then refresh
        - **Admin panel**: `http://{cfg['ip']}/admin?token=your_secret`

        ---
        *EduNode is open-source — UNESCO SDG4 aligned.*
    """)


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

def build_hub(hub_id: str, output_root: Path = Path("builds")) -> Path:
    if hub_id not in HUB_CONFIGS:
        raise ValueError(f"Unknown hub '{hub_id}'. Use --list to see valid IDs.")

    cfg     = HUB_CONFIGS[hub_id]
    out_dir = output_root / f"edunode_{hub_id}"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    # --- config.py ---
    (out_dir / "config.py").write_text(_gen_config_py(hub_id, cfg))

    # --- wifi_setup.sh ---
    wifi_sh = out_dir / "wifi_setup.sh"
    wifi_sh.write_text(_gen_wifi_setup_sh(hub_id, cfg))
    wifi_sh.chmod(0o755)

    # --- kolibri_setup.sh ---
    kolibri_sh = out_dir / "kolibri_setup.sh"
    kolibri_sh.write_text(_gen_kolibri_setup_sh(hub_id, cfg))
    kolibri_sh.chmod(0o755)

    # --- DEPLOY.md ---
    (out_dir / "DEPLOY.md").write_text(_gen_deploy_md(hub_id, cfg))

    # --- Glossaries: copy only the ones needed for this hub's Tier-2 langs ---
    glossary_src = Path("data/glossaries")
    glossary_dst = out_dir / "data" / "glossaries"
    glossary_dst.mkdir(parents=True)
    lang_to_file = {
        "cebuano":  "cebuano.json",
        "iban":     "iban.json",
        "hmong":    "hmong.json",
        "sundanese":"sundanese.json",
        "isan":     "isan.json",
        "shan":     "shan.json",
        "tetum":    "tetum.json",
        "dayak":    "dayak.json",
        "kedayan":  "kedayan.json",
    }
    for lang in cfg["tier2"]:
        fname = lang_to_file.get(lang.lower())
        if fname:
            src_file = glossary_src / fname
            if src_file.exists():
                shutil.copy2(src_file, glossary_dst / fname)
            else:
                # Write an empty placeholder so the bundle is self-contained
                (glossary_dst / fname).write_text("[]")

    # --- tar.gz ---
    tar_path = output_root / f"edunode_{hub_id}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(out_dir, arcname=f"edunode_{hub_id}")

    return out_dir


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build EduNode hub configuration bundles.",
    )
    parser.add_argument("--hub",  help="Hub ID to build (e.g. sarawak)")
    parser.add_argument("--all",  action="store_true", help="Build all 13 hubs")
    parser.add_argument("--list", action="store_true", help="List available hub IDs")
    parser.add_argument("--output", default="builds", help="Output directory (default: builds/)")
    args = parser.parse_args()

    if args.list:
        print("Available hubs:")
        for hid, hcfg in HUB_CONFIGS.items():
            t1 = ", ".join(hcfg["tier1"])
            t2 = ", ".join(hcfg["tier2"]) if hcfg["tier2"] else "—"
            print(f"  {hid:<25} {hcfg['region']:<30} T1: {t1}  T2: {t2}")
        return

    output_root = Path(args.output)

    if args.all:
        for hid in HUB_CONFIGS:
            out = build_hub(hid, output_root)
            print(f"  Built: {out}")
        print(f"\nAll {len(HUB_CONFIGS)} hub bundles written to {output_root}/")
        return

    if args.hub:
        out = build_hub(args.hub, output_root)
        tar = output_root / f"edunode_{args.hub}.tar.gz"
        print(f"Built:   {out}/")
        print(f"Archive: {tar}")
        print(f"\nFiles in bundle:")
        for p in sorted(out.rglob("*")):
            if p.is_file():
                print(f"  {p.relative_to(output_root)}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
