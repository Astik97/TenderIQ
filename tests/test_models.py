from backend.models.tender import Tender

tender = Tender(1,
                10,
                "Bridge Tender",
                "bridge.pdf",
                "Sample Text",
                "2026-07-11")

print(tender)

print(tender.tender_name)