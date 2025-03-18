-- Up migration
ALTER TABLE users
ADD COLUMN hashed_password VARCHAR(255) NOT NULL;

-- Down migration
ALTER TABLE users
DROP COLUMN hashed_password;
