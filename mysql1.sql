use geneed;
-- insert into users(username, password, is_admin)
-- values('zsa','zsa',1);

describe users;
-- create table recommend(
-- 	user_id int,
--     symbol varchar(8),
--     primary key (user_id, symbol),
--     foreign key (user_id) references users(id),
--     foreign key (symbol) references gene(symbol)
-- )
describe recommend;
-- describe protein;
-- describe gene;
-- describe gene;
-- describe protein;
-- 		select symbol 
--         from gene
--         where proteinId = (
-- 			select proteinId from gene
--             where symbol = 'LTBP2'
--         );
-- select symbol 
-- from gene join protein using (proteinId)
-- group by proteinId
-- having count(*) > 1
-- use geneed;
-- CREATE TABLE favorites(
--     user_id int,
--     symbol VARCHAR(8),
--     createDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
--     FOREIGN KEY (symbol) REFERENCES gene (symbol) ON DELETE CASCADE
-- );
describe favorites;
-- select * from favorites;

-- select * from users where id = 9;
update users set is_admin = 0 where id = 9;
select * from users where id = 9;
delete from recommend where user_id = 9;
select * from recommend;
-- show triggers from geneed;
-- drop trigger afterLike;
