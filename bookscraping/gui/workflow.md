# Case 1 - Edibility Text not found
When edibility is not found, run these records through the human-in-the-loop gui.
With the gui flags/boxes, will be able to distingush the species and their edible parts (sometimes multiple on the same page)

# Case 2 - Edibility Text found
The extracted csv will be fed into an LLM to extract the exact text that states species names and edible parts.
Afterwards, this Extracted data will be run through the human-in-the-loop gui for verification.


