-- Read-side views, created by `tools/kb.py build` after the tables.
-- The `entities` view (union of every entity table) is generated automatically from schema/tables.yaml.
-- Each view starts with a "-- view: <name> — <description>" line; SCHEMA.md is generated from those lines.

-- view: v_governments — Governments with head's name and governing / supporting parties (comma lists; check government_parties for dates).
CREATE VIEW v_governments AS
SELECT g.*,
       p.name AS head_name,
       (SELECT string_agg(gp.party_id, ', ' ORDER BY gp.party_id) FROM government_parties gp
         WHERE gp.government_id = g.government_id AND gp.role = 'governing') AS governing_parties,
       (SELECT string_agg(gp.party_id || ' (' || gp.role || ')', ', ' ORDER BY gp.party_id) FROM government_parties gp
         WHERE gp.government_id = g.government_id AND gp.role <> 'governing') AS support_parties
FROM governments g
LEFT JOIN people p ON p.person_id = g.head_person_id;

-- view: v_entity_context — Each dated entity with the local, regional and state government in office on its date (ASOF join).
CREATE VIEW v_entity_context AS
WITH e AS (
    SELECT id, type, title, date, jurisdiction_id,
           split_part(jurisdiction_id, '-', 1) AS state_id,
           CASE WHEN len(string_split(jurisdiction_id, '-')) >= 2
                THEN split_part(jurisdiction_id, '-', 1) || '-' || split_part(jurisdiction_id, '-', 2) END AS region_id
    FROM entities
    WHERE date IS NOT NULL AND jurisdiction_id IS NOT NULL
)
SELECT e.id, e.type, e.title, e.date, e.jurisdiction_id,
       g.government_id, g.head_name, g.governing_parties,
       rg.government_id AS regional_government_id, rg.head_name AS regional_head_name, rg.governing_parties AS regional_governing_parties,
       sg.government_id AS state_government_id, sg.head_name AS state_head_name, sg.governing_parties AS state_governing_parties
FROM e
ASOF LEFT JOIN v_governments g  ON e.jurisdiction_id = g.jurisdiction_id AND e.date >= g.valid_from
ASOF LEFT JOIN v_governments rg ON e.region_id       = rg.jurisdiction_id AND e.date >= rg.valid_from
ASOF LEFT JOIN v_governments sg ON e.state_id        = sg.jurisdiction_id AND e.date >= sg.valid_from;

-- view: v_vote_party — Position of each party in each vote (summed over groups). split = the party's deputies did not all vote alike.
CREATE VIEW v_vote_party AS
SELECT v.vote_id, v.date, v.jurisdiction_id, v.chamber, v.legislature_id, v.object, v.bundled,
       v.title, v.result, v.initiative_id, r.party_id,
       sum(r.yes) AS yes, sum(r.no) AS no, sum(r.abstain) AS abstain, sum(r.absent) AS absent,
       CASE WHEN sum(r.yes) + sum(r.no) + sum(r.abstain) = 0 THEN 'absent'
            WHEN sum(r.yes) >= greatest(sum(r.no), sum(r.abstain)) THEN 'yes'
            WHEN sum(r.no) >= sum(r.abstain) THEN 'no'
            ELSE 'abstain' END AS position,
       ((sum(r.yes) > 0)::INT + (sum(r.no) > 0)::INT + (sum(r.abstain) > 0)::INT) > 1 AS split
FROM vote_results r
JOIN votes v USING (vote_id)
WHERE r.party_id IS NOT NULL
GROUP BY ALL;

-- view: v_party_actions — Everything a party did: its position in each vote plus every entity where it appears as actor (author, implementer...).
CREATE VIEW v_party_actions AS
SELECT party_id, date, 'vote' AS entity_type, vote_id AS entity_id, title,
       position AS role_or_position, object AS detail, bundled
FROM v_vote_party
UNION ALL
SELECT a.party_id, e.date, e.type, e.id, e.title, a.role, NULL, NULL
FROM entity_actors a
JOIN entities e ON e.id = a.entity_id;

-- view: v_promises — Promises with party, election and number of evidence links.
CREATE VIEW v_promises AS
SELECT pr.*, pg.party_id, pg.election_id,
       (SELECT count(*) FROM promise_outcomes o WHERE o.promise_id = pr.promise_id) AS n_evidence
FROM promises pr
LEFT JOIN programs pg ON pg.id = pr.program_id;

-- view: v_claims — Knowledge claims with counts of supporting / contradicting studies and best evidence grade (A best).
CREATE VIEW v_claims AS
SELECT c.claim_id, c.statement, c.strength, c.consensus, c.scope, c.entity_id AS note_id, k.path,
       count(ce.study_id) FILTER (WHERE ce.direction = 'supports')                 AS n_supporting,
       count(ce.study_id) FILTER (WHERE ce.direction = 'contradicts')              AS n_contradicting,
       count(ce.study_id) FILTER (WHERE ce.direction IN ('mixed', 'null_result'))  AS n_mixed_or_null,
       min(s.evidence_grade) AS best_grade
FROM claims c
JOIN knowledge_notes k ON k.id = c.entity_id
LEFT JOIN claim_evidence ce ON ce.claim_id = c.claim_id
LEFT JOIN studies s ON s.id = ce.study_id
GROUP BY ALL;

-- view: v_indicators — Observations joined with their definition (name, unit, nominal/real, source).
CREATE VIEW v_indicators AS
SELECT i.*, d.name_es, d.name_en, d.unit, d.frequency, d.real_or_nominal, d.seasonally_adjusted, d.source_id
FROM indicators i
JOIN indicator_defs d USING (indicator_id);

-- view: v_topic_entities — Entities per topic including sub-topics (use: WHERE root_topic = 'housing').
CREATE VIEW v_topic_entities AS
WITH RECURSIVE tree(root_topic, topic_id) AS (
    SELECT topic_id, topic_id FROM topics
    UNION ALL
    SELECT tree.root_topic, t.topic_id FROM topics t JOIN tree ON t.parent_id = tree.topic_id
)
SELECT tree.root_topic, et.topic_id, e.*
FROM tree
JOIN entity_topics et ON et.topic_id = tree.topic_id
JOIN entities e ON e.id = et.entity_id;
