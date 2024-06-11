# 5g_chatbot

1.Data source - excel sheet with historic Q&A (CSVloader) 
2.creating embeeding(from text to numeric) of data (Hugging face) 
3.save those embeeding into vector database (Chroma) 
4.the question asked by user will convert into embedding and search in the vector database which Q&A embeeding matches the most. (Retervial QA) 
5.Those embedding will convert into text and a promt will be create and be given to LLM and LLM will give human readble answer.(Google Palm)

LLM-SQL --

1.Taking to sql in plain english langauge 2.Convert text into sql querty using google palm sqlsequentialchain. 3.create Fewshot learning so that model doesnt fail 4.creating embeeding(from text to numeric) of data (Hugging face) 5.save those embeeding into vector database (ChromaDB) 6.Few shot promt template (SQLdatabase chain)
