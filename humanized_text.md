If you want Claude to reliably strip the "AI voice" out of text, you can't just tell it to "write like a human." That means nothing to an LLM. Instead, you have to build a system that teaches it to think in two passes: diagnosis and reconstruction.

The first pass is purely diagnostic. You have it scan for the usual suspects—words like "leverage," "robust," or "delve." It needs to flag monotonous sentence lengths and lock down hard facts like names and dates so they don't get hallucinated away.

Then comes reconstruction. Claude rewrites the draft based on that diagnosis. It varies the rhythm, swaps abstract verbs for concrete ones, and trashes any obvious template structures, all while keeping the protected facts intact.

But here's the trick: don't just give it rules. Give it reference materials.

Set up a folder with a rubric defining your exact criteria for "human enough." Add a library of before-and-after edits, a categorized hit list of taboo AI-isms, and strict rules for preserving facts.

Then, write scripts to validate the output. Did it drop a number? Did a banned phrase slip through? Is the readability score right? Did it change the original meaning too much?

The main Skill file just routes traffic. It takes the input, runs the two passes against your reference materials, and validates the result.

"Write better" is vague. "Score above a 4 on natural rhythm, drop these 17 specific phrase patterns, and keep sentence variance between 8 and 25 words" is executable. Once you build it this way, it stops being a prompt and becomes a system. When you notice a new AI tic, you just update your reference files.