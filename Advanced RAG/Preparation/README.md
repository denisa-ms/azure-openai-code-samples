
### Generating synthetic data for testing

Please read the following CONTEXT and generate two question and answer json objects in an array based on the CONTEXT provided. The questions should require deep reading comprehension, logical inference, deduction, and connecting ideas across the text. Avoid simplistic retrieval or pattern matching questions. Instead, focus on questions that test the ability to reason about the text in complex ways, draw subtle conclusions, and combine multiple pieces of information to arrive at an answer. Ensure that the questions are relevant, specific, and cover the key points of the CONTEXT.  Provide concise answers to each question, directly quoting the text from provided context. Provide the array output in strict JSON format as shown in output format. Ensure that the generated JSON is 100 percent structurally correct, with proper nesting, comma placement, and quotation marks. There should not be any comma after last element in the array.
  
Output format:
```
[
  {
    "question": "Question 1",
    "answer": "Answer 1"
  },
  {
    "question": "Question 2",
    "answer": "Answer 2"
  }
]
```

CONTEXT:{{add context here}}