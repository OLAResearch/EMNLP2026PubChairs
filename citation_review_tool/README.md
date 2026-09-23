# Citation Review Tool

Tools for checking citations that GPTZero flagged as possibly hallucinated. The work is split between annotators by paper. Each annotator labels every flagged reference in their papers, and everyone's labels are then combined into one CSV.

Everything runs locally and works offline. The data never leaves your machine.


## Workflow

### 1. Split the papers

```bash
python3 split_papers.py results.csv              # two annotators (default)
python3 split_papers.py results.csv -n 3         # three annotators
```

The script writes `results_annotator1.csv`, `results_annotator2.csv`, … next to the input. The input CSV can have any name.

All citations of a paper go to the same annotator. Papers are assigned so that each annotator gets about the same number of papers and the same number of citations.

### 2. Review your share

1. Open `citation_review.html` in a browser, by double-clicking it or by serving the folder:
   ```bash
   python3 -m http.server 8765
   # then open http://127.0.0.1:8765/citation_review.html
   ```
2. On the start screen, drop **your** annotator CSV onto the page, or click **Choose CSV**.
3. Type your name in the **Annotator name** box at the top right. Every label you add is stamped with it.
4. Label every citation (see [Using the page](#using-the-page)), then click **Export CSV** and send the file to whoever is combining the results.

### 3. Combine the results

1. Load the **full** original CSV (`flagged_papers_fake_citations.csv`) in the page.
2. Click **Import annotations** once for each annotator's export.
3. Click **Export CSV**.

The result is a single file with every label. Use the sidebar filter **Papers with unlabeled citations** to check that nothing was missed.

## Input format

The page expects the flagged-citation CSV exported from GPTZero, or a share of it produced by `split_papers.py`, with one row per flagged citation. It uses these columns:

| Column(s) | Used for |
|---|---|
| `paper_id`, `paper_title`, `document_name` | Grouping citations by paper |
| `citation_id`, `citation_text` | The reference as it appears in the paper |
| `citation_*` (title, authors, url, doi, arxiv_id, publication_date, publisher) | Fields the checker read from the reference |
| `source_*` (same fields) | The closest real source the checker found |
| `*_match`, `*_match_justification` | The checker's per-field verdict and its reason |
| `citation_scan_url` | Link to the GPTZero scan |

## Using the page

- **Sidebar:** one entry per paper, with how many citations you've labeled and how many you've marked hallucinated. You can search by paper ID, title or citation text, and filter by status:
  - all papers;
  - papers with unlabeled citations;
  - fully labeled papers;
  - papers with confirmed hallucinations.
- **Citation cards:** each card shows the reference, then a table comparing it with the closest source the checker found. Each field has a match badge (`match`, `partial/weak match`, `no match`, `unknown`); hover a badge to see the checker's reason. If the checker found no source at all, the card says so.
- **Lookup links:** Google Scholar, Semantic Scholar, DBLP, Google and the GPTZero scan, for checking a reference yourself. The paper header also links to the paper's OpenReview page.
- **Labels:** each citation gets one of these:
  - **Hallucinated:** the reference doesn't exist.
  - **Likely hallucinated:** strong signs that it's fake, but you couldn't confirm it.
  - **Real (false positive):** the reference exists, perhaps with small metadata errors.
  - **Unsure:** needs a second opinion.

  Each citation also has a free-text notes box, for example for the correct reference.
- **Paper verdict:** a dropdown and notes box for each paper, with these options:
  - No action
  - Minor: ask authors to fix
  - Serious: escalate
  - Needs second look

### Keyboard shortcuts

| Key | Action |
|---|---|
| `1` / `2` / `3` / `4` | Label the current citation (Hallucinated / Likely / Real / Unsure) and move to the next one |
| `0` | Clear the current label |
| `j` / `k` | Next / previous citation |
| `n` / `p` | Next / previous paper in the filtered list |
| `Esc` | Leave a text box so the shortcuts work again |

## Saving your work

- **Autosave:** labels are saved in the browser you're using (local storage). They survive a page reload, but not a switch to another browser or machine, or clearing your site data.
- **Export CSV:** downloads all the original columns plus these ones:
  - `annotation_label`
  - `annotation_note`
  - `annotation_by`
  - `annotation_at`
  - `paper_verdict`
  - `paper_note`

  The file name includes your annotator name and the date. Export regularly: the exported file is the only lasting copy of your work.
- **Import annotations:** loads a previously exported CSV. Use it to resume on another machine or to combine annotators' work. Rows are matched on `paper_id` + `citation_id`, and imported labels overwrite existing labels for the same citation.

## Privacy

The CSVs contain confidential submission data. The page makes no network requests with them: nothing is uploaded, and the lookup links open only when you click them. Share the CSVs and exports only through your usual confidential channels.
