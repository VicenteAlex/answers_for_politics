# Licensing, attribution and sources

## Licences of this project

| Part | Licence | Text |
|---|---|---|
| Software: `tools/`, the `kb` and `kb.cmd` wrappers | **GNU AGPL-3.0** | [LICENSE](LICENSE) |
| Everything else: data (`data/`), knowledge content (`entries/`, `knowledge/`, `library/`), data model (`schema/`, `SCHEMA.md`) and documentation | **CC BY-SA 4.0** | [LICENSES/CC-BY-SA-4.0.txt](LICENSES/CC-BY-SA-4.0.txt) |

Both licences allow **commercial use**, provided that:
- **you give attribution**;
- **you share derivatives under the same licence**:
  - modified data or content under CC BY-SA 4.0;
  - modified software under AGPL-3.0. This also applies if you only run the modified software as a network service, for example a hosted MCP server.

Suggested attribution: *"Base de conocimiento política (contributors), CC BY-SA 4.0, &lt;repository URL&gt;"*, plus the original sources listed below when you reuse their data.

The licence covers this project's own work: selection, structure, classifications, summaries and analysis, and its own elaboration of the data. Facts, and the public data of the sources below, remain available from those sources under their own terms.

## Third-party sources and their conditions

| Source | Used for | Conditions |
|---|---|---|
| **Congreso de los Diputados** (open data) | Votes and each deputy's vote (`votes`, `vote_casts`), initiatives, deputies | Reuse allowed if the content is not altered and its meaning is not distorted, the source is cited and the date of last update is given ([aviso legal](https://www.congreso.es/es/cem/aviso-legal)). Each vote records its official `source_file`, `url` and `retrieved` date. Deputy-level records are kept as published. |
| **INE** | Statistical series (`indicators`) | Reuse allowed, including commercial, citing the source and the update date; CC BY 4.0 unless stated otherwise ([aviso legal](https://ine.es/dyngs/AYU/index.htm?cid=125)). Each series records its INE table and retrieval date. |
| **Eurostat** | Statistical series (`indicators`) | Free reuse, including commercial, with attribution and indication of changes ([copyright notice](https://ec.europa.eu/eurostat/help/copyright-notice)). |
| **BOE and official bulletins** | Laws, decrees, appointments, election results | Legal and official texts are not subject to intellectual property (art. 13 of the Spanish Ley de Propiedad Intelectual); cited per entry. |
| **Wikipedia** | Some election results and government data (rows whose `source_url` points to wikipedia.org, marked `verification: secondary`) | CC BY-SA 4.0: compatible with this project's data licence. Attribution is the linked article and revision. |
| **Studies, reports and press** | `library/` cards, dossiers, events | Cards are original summaries; short quotations are used under the quotation right (art. 32 LPI). The original works keep their own copyright; follow the links. |
| **Party programmes and statements** | Dossiers, `statements` | Short verbatim quotations with source, for analysis and criticism (art. 32 LPI). |

## Our own elaboration ("elaboración propia")

These are this project's work, not data published by the sources:
- the attribution of each deputy's vote to a party, in `vote_casts.party_id`, `vote_results` and `v_vote_party`;
- the classification of votes (`votes.object`);
- links between entities;
- graded claims;
- answers.

The party mapping and its sources are in `tools/congreso_party_map.csv`.

## Disclaimer

This knowledge base is built with the help of AI agents and reviewed only partially by humans. It may contain errors. It is not legal, financial or electoral advice. Check the cited primary sources before relying on any figure, and please report errors.
