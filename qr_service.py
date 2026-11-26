import asyncio
from io import BytesIO

import qrcode
from qrcode.constants import ERROR_CORRECT_M


def _build_qr(data: str) -> BytesIO:
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=12,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    buffer.name = "qrcode.png"
    return buffer


async def generate_qr(data: str) -> BytesIO:
    """Generate a QR code PNG without blocking the event loop."""
    return await asyncio.to_thread(_build_qr, data)
