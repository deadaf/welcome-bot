-- drop table if exists welcome;

create table if not exists welcome (
    guild_id bigint primary key,
    channel_id bigint not null,
    message varchar(255) not null default 'Welcome **{user}** to **{guild}**!'
);
