---

Prompt evaluations: the missing half of working with AI
Everyone is writing prompts. Blog posts, courses, Twitter threads, entire communities devoted to the art of crafting the perfect instruction for a language model. But there is a quiet problem hiding beneath all that enthusiasm: almost nobody is measuring whether their prompts actually work.
Prompt evaluation is the practice of systematically testing and scoring your prompts against real-world scenarios before they reach production. It is to prompt engineering what unit testing is to software development - a discipline that separates hobbyist experimentation from reliable, production-grade systems. And just like unit testing, the teams that skip it pay for it later.
This article is a comprehensive guide to prompt evaluation: what it is, why it matters, how a typical workflow operates, and the specific techniques - from generating test datasets to grading with models and code - that make evaluation practical at any scale.

---

Why prompt evaluation matters
Consider a common scenario. An engineer writes a prompt for a customer support chatbot. They test it with five or six questions, get reasonable answers, and ship it. Within a week, users are sending messages the engineer never imagined: misspelled queries, multi-part questions, sarcastic complaints, messages in languages the prompt was never designed for. The chatbot stumbles, and trust erodes.
This is not a prompt engineering failure. The prompt itself might be well-crafted. It is an evaluation failure - a failure to stress-test the prompt against the full range of inputs it will encounter.
Prompt evaluation solves this by providing three things that manual testing cannot: breadth (testing against hundreds or thousands of diverse inputs), objectivity (scoring with consistent criteria rather than gut feel), and reproducibility (running the same tests after every change to track whether the prompt is improving or regressing).
Without evaluation, prompt development is guesswork. With it, prompt development becomes engineering.

---

Prompt evaluation versus prompt engineering
These two disciplines are complementary but distinct. Prompt engineering is about craft - the techniques you use to write better prompts. Chain of thought, few-shot examples, XML structuring, role assignment, and dozens of other methods that shape how a language model interprets and responds to your instructions.
Prompt evaluation is about measurement. It answers a single question: does this prompt work? And more specifically, does it work better than the last version? Evaluation gives you a number, and that number lets you make decisions with confidence rather than intuition.
The relationship between the two is cyclical. You engineer a prompt, evaluate it, learn where it falls short, engineer a better version, and evaluate again. Neither discipline is useful in isolation. A beautifully engineered prompt that has never been evaluated is a liability. An evaluation pipeline with nothing to test is an empty framework.

---

A typical eval workflow
A prompt evaluation workflow is a pipeline that takes a prompt, runs it against a set of test cases, scores the results, and produces a performance metric. While implementations vary in tooling and complexity, the core steps are consistent.
Step 1: Draft your initial prompt
Every evaluation begins with a prompt to test. This is your baseline - the version you suspect works, but cannot yet prove. It does not need to be perfect. In fact, it should not be. The point of evaluation is to reveal the gap between what you think works and what actually works.
Your initial prompt might be as simple as a single instruction line, or it might be a complex template with multiple variables, system instructions, and formatting rules. Either way, it becomes the first version in your evaluation history.
Step 2: Build an evaluation dataset
The evaluation dataset is the backbone of your pipeline. It is a collection of test cases - inputs that you will feed into your prompt - that represent the range of scenarios your prompt will encounter in production.
Each test case typically contains an input (the data that gets merged into your prompt template) and, optionally, an expected output or reference answer that the grader will compare against.
The quality of your evaluation is directly proportional to the quality of this dataset. A small, narrow dataset will give you false confidence. A large, diverse dataset will reveal the true performance envelope of your prompt.
Step 3: Run the prompt against every test case
With your prompt template and dataset ready, you merge each test case into the prompt and send it to the language model. This step is mechanical - iterate through the dataset, substitute each input into your prompt template, call the model, and collect the responses.
The result is a set of input-output pairs: every test case now has a corresponding model response. These pairs become the raw material for grading.
Step 4: Grade the results
Grading is where evaluation becomes objective. Each input-output pair is scored according to criteria you define. The grading can be done by another language model (model-based grading), by deterministic code (code-based grading), or by a combination of both.
The grader assigns a score to each response - typically on a numerical scale - and produces an aggregate metric across the entire dataset. This metric is your prompt's performance score.
Step 5: Iterate and compare
Armed with a baseline score, you now modify your prompt and repeat the entire pipeline. The new version gets the same dataset, the same grading criteria, and produces a new score. If the score improves, the change was beneficial. If it drops, you revert or try a different approach.
This cycle of modify, evaluate, compare is what transforms prompt development from a creative exercise into a measurable engineering process.

---

