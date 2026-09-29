# Instructions for Workshop Organizers

These instructions are from ACL 2026 Publication Chairs. 

It is the responsibility of workshop organisers to prepare the workshop volume.

For each workshop, the idea is to build something similar to workshop volumes that are visible here: https://aclanthology.org/events/acl-2025/

The entire publication process relies on ACLPUB2 to build all the ACL volumes. Given the PDFs of each paper and some YAML files, the tool can make the volume with all the information.

It is your responsibility:
1. Collect the PDFs (you can use OpenReview API, see the documentation for aclpub2)
2. You should also check if papers follow the correct ACL template using this tool: https://github.com/acl-org/aclpubcheck 
3. For papers that have problems with the ACL template, you ask the authors to fix the paper
4. Collect copyright forms 
    You should send an email to all authors asking them to submit the copyright forms (https://github.com/acl-org/ACLPUB/blob/master/templates/copyright/acl-copyright-transfer-2021.pdf). Then, you must create a folder named "attachments" and put all the copyright forms named <paper_ID>.pdf into it.
5. Compile the YAML files required for building the volume (see the documentation for aclpub2 and this guide https://zeerak.org/workshops )
6. Upload all files on GitHub following the directories and files structure described in aclpub2 (an example is available here https://github.com/rycolab/aclpub2/tree/main/examples/sigdial )

As publication chairs, we will compile the volume by running ACLPUB2 on your files. Once everything is in order, we will upload the volume to the ACL Anthology.

Info about how to compile YAML files:
- https://zeerak.org/workshops 
- https://github.com/rycolab/aclpub2 

For questions about workshop volumes, contact:
- Jan Niehues jan.niehues@kit.edu




