import torch
from transformers import XLMTokenizer, XLMForQuestionAnswering


tokenizer = XLMTokenizer.from_pretrained('xlm-mlm-tlm-xnli15-1024')
model = XLMModel.from_pretrained('xlm-mlm-tlm-xnli15-1024')


def sample_because_im_learning(string):
    tokens = tokenizer.tokenize(string) # Will build tokens as the model sees them
    ids = tokenizer.convert_tokens_to_ids(tokens) # Transforms tokens to ids
    special_ids = tokenizer.build_inputs_with_special_tokens(ids) # Adds special ids, like begining of sentences
    return special_ids


# From https://huggingface.co/mrm8488/bert-spanish-cased-finetuned-ner
xlm_ner = pipeline(
    "ner",
    model='xlm-mlm-tlm-xnli15-1024',
    tokenizer=('xlm-mlm-tlm-xnli15-1024', {"use_fast": False})
)


# bert-spanish-cased-finetuned-ner
from transformers import pipeline
nlp_ner = pipeline(
    "ner",
    model="mrm8488/bert-spanish-cased-finetuned-ner",
    tokenizer=('mrm8488/bert-spanish-cased-finetuned-ner', {"use_fast": False})
)


# BETO: https://github.com/dccuchile/beto

