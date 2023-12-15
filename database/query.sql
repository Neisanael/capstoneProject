CREATE TABLE `recipes` (
  `name` text DEFAULT NULL,
  `id` bigint(20) NOT NULL,
  `minutes` bigint(20) DEFAULT NULL,
  `contributor_id` bigint(20) DEFAULT NULL,
  `submitted` text DEFAULT NULL,
  `tags` text DEFAULT NULL,
  `nutrition` text DEFAULT NULL,
  `n_steps` bigint(20) DEFAULT NULL,
  `steps` text DEFAULT NULL,
  `description` text DEFAULT NULL,
  `ingredients` text DEFAULT NULL,
  `n_ingredients` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE user_recipe_ratings (
    id INT(11) NOT NULL AUTO_INCREMENT,
    user_id VARCHAR(255),
    recipe_id BIGINT(20),
    date DATE,
    rating INT(11),
    PRIMARY KEY (id),
    INDEX (recipe_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);