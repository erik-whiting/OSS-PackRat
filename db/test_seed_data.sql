INSERT INTO repositories (
  id,
  name,
  description,
  html_url,
  clone_url,
  ssh_url,
  git_url,
  stars,
  forks,
  watchers,
  issues,
  created
)
VALUES (
  100,
  'TestRepo',
  'This is a record in the repositories table, it is not a real repository',
  'https://fake.website',
  'https://fake.website',
  'https://fake.website',
  'https://fake.website',
  100,
  10,
  20,
  4,
  CURRENT_TIMESTAMP
);

INSERT INTO programming_languages (id, name) VALUES (
  1,
  'C'
);

INSERT INTO repositories_programming_languages (
  repository_id,
  programming_language_id
)
VALUES (
  100,
  1
);

INSERT INTO topics (id, name) VALUES (10, 'Tests');

INSERT INTO repo_topics (
  repository_id,
  topic_id
)
VALUES (
  100,
  10
);
