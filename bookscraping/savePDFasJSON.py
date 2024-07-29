import os
import json
import fitz

def convert_pdf_to_json(pdf_path, save_path, start_page, end_page):
    with fitz.open(pdf_path) as doc:
        num_pages = doc.page_count

        if start_page < 0 or start_page >= num_pages:
            raise ValueError('Invalid start page')

        if end_page < 0 or end_page >= num_pages or end_page < start_page:
            raise ValueError('Invalid end page')

        pdf_data = []

        for page_num in range(start_page, end_page + 1):
            page = doc.load_page(page_num)

            # Extract formatting information
            text_content = []
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                lines = block.get("lines", [])
                for line in lines:
                    spans = line.get("spans", [])
                    for span in spans:
                        text = span["text"]
                        bbox = span["bbox"]
                        font_size = span["size"]

                        # Create a dictionary for each text element
                        text_content.append({
                            'text': text,
                            'bbox': bbox,
                            'font_size': font_size
                        })

            # Create a dictionary for each page
            page_data = {
                'page_number': page_num + 1,
                'text_content': text_content
            }

            pdf_data.append(page_data)

        # Create a dictionary to store the PDF data
        output_data = {
            'file_name': pdf_path,
            'num_pages': num_pages,
            'pages': pdf_data
        }

        # Convert the dictionary to JSON
        json_data = json.dumps(output_data, indent=4)

        # Save the JSON to a file
        with open(save_path, 'w') as json_file:
            json_file.write(json_data)


if __name__ == '__main__':
    # Usage example
    pdf_file_path = "~/Projects/iNaturalist-edible-plants/data/raw/'Southeast Foraging-compressed.pdf'"
    save_path = '~/Projects/iNaturalist-edible-plants/data/outputs/southeast_foraging.json'
    start_page_number = 58  # 0-based index
    end_page_number = 516  # 0-based index

    convert_pdf_to_json(pdf_file_path,save_path, start_page_number, end_page_number)
