from pathlib import Path


DATA_DIR = Path("data")


SERVICE_MANUAL = """Mitsubishi After-Sales Service Manual - Training Sample

Routine service interval:
Servis berkala Xpander, Pajero Sport, Triton, dan Outlander direkomendasikan setiap 10.000 km atau 6 bulan, mana yang tercapai lebih dahulu. Routine service for Xpander and other Mitsubishi passenger vehicles is recommended every 10,000 km or 6 months, whichever comes first.

Engine oil:
Oli mesin diperiksa pada setiap kunjungan servis. Penggantian oli mengikuti jadwal servis berkala dan kondisi pemakaian kendaraan. Engine oil is inspected during every routine visit and replaced according to service schedule and usage condition.

20,000 km inspection:
Servis 20.000 km mencakup pemeriksaan sistem rem, kondisi ban, tekanan ban, cairan kendaraan, filter udara, filter kabin, lampu, aki, wiper, suspensi, dan komponen keselamatan.

Tire pressure:
Tekanan ban harus mengikuti label pada pintu pengemudi atau manual kendaraan. Periksa tekanan saat ban dingin dan sebelum perjalanan jauh.

Air filter:
Filter udara diperiksa saat servis berkala. Filter diganti jika kotor, rusak, atau sesuai interval yang direkomendasikan dealer resmi.

Brake pad:
Kampas rem harus diganti jika ketebalan sudah di bawah batas aman, muncul bunyi abnormal, atau ditemukan performa pengereman menurun saat inspeksi.

Authorized dealer:
Servis di dealer resmi disarankan agar riwayat servis tercatat, suku cadang sesuai spesifikasi, dan pemeriksaan mengikuti standar pabrikan.

Battery inspection:
Inspeksi aki mencakup pemeriksaan tegangan, terminal, kondisi fisik, kebersihan konektor, dan performa starting.

Fluids:
During routine service, technicians inspect engine oil, brake fluid, coolant, transmission fluid, and washer fluid.
"""


WARRANTY_TERMS = """Mitsubishi Warranty Terms - Training Sample

Coverage:
Garansi menanggung cacat material atau pengerjaan pabrik selama periode dan syarat garansi masih berlaku. The warranty covers manufacturing defects in material or workmanship within the valid warranty period and conditions.

Warranty period:
Masa berlaku garansi mengikuti periode yang tertulis pada buku garansi atau dokumen penyerahan kendaraan. Customers must refer to the warranty booklet for the exact period.

Claim requirements:
Klaim garansi memerlukan pemeriksaan dealer resmi, riwayat servis, dan bukti bahwa kerusakan termasuk cakupan garansi. Dealer berwenang menentukan hasil pemeriksaan.

Exclusions:
Kerusakan akibat banjir, kecelakaan, modifikasi, kelalaian, penggunaan tidak sesuai manual, kompetisi, atau penggunaan komersial ekstrem tidak ditanggung garansi.

Modification:
Modifikasi yang memengaruhi komponen terkait dapat membuat klaim garansi ditolak untuk komponen tersebut. Warranty impact is limited to affected components after dealer assessment.

Wear items:
Normal wear items and consumables are not covered unless a manufacturing defect is confirmed by an authorized dealer.

Service cost:
Garansi tidak berarti semua servis gratis. Item perawatan berkala, consumables, jasa servis, dan program gratis servis mengikuti ketentuan dealer atau program resmi yang berlaku.

Unsupported claims:
Dealer should not promise that all damage is free under warranty. If evidence is insufficient, the correct answer is that information is not available from the provided documents.
"""


def escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def write_minimal_pdf(path: Path, title: str, text: str) -> None:
    lines = [title, ""] + [line.strip() for paragraph in text.splitlines() for line in paragraph.split(". ")]
    lines = [line for line in lines if line]
    content_lines = ["BT", "/F1 10 Tf", "50 790 Td", "14 TL"]
    for idx, line in enumerate(lines[:50]):
        if idx:
            content_lines.append("T*")
        content_lines.append(f"({escape_pdf_text(line[:95])}) Tj")
    content_lines.append("ET")
    stream = "\n".join(content_lines).encode("latin-1", errors="replace")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")
    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n".encode(
            "ascii"
        )
    )
    path.write_bytes(pdf)


def write_pdf(path: Path, title: str, text: str) -> None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError:
        write_minimal_pdf(path, title, text)
        return

    c = canvas.Canvas(str(path), pagesize=A4)
    _, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(45, y, title)
    y -= 26
    c.setFont("Helvetica", 10)
    for paragraph in text.splitlines():
        paragraph = paragraph.strip()
        if not paragraph:
            y -= 8
            continue
        words = paragraph.split()
        line = ""
        for word in words:
            candidate = f"{line} {word}".strip()
            if len(candidate) > 100:
                c.drawString(45, y, line)
                y -= 14
                line = word
            else:
                line = candidate
        if line:
            c.drawString(45, y, line)
            y -= 16
        if y < 45:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 45
    c.save()


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    write_pdf(DATA_DIR / "service_manual.pdf", "Service Manual", SERVICE_MANUAL)
    write_pdf(DATA_DIR / "warranty_terms.pdf", "Warranty Terms", WARRANTY_TERMS)
    print("Generated data/service_manual.pdf and data/warranty_terms.pdf")


if __name__ == "__main__":
    main()
