# Publication Chairs Duty, Workflow, etc.


## Workflow

The workflow followed by the Publication Chairs is outlined below.

1. **Collect the camera-ready submissions.** Download the full set of camera-ready PDFs from OpenReview. An OpenReview client library is available for this purpose; however, no script for this step is currently available.
2. **Check formatting.** Run the ACLPUBcheck formatting check (https://github.com/acl-org/aclpubcheck) on all submissions.
    1. Note that the tool occasionally produces false positives, so flagged issues should be verified manually.
3. **Notify authors.** Contact the authors of flagged submissions and request that they resubmit a corrected version.
    1. There is a script to automate this.
4. **Collect the front matter.** Gather the additional materials separately, including the cover image, the message from the General Chair, the message from the Program Chairs, and other front matter.
5. **Build and publish the proceedings** once all submissions have passed the formatting check.

Two further points may be useful:

**Scope.** As a tradition, the Publication Chairs were responsible for the Main and Findings proceedings only. The proceedings of the other tracks (Demonstrations, Industry, Workshops, etc.) were compiled and published by the respective track chairs.

**Revision requests after publication.** After the proceedings were published, we received a large number of requests from authors to revise their papers. We informed them that revisions were no longer possible on our side and referred them to the ACL Anthology corrections process (https://aclanthology.org/info/corrections/).


## Instructions for chairs

Please refer to the information below. 

1. General information for chairs (workshop, demonstration, student research workshop, sponsorship, tutorial, general and program chairs): [`./instructions/instructions_for_chairs.md`](./instructions/instructions_for_chairs.md).
2. Instructions for workshop chairs: [`./instructions/Instructions_for_workshop_organizers.md`](./instructions/Instructions_for_workshop_organizers.md).

### EMNLP 2026 Publication Management

This Google spreadsheet is a tracking and management sheet for the EMNLP 2026 conference publications. 
It organizes the various proceedings, tracks, and volumes along with operational metadata required for publication.

**Field Descriptions**

1.  **Proceedings**
    
      * **Purpose:** The formal, full official title of the proceedings volume or publication track.
      * **Example Values:**
          * `Proceedings of the 2026 Conference on Empirical Methods in Natural Language Processing (Volume 1: Long Papers)`
          * `Findings of the Association for Computational Linguistics: EMNLP 2026`

2.  **Acronym**
    
      * **Purpose:** Short identifier or shorthand code used to distinguish each specific track/volume within submission platforms, file paths, or publication scripts.
      * **Example Values:** `emnlp_long`, `emnlp_short`, `demos`, `student_ws`, `tutorial`, `industry_track`, `findings`.

3.  **Google Drive link**
    
      * **Purpose:** Stores the URL or path to a shared folder or repository containing camera-ready files, PDFs, and materials for that track.

4.  **Venue Id**
    
      * **Purpose:** Venue identifier code used in indexing systems (such as the ACL Anthology) to group related tracks under a parent venue.
      * **Example Values:** `emnlp`, `findings`.

5.  **Contact person**
    
      * **Purpose:** Name of the publication chair, track chair, or manager responsible for overseeing that specific volume's publication process.

6.  **Contact e-mail**
    
      * **Purpose:** The email address of the assigned contact person for editorial queries or publication issues.

7.  **ISBN**
    
      * **Purpose:** The International Standard Book Number assigned to the published proceedings volume for cataloging and archival reference. This number will be obtained in the later publication stage. 

8.  **Self-correction?**
    
      * **Purpose:** A tracking flag (e.g., Yes/No) to indicate whether author self-corrections, post-accept errata, or camera-ready revisions are permitted or pending verification for that volume.

9.  **Notes**
    
      * **Purpose:** Free-form text field for administrative notes, special formatting rules, submission deadlines, or status updates specific to a track.

10. **Publication Status**
    
      * **Purpose:** Workflow tracking status indicating the current progress of the proceedings (e.g., *Draft*, *In Review*, *Camera-Ready Complete*, *Published*).