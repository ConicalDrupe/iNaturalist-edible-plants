# Workflow and Rules 

## Rules
### Rule 1
If ,on the current page, the species info spans to the next page. Mark as spanning multiple pages.

### Rule 2
When appending a page with multilpe species. Seperate the manually edited names/edibles with a pipe "|" 

### Rule 3 - PostProcessing
For any appended data that is null, it is assumed that the extracted data is correct; and thus can be filled in.

## Cases
### Case 1 - Edibility Text not found
When edibility is not found, run these records through the human-in-the-loop gui.
With the gui flags/boxes, will be able to distingush the species and their edible parts (sometimes multiple on the same page)

### Case 2 - Edibility Text found
The extracted csv will be fed into an LLM to extract the exact text that states species names and edible parts.
Afterwards, this Extracted data will be run through the human-in-the-loop gui for verification.

