# English edition — 2026-11-24

All Git-managed documentation, report text, annotations and notebook instructions are now English. Corresponding HTML reports were rebuilt from their complete English Markdown sources. Original experiment dates, numerical results, semantic labels, model weights and training logic are preserved. Existing parallel English was reused and the remaining translations were written directly by the assistant; third-party translation results were not used.

The original bilingual material remains recoverable from commit `f82bd685352c5f64b69ce1c6b080592ede059c97`. Additional local backups are outside the repository.

Some historical failed model generations contained Chinese fragments. Those fragments now have bracketed English explanations in display strings. **Do not rescore the localized strings as the original model generations.** Published metrics continue to describe the original predictions. The original UTF-8 strings are recoverable from the base64 records in [raw_output_originals.json](raw_output_originals.json), or directly from the source commit. No model was retrained or re-evaluated during localization.

Historical manifests and embedded scientific exports may describe original file hashes. The [localization manifest](ENGLISH_LOCALIZATION_2026-11-24.json) distinguishes original and English-edition hashes. Numerical JSON values are checked against the original commit. The complete original model ZIPs and original research directories remain preserved outside this English-only Git content.

This change is prepared as a new local commit named `update md file and code`; the owner will push it. No Hugging Face model contents are changed by this commit.