Generating test datasets
The evaluation dataset is the most underestimated component of the entire pipeline. A poorly constructed dataset will mislead you as surely as no dataset at all. Building good datasets requires thinking carefully about coverage, edge cases, and realism.
Manual curation
The most reliable datasets start with human judgment. Domain experts sit down and write test cases that represent the real-world scenarios the prompt must handle. This is labor-intensive but produces high-quality, realistic inputs that automated methods often miss.
Manual curation works best for specialized domains - medical triage, legal analysis, financial compliance - where the nuance of realistic inputs matters enormously and cannot be easily synthesized.
Synthetic generation with language models
For broader coverage, you can use language models themselves to generate test cases. By providing a description of your domain and the types of inputs you expect, you can ask a model to produce dozens or hundreds of varied test cases. This approach scales well and often surfaces edge cases that human curators overlook because the model draws on a wider range of patterns than any single person carries in their head.
The risk with synthetic datasets is homogeneity. Models can fall into repetitive patterns, generating variations that look diverse but test the same underlying capability. Mitigate this by generating in batches with different instructions, explicitly requesting edge cases, adversarial inputs, and out-of-distribution examples.
Production log sampling
If your prompt is already in production, your richest source of test data is the real inputs users are sending. Sampling from production logs gives you the most realistic dataset possible - these are the actual scenarios your prompt faces daily, including the bizarre, malformed, and unexpected inputs that no curated or synthetic dataset would think to include.
Production sampling is particularly valuable for regression testing. When you modify a prompt, running it against real historical inputs tells you whether the change would have improved or degraded the experience for actual users.
Adversarial test cases
Every dataset should include a deliberate adversarial subset: inputs designed to break, confuse, or exploit the prompt. These are the messages that real users will eventually send, whether intentionally or not.
Adversarial cases include ambiguous inputs with multiple valid interpretations, inputs that contradict assumptions baked into the prompt, extremely long or extremely short inputs, inputs in unexpected languages or formats, inputs that attempt to override or manipulate the prompt's instructions, and inputs that fall entirely outside the prompt's intended domain.
A prompt that scores well on clean inputs but collapses on adversarial ones is not production-ready.
Dataset size and diversity
There is no universal answer to how large your dataset should be, but there are useful heuristics. For initial development, 30 to 50 well-chosen test cases will surface most major issues. For pre-production validation, 200 to 500 cases provide stronger statistical confidence. For ongoing monitoring, datasets of 1,000 or more allow you to detect subtle regressions and performance shifts over time.
Diversity matters more than size. Fifty carefully varied test cases will tell you more than five hundred repetitive ones. Ensure your dataset covers the full range of input types, difficulty levels, topics, and edge cases your prompt must handle.

---

Running the eval
Running an evaluation means executing your prompt against every test case in the dataset and collecting the results. While conceptually simple, the execution details matter for reliability and efficiency.
Batch execution
For datasets of any meaningful size, you will want to run evaluations in batch rather than one at a time. Most API providers offer batch or concurrent request capabilities that let you process hundreds of test cases efficiently. The key considerations are rate limiting (staying within API quotas), error handling (retrying failed requests without losing progress), and cost management (evaluation runs add up quickly at scale).
Temperature and sampling
Language model outputs are often non-deterministic - the same prompt can produce different responses on repeated runs. This variability means a single evaluation run provides a noisy signal. For more reliable scores, run each test case multiple times and average the results, or set the model's temperature to zero to get deterministic outputs during evaluation.
The choice depends on your use case. If your production system uses a temperature above zero, evaluating at that same temperature gives you a more honest picture of real-world performance, but you will need multiple runs to get stable scores.
Tracking metadata
Every evaluation run should record not just the scores but the full context: which prompt version was tested, which model was used, what temperature and parameters were set, when the evaluation was run, and any other configuration that might affect results. This metadata becomes essential when you are comparing results across dozens of prompt iterations and need to understand exactly what changed between versions.
Cost considerations
Evaluation is an investment. Every test case requires at least one API call to the model being tested, and model-based grading adds additional calls on top. For a dataset of 500 test cases with model-based grading, a single evaluation run costs roughly 1,000 API calls. Running five prompt iterations means 5,000 calls.
This cost is real but typically modest compared to the cost of shipping a broken prompt to production. Think of evaluation as quality assurance - the expense is justified by the defects it catches.

---

Model-based grading
Model-based grading uses a language model as the judge. You take each question-answer pair from your evaluation, feed it to a grading model along with scoring criteria, and ask the model to assess the quality of the response. This approach is flexible, nuanced, and capable of evaluating qualities that are difficult to capture with code alone.
How it works
The grading model receives the original input, the model's response, optionally a reference answer, and a rubric describing what constitutes a good versus poor response. The grader then produces a score - typically a number on a fixed scale - along with an explanation of its reasoning.
The rubric is the critical piece. A vague rubric like "rate the quality from 1 to 10" produces inconsistent scores because the model has no shared definition of quality. A precise rubric that specifies what each score level means produces much more reliable and consistent grading.
What model-based grading is best for
Model-based grading excels at evaluating qualities that are inherently subjective or context-dependent. Tone and style assessment is a natural fit - determining whether a response sounds professional, empathetic, friendly, or authoritative requires understanding nuance that code cannot capture.
Completeness evaluation works well because the grading model can read the input, understand what was asked, and assess whether the response addressed all aspects of the question. Similarly, coherence and logical flow, appropriate level of detail for the audience, and creative quality in open-ended tasks are all areas where model-based grading outperforms rule-based alternatives.
It is also the default choice when there is no single correct answer. If you ask a model to write a marketing email, there are thousands of valid outputs. A code-based grader cannot enumerate them. A model-based grader can read the output, compare it to the intent, and make a judgment.
Designing effective rubrics
An effective rubric defines each score level with concrete, observable criteria. Rather than asking "how good is this response," a strong rubric might specify that a score of 10 means the response directly answers the question, provides accurate information, uses an appropriate tone, and includes relevant context without unnecessary filler. A score of 5 means the response is partially correct but missing key information or including irrelevant material. A score of 1 means the response is incorrect, off-topic, or harmful.
The more specific the rubric, the more consistent the grading. Rubrics should also be tested and iterated - just like the prompts they evaluate.
Using a stronger model as grader
A common and effective pattern is to use a more capable model as the grader than the one being evaluated. If you are evaluating responses from a smaller, faster model, use a larger, more capable model to grade them. This creates a quality hierarchy where the grader can reliably identify issues that the evaluated model might produce.
Limitations
Model-based grading is not perfect. Grading models have their own biases - they may favor verbose responses, penalize unconventional but correct answers, or struggle with domain-specific accuracy. Grading models can also be inconsistent, scoring the same response differently on repeated runs.
These limitations are manageable but must be acknowledged. Validate your grading model's judgments against human assessments on a sample of test cases to ensure alignment. And always pair model-based grading with code-based checks for any criteria that can be measured deterministically.

---

Code-based grading
Code-based grading uses deterministic functions to evaluate model outputs. Where model-based grading relies on judgment, code-based grading relies on rules. The result is perfectly consistent, fast, cheap, and transparent - but limited to criteria that can be expressed as logic.
How it works
A code-based grader is a function that takes the model's response (and optionally the input and reference answer) and returns a score. The function applies one or more checks and produces a numerical result.
These checks can be simple (does the response contain the expected keyword?) or complex (does the response conform to a specific JSON schema with all required fields populated and all values within valid ranges?). The key property is determinism: the same input always produces the same score.
What code-based grading is best for
Code-based grading is the right choice whenever the correctness criteria can be precisely defined. Factual accuracy is the most common case - if there is a known correct answer, a code grader can check whether the response matches, contains, or approximates it.
Format compliance is another strong use case. If your prompt asks the model to respond in JSON, XML, or a specific template, code can parse the output and verify structural correctness with perfect reliability. No model-based grader matches the precision of a JSON schema validator.
Length constraints, required keyword inclusion or exclusion, mathematical correctness, language detection, PII detection, and response latency are all naturally suited to code-based grading. Any criterion that has a definitive right or wrong answer belongs in a code grader.
Common grading patterns
Exact match grading compares the model's output directly against a reference answer. This is strict - useful for questions with unambiguous answers like calculations, factual lookups, or classification tasks.
Containment grading checks whether the response includes specific required elements. This is more flexible than exact match and works well for open-ended responses where the answer can vary in phrasing but must include certain facts.
Regex and pattern matching allows you to verify that responses follow expected formats without requiring exact wording. This is useful for structured outputs like dates, phone numbers, addresses, or identifiers.
Semantic similarity uses embedding models to compute how close the response is to a reference answer in meaning, even if the wording differs. This bridges the gap between rigid code checks and flexible model grading.
Composite scoring combines multiple checks into a weighted aggregate. A single response might be scored on factual accuracy (40% weight), format compliance (20%), appropriate length (20%), and absence of prohibited content (20%). Each component is a deterministic check, and the weighted sum produces an overall score.
Advantages over model-based grading
Code-based grading is perfectly reproducible. Run the same grader on the same response a million times, and you get the same score every time. This makes it ideal for regression testing and continuous integration.
It is also fast and free. Unlike model-based grading, which requires API calls, code-based grading runs locally at the speed of your compute. For large datasets, this difference is significant.
And it is transparent. When a code grader gives a low score, you can trace exactly which check failed and why. There is no black box. This traceability makes debugging straightforward and builds confidence in the evaluation results.
Limitations
Code-based grading cannot evaluate open-ended quality. It cannot tell you whether a response is well-written, appropriately nuanced, or emotionally intelligent. It cannot assess whether a creative response is good. For these qualities, you need model-based grading.
The practical approach is to use both: code-based grading for everything that can be precisely defined, and model-based grading for everything else.

---

Combining model-based and code-based grading
The most robust evaluation pipelines use both approaches in combination. Code-based checks handle the hard constraints - format, accuracy, length, compliance - while model-based grading evaluates the softer qualities: tone, completeness, usefulness, coherence.
A combined grading pipeline might first run code checks to filter out obviously broken responses (malformed JSON, missing required fields, incorrect calculations), then pass the remaining responses to a model-based grader for quality assessment. The final score is a weighted combination of both.
This layered approach gives you the best of both worlds: the precision and speed of code, plus the nuance and flexibility of model judgment.

---

Real-world use cases for prompt evaluation
Prompt evaluation is not an academic exercise. It solves real problems across every domain where language models are deployed.
Customer support automation
A company deploys a chatbot to handle customer inquiries. The evaluation dataset contains hundreds of real customer messages sampled from support logs, covering product questions, billing disputes, technical issues, emotional complaints, and off-topic messages. Code-based grading checks that the bot never leaks internal data and always follows the escalation protocol. Model-based grading evaluates whether responses are empathetic, accurate, and helpful. The eval pipeline runs after every prompt change, catching regressions before they reach customers.
Content generation at scale
A media company uses prompts to generate article summaries, social media posts, and email newsletters. The evaluation dataset includes articles from every content category the company covers. Code grading checks output length, format compliance, and absence of prohibited language. Model grading evaluates readability, accuracy of summarization, and brand voice consistency. Each prompt version is scored and compared, allowing the team to confidently roll out improvements.
Data extraction and structuring
A legal tech company uses prompts to extract key clauses from contracts. The evaluation dataset contains annotated contracts where the correct extractions are known. Code grading checks whether the extracted fields match the ground truth - clause type, parties involved, dates, monetary amounts. Model grading evaluates whether the extracted context is complete and correctly interpreted. Precision and recall metrics are computed automatically, giving the team clear performance targets.
Code generation and developer tools
A developer tools company uses prompts to generate code from natural language descriptions. The evaluation dataset contains programming tasks with known solutions. Code grading runs the generated code against test suites to verify correctness. Additional code checks measure syntax validity, adherence to style guides, and absence of security vulnerabilities. Model grading evaluates code readability and documentation quality.
Retrieval-augmented generation
A knowledge management platform uses prompts that incorporate retrieved documents to answer user questions. The evaluation dataset tests both retrieval quality and answer quality. Code grading verifies that the answer cites the correct source documents and does not hallucinate facts not present in the retrieved context. Model grading evaluates answer completeness and coherence.
Classification and routing
A financial services company uses prompts to classify customer requests and route them to the appropriate department. The evaluation dataset contains labeled requests spanning every category. Code grading computes classification accuracy, precision, and recall for each category. This is one of the few use cases where code-based grading alone may be sufficient, since the output space is finite and well-defined.
Safety and compliance
Any organization deploying language models in sensitive contexts - healthcare, finance, education, government - needs evaluation pipelines specifically designed to test safety boundaries. The evaluation dataset includes adversarial prompts designed to elicit harmful, biased, or non-compliant responses. Code grading checks for prohibited content and PII exposure. Model grading evaluates whether responses appropriately decline harmful requests while remaining helpful for legitimate ones.

---

Building an evaluation practice
Starting with prompt evaluation does not require sophisticated tooling. Begin with a spreadsheet of 30 test cases, a simple script that runs them through your prompt, and a grading function that scores the outputs. This minimal setup will immediately surface issues you did not know existed.
As your needs grow, adopt or build tooling that automates the pipeline: dataset management, batch execution, grading, scoring, and version comparison. Several open-source frameworks and commercial platforms exist for this purpose, and the right choice depends on your scale and requirements.
The most important step is the first one: deciding that evaluation is not optional. Every prompt that matters - every prompt that touches users, handles data, or makes decisions - deserves to be evaluated. The teams that internalize this discipline ship better products, catch problems earlier, and iterate with confidence.
Prompt engineering gets you started. Prompt evaluation is what gets you to production.