use geneed;
drop procedure if exists updateRecommend;
DELIMITER $$
create procedure updateRecommend(
	user_id int,
    fav_symbol varchar(8)
)
begin
	declare done int default 0;
    declare recmd_gene1 varchar(8);
    declare recmd_gene2 varchar(8);
    declare recmd_gene3 varchar(8);
    declare genecur cursor for (
		select symbol 
        from gene
        where proteinId = (
			select proteinId from gene
            where symbol = fav_symbol
        )
        union
        select symbol
        from gene join protein using (proteinId)
        group by proteinId
        having avg(popularity) > 5
    );

    declare favcur cursor for (
        -- pick genes that other users liked
        select symbol from (
        select symbol, count(user_id) as numLikes
        from favorites 
        where user_id in (
            select user_id
            from favorites
            where symbol = fav_symbol
        )
        and symbol <> fav_symbol
        group by symbol
        order by numLikes
        limit 3) as t2
    );

    declare namecur cursor for (
        -- similar full names
        select symbol
        from gene
        where fullName like 
        concat('%', substring_index(
            (select fullName
            from gene
            where symbol = fav_symbol), ' ', 1
        ), '%')
        and symbol <> fav_symbol
        union
        -- similar disease names
        select symbol
        from gene natural join protein natural join disease
        where diseaseName like
        concat('%', substring_index(
            (select diseaseName
            from gene natural join protein natural join disease
            where symbol = fav_symbol
            ), '-', 1), '%')
        and symbol <> fav_symbol
    );

    declare continue handler for not found set done = 1;
    open genecur;
    open favcur;
    open namecur;
    rp: repeat
		fetch genecur into recmd_gene1;
        fetch favcur into recmd_gene2;
        fetch namecur into recmd_gene3;
        if recmd_gene1 != fav_symbol then
			insert ignore into recommend values (user_id, recmd_gene1);
		end if;
        insert ignore into recommend values (user_id, recmd_gene2);
        insert ignore into recommend values (user_id, recmd_gene3);
		until done
	end repeat;
    close genecur;


end$$
DELIMITER ;

drop trigger if exists afterLike;
DELIMITER $$
create trigger afterLike
after insert on favorites
for each row
begin
	set @is_admin = (
		select is_admin from users
		where id = new.user_id
	);
    if @is_admin != 1 or @is_admin is null then
		delete from recommend
        where user_id = new.user_id;
        call updateRecommend(
			new.user_id,
            new.symbol
        );
	end if;
end$$    
DELIMITER ;