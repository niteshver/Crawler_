## Information for Submitters
General information for submitting proceedings to the ACL Anthology (for event chairs)
August 26, 2025
This page contains general information about submitting proceedings of a conference to the ACL Anthology. It is intended for publication chairs of main conferences and standalone events, who have the responsibility of delivering the proceedings for all main conference and workshop volumes to the Anthology director. **Chairs of workshops** attached to a larger conference should also read this page, but should work through their main conference publication chair instead of directly with the Anthology. It is also common for people to submit older proceedings or journals.
Please note that this document does not describe how to manage the submissions and review process, or even how to assemble proceedings from accepted papers. For complete information about the conference management process, especially for ACL conference publication chairs, please see 
## About Venues
A _venue_ in the ACL Anthology is a conference, workshop, journal, or other publication series that publishes _volumes_ of papers. The central venues in the ACL are the major ACL-operated **conferences** (ACL, AACL, EMNLP, NAACL, EACL, CoNLL) and **journals** (CL and TACL). We also host papers for many other **non-ACL** venues, for example, COLING, LREC, IJCNLP, NoDaLiDa, and AMTA. You can browse the full list of current venues.
We are happy to ingest and host material for **new venues**. We generally accept proceedings subject to the following conditions:
  * The venue publishes papers in the fields of computational linguistics or speech and natural language processing, broadly defined.
  * The venue has high standards, which generally means that it is peer-reviewed by experts in the field.
  * The venue organizers either sign over paper copyrights to the ACL (preferred), or sign an agreement allowing us to share the papers under a Creative Commons 


## Overview of the Submission Process
Please note the following important dates.  
| Deadline  | Step  |  
| --- | --- |  
| Before paper submission deadline  |  
| Before paper submission deadline  |  
| 2 weeks before publication  |  
| 2 weeks before publication  | Submit copyright transfer forms  |  
| After publication  |  
## Register your meeting
If you are a conference publications chair, you must register your intention to submit your proceedings. (Workshop chairs should do this through your main conference publication chair). This step requires you to send (a) the complete list of volumes that will be published in the Anthology (main conference volumes and workshops) and (b) the desired publication date. Your proceedings will be due no later than **two weeks** prior to this negotiated date.
This information should be submitted to us **Please do this as early as possible** , ideally well before the submission deadline. This will allow us to do a quick sanity check of the metadata. As noted above, if you are the chair of a workshop that is colocated with a larger event, please work with your main conference publication chair instead of directly with the Anthology.
Your Github issue should contain the following information for each volume.
  * **Venue identifier**. Each venue (conference or workshop) has a venue identifier. Its basic form is the conference acronym, such as ACL, NAACL, JEP/TALN/RECITAL, and so on. A ACL → acl, JEP/TALN/RECITAL → jeptalnrecital), and also forms a component of the Anthology ID. For existing venues, be sure to look up the venue’s existing identifier. New venues must have their venue identifier confirmed by the Anthology director (see subsection below). Note: a common mistake is to include the year in the venue identifier, e.g., ACL2020. This confuses a _meeting_ of a venue with the venue itself. The identifier should not have the year or meeting number in it.
  * **Volume title**. This is the title of the volume book that will be published, e.g., _Proceedings of the…_. We recommend you choose a name consistent with your prior years’ volumes. The full title should not contain abbreviations, except parenthetically. For example, “Proceedings of EMNLP 2019” is not a good title, but “Proceedings of the 2019 Meeting of the Conference on Empirical Methods in Natural Language Processing (EMNLP)” is a great one. If you have sub-volumes (e.g., long papers, short papers, demonstrations, tutorial abstracts), we suggest you append descriptors after the full volume name. For example, “Proceedings of the 2019 Meeting of the Conference on Empirical Methods in Natural Language Processing (EMNLP): Tutorial Abstracts”. But above all, you should also seek consistency with the names of your volumes from prior years.


**We emphasize** that if you are chairing a meeting attached as a satellite of a main conference (e.g., ACL or EMNLP), please do not communicate directly with the Anthology, but instead first work with your main conference publication chair(s), who will take care of registration and many of the details below.
### New venues
As noted above, the Anthology welcomes new ACL and non-ACL venues. If your venue is appearing for the first time in the Anthology, we need to assign it a venue identifier, as described above. You can choose one yourself, but it will require confirmation from the Anthology director. If you are submitting a new venue, please be sure to also include the following information:
  * **Venue name**. Each venue has a name. These names are attached to the venue identifier and stored in _not_ to put the year or meeting number in the venue name.
  * **Website**. The website of the venue. Ideally this is a website of the venue itself (e.g., 


## Submit your data
After your conference management software has collected all the camera-ready papers and associated attachments, you will arrange them into one of two formats.
  1. _ACLPUB_. If you’re using Softconf, this will likely be the original ACLPUB format, as described in the 
  2. _aclpub2_. More recently, ACL has moved to using 


If you are submitting multiple volumes (e.g., main conference volumes and workshops), please group each volume’s directory inside a single top-level folder for sharing. A link to this directory should be posted to the ingestion request Github issue you created, or alternately shared with the Anthology Director via email. We prefer sharing via HTTP, FTP, or a private GitHub repo since these allow automated downloads, but we can accommodate other methods, such as Dropbox or Google Drive. This sharing should be done **two weeks prior to your desired publication date** (which was negotiated when you first contacted us) to give us time to process it.
If you are using aclpub2, we suggest you run our 
The remaining steps are handled by Anthology staff and use 
  * We ingest that data by running additional scripts that convert it into our authoritative format, apply title-case protection, and disambiguate author names.
  * This becomes a pull request on 
  * Once approved and merged into the `master` branch, the site will be automatically rebuilt (which happens twice a day) and made live.


**Please note** that workshop chairs should handle this step through their main conference publication chair, and not directly with the Anthology.
## Copyright
If you are using the START system, this process is handled as part of the camera-ready submission process.
Otherwise, for copyright transfers, please use the form at:
Forms should be signed by authors and saved using the ACL Anthology identifiers as names. Please place these into a folder (e.g., `copyright-transfers/P11-1001.pdf`) and then deliver them in bulk to the Anthology Editor when submitting the proceedings. In aclpub2, copyrights should be listed as paper attachments with a type of ‘copyright’.
For both current and legacy events, it is good practice for the organizers to attempt to obtain copyright transfers for their materials, but we will ingest materials even if no copyright transfers are on file.
## ISBN Numbers
If you plan to publish or print your proceedings, you will need an ISBN. The ACL can provide these for *ACL conferences. Please provide the exact titles of each volume to be assigned an ISBN and send this information to Jennifer Rachford, the ACL Business Manager.
## Errata and Corrections
If you get requests from authors needing to post errata or revised versions of the papers, or supplemental attachments after the publication of the proceedings, please refer them to our documentation on the matter. Note that after the publication date, corrections can only be applied to individual papers; the full proceedings volumes will not be replaced or revised.
