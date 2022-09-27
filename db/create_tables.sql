
-- Please be sure to first create the database!

CREATE TABLE IF NOT EXISTS public.repositories
(
	id bigint NOT NULL,
	name CHARACTER varying(400),
  description TEXT,
	html_url CHARACTER varying(450),
	clone_url CHARACTER varying(450),
	ssh_url CHARACTER varying(450),
	git_url CHARACTER varying(450),
	stars bigint,
	forks bigint,
	watchers bigint,
  issues bigint,
  created date,

	CONSTRAINT repositories_pkey PRIMARY KEY (id)
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.repositories
	OWNER TO postgres;

-- Create m2m mapping for repositories and programming languages
CREATE TABLE IF NOT EXISTS public.programming_languages
(
	id SERIAL PRIMARY KEY,
	name character varying(30) COLLATE pg_catalog."default" NOT NULL
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.programming_languages
    OWNER to postgres;


CREATE TABLE IF NOT EXISTS public.repositories_programming_languages
(
	id SERIAL PRIMARY KEY,
	repository_id bigint NOT NULL,
	programming_language_id bigint NOT NULL,
	CONSTRAINT fk_rpl_repository FOREIGN KEY (repository_id) REFERENCES repositories(id),
	CONSTRAINT fk_rpl_language FOREIGN KEY (programming_language_id) REFERENCES programming_languages(id)
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.repositories_programming_languages
    OWNER to postgres;


-- Create m2m mapping for repositories and topics
CREATE TABLE IF NOT EXISTS public.topics
(
	id SERIAL PRIMARY KEY,
	name CHARACTER VARYING(50)
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.topics
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public.repo_topics
(
  id SERIAL PRIMARY KEY,
  repository_id BIGINT NOT NULL,
  topic_id BIGINT NOT NULL,
  CONSTRAINT fk_topic_repository FOREIGN KEY (repository_id) REFERENCES repositories(id),
	CONSTRAINT fk_repository_topic FOREIGN KEY (topic_id) REFERENCES topics(id)
)
WITH (
  OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.repo_topics OWNER TO postgres;

-- Create the analysis table
CREATE TABLE IF NOT EXISTS public.analyses
(
  id SERIAL PRIMARY KEY,
  date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  repo_extraction_sql CHARACTER VARYING(1000),
  completed BOOLEAN DEFAULT false
)
WITH (
  OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.analyses OWNER TO postgres;

-- Associate repositories with analysis
CREATE TABLE IF NOT EXISTS public.analysis_repo
(
  id SERIAL PRIMARY KEY,
  analysis_id BIGINT NOT NULL,
  repository_id BIGINT NOT NULL,
  repo_head character varying(40),
  completed BOOLEAN DEFAULT false,
  CONSTRAINT fk_analysis_repo FOREIGN KEY (analysis_id) REFERENCES analyses(id),
  CONSTRAINT fk_repo_analysis FOREIGN KEY (repository_id) REFERENCES repositories(id)
)
WITH (
  OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.analysis_repo OWNER TO postgres;
