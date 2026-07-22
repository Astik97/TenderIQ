class Tender:

    def __init__(
        self,
        id,
        user_id,
        tender_name,
        file_name,
        extracted_text,
        upload_date):

        self.id = id

        self.user_id = user_id

        self.tender_name = tender_name

        self.file_name = file_name

        self.extracted_text = extracted_text

        self.upload_date = upload_date

    def __repr__(self):

        return f"Tender({self.tender_name})"