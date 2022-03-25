CREATE TRIGGER cleanDuplicates
ON tweetTest
AFTER INSERT AS
DELETE T
FROM
(
Select *, dupRank = ROW_NUMBER() OVER (PARTITION BY tweetContent ORDER BY (SELECT NULL)) FROM tweetTest) AS T
WHERE dupRank > 1
select * from tweetTest