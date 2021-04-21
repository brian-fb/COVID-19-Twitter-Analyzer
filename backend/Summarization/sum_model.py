from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import pipeline
import numpy as np

class Summary_Generator():
    def __init__(self):
        self.summarizer_bart = pipeline('summarization', model='facebook/bart-large-cnn',
                                        tokenizer='facebook/bart-large-cnn')
        self.summarizer_T5 = T5ForConditionalGeneration.from_pretrained('t5-base')
        self.tokenizer = T5Tokenizer.from_pretrained('t5-base')

    def bart(self, text):
        max_l = int(np.maximum(2, round(0.2 * len(text.split(' ')))))
        min_l = int(np.maximum(1, round(0.1 * len(text.split(' ')))))
        summary_bart = self.summarizer_bart(text, min_length=min_l, max_length=max_l, do_sample=False)
        return summary_bart[0]['summary_text']

    def T5(self, text):
        tokens_input = self.tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
        summary_T5_ids = self.summarizer_T5.generate(tokens_input, min_length=60, max_length=180, length_penalty=4.0)
        summary_T5 = self.tokenizer.decode(summary_T5_ids[0]).split('>')[1].split('<')[0]
        return summary_T5