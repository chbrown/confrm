-- DB=confrm_dev; dropdb $DB; createdb $DB && psql $DB < schema.sql
CREATE TABLE users (
    id serial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text,
    first_name text,
    middle_name text,
    last_name text,
    all_emails text,
    classification text,
    institution text,
    department text,
    international boolean,
    notes text,
    url text,
    photo text,
    biography text,
    superuser boolean DEFAULT false NOT NULL,
    tags text,
    -- json text,
    created timestamp DEFAULT current_timestamp,
    created_by_id integer references users(id),
    archived timestamp,
    archived_by_id integer references users(id),
    deleted timestamp,
    deleted_by_id integer references users(id)
);
CREATE TABLE groups (
    id serial PRIMARY KEY,
    name text NOT NULL,
    tags text,
    -- json text,
    created timestamp DEFAULT current_timestamp,
    created_by_id integer references users(id) NOT NULL,
    archived timestamp,
    archived_by_id integer references users(id),
    deleted timestamp,
    deleted_by_id integer references users(id)
);
CREATE TABLE files (
    id serial PRIMARY KEY,
    filename text NOT NULL,
    tags text,
    -- json text,
    created timestamp DEFAULT current_timestamp NOT NULL,
    created_by_id integer references users(id) NOT NULL,
    archived timestamp,
    archived_by_id integer references users(id),
    deleted timestamp,
    deleted_by_id integer references users(id)
);
CREATE TABLE files_groups (
    id serial PRIMARY KEY,
    file_id integer references files(id) NOT NULL,
    group_id integer references groups(id) NOT NULL,
    owner boolean DEFAULT false NOT NULL
);
CREATE TABLE files_users (
    id serial PRIMARY KEY,
    file_id integer references files(id) NOT NULL,
    user_id integer references users(id) NOT NULL,
    owner boolean DEFAULT true NOT NULL
);
CREATE TABLE groups_users (
    id serial PRIMARY KEY,
    group_id integer NOT NULL,
    user_id integer NOT NULL,
    owner boolean DEFAULT false NOT NULL,

    created timestamp DEFAULT current_timestamp,
    created_by_id integer references users(id) NOT NULL,
    archived timestamp,
    archived_by_id integer references users(id),
    deleted timestamp,
    deleted_by_id integer references users(id)
);
CREATE TABLE messages (
    id serial PRIMARY KEY,
    subject text NOT NULL,
    body text NOT NULL,
    group_id integer references groups(id) NOT NULL,
    tags text,

    created timestamp DEFAULT current_timestamp,
    created_by_id integer references users(id) NOT NULL,
    archived timestamp,
    archived_by_id integer references users(id),
    deleted timestamp,
    deleted_by_id integer references users(id)
);
CREATE TABLE organizations (
    id serial PRIMARY KEY,
    slug text NOT NULL,
    name text NOT NULL,
    created timestamp DEFAULT current_timestamp,
    tags text,

    created timestamp DEFAULT current_timestamp,
    created_by_id integer references users(id) NOT NULL,
);
CREATE TABLE organizations_users (
    id serial PRIMARY KEY,
    organization_id integer references organizations(id) NOT NULL,
    user_id integer references users(id) NOT NULL,
    owner boolean DEFAULT false NOT NULL,
    tags text,

    created timestamp DEFAULT current_timestamp,
    created_by_id integer references users(id) NOT NULL,
    archived timestamp,
    archived_by_id integer references users(id),
    deleted timestamp,
    deleted_by_id integer references users(id)
);
CREATE TABLE user_sessions (
    id serial PRIMARY KEY,
    user_id integer references users(id) NOT NULL,
    ticket text NOT NULL,
    ip_address text,
    user_agent text,

    created timestamp DEFAULT current_timestamp,
    deleted timestamp
);
