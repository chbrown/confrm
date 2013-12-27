package main

type User struct {
    Id int64
    Email string
    Password NullString
    FirstName NullString
    MiddleName NullString
    LastName NullString
    AllEmails NullString
    Classification NullString
    Institution
    Department NullString
    International NullBool
    Notes NullString
    Url NullString
    Photo NullString
    Biography NullString
    Superuser bool DEFAULT false NOT NULL,
    Tags NullString

    Created int64
    CreatedById NullInt64
    Archived NullInt64
    ArchivedById NullInt64
    Deleted NullInt64
    DeletedById NullInt64
}

type Group struct {
    Id int64
    Name string
    Tags NullString

    Created int64
    CreatedById int64
    Archived NullInt64
    ArchivedById NullInt64
    Deleted NullInt64
    DeletedById NullInt64
}

type File struct {
    Id int64
    Filename string
    Tags NullString

    Created int64
    CreatedById int64
    Archived NullInt64
    ArchivedById NullInt64
    Deleted NullInt64
    DeletedById NullInt64
}

type Message struct {
    Id int64
    Subject string
    Body string
    GroupId NullInt64
    Tags NullString

    Created int64
    CreatedById int64
    Archived NullInt64
    ArchivedById NullInt64
    Deleted NullInt64
    DeletedById NullInt64
}

type Organization struct {
    Id int64
    Slug string
    Name string

    Created int64
    CreatedById int64
}

type UserSession struct {
    Id int64
    UserId int64
    Ticket string
    IpAddress NullString
    UserAgent NullString

    Created int64
    Deleted NullInt64
}
