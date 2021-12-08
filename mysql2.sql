use geneed;
drop procedure if exists updateRecommend;
DELIMITER $$
create procedure updateRecommend(
	user_id int,
    fav_symbol varchar(8)
)
begin
	declare done int default 0;
    declare recmd_gene varchar(8);
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
    declare continue handler for not found set done = 1;
    open genecur;
    rp: repeat
		fetch genecur into recmd_gene;
        if recmd_gene != fav_symbol then
			insert ignore into recommend values (user_id, recmd_gene);
		end if;
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