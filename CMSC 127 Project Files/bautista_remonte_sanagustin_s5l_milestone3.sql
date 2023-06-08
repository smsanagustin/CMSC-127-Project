-- Bautista, Elvin Marc
-- Remonte, Jonathan Andre
-- San Agustin, Sophia Mae M.
-- CMSC 127 S-5L
-- GROUP 3

-- create database
CREATE DATABASE cmsc127group3;
-- use cmsc127group3;

-- create user table
CREATE TABLE user (
    user_id INT(10) NOT NULL AUTO_INCREMENT,   
    name VARCHAR(50) NOT NULL,
    username VARCHAR(18) NOT NULL,
    password VARCHAR(16) NOT NULL,
    CONSTRAINT user_id_pk PRIMARY KEY(user_id)
);

-- create expense table
CREATE TABLE expense(
    expense_id INT(10) NOT NULL AUTO_INCREMENT,
    total_value DECIMAL(5,2) NOT NULL,
    date_incurred DATE,
    isSettled BOOLEAN,
    split_method VARCHAR(6) NOT NULL CHECK (split_method IN ('custom', 'equal')),
    cash_flow INT(10),
    expense_name VARCHAR(60) NOT NULL,
    user_id INT(10) NOT NULL,
    friend_id INT(10),
    -- primary key
    CONSTRAINT fk_expense_userid FOREIGN KEY (user_id) REFERENCES user (user_id),
    CONSTRAINT fk_expense_friendid FOREIGN KEY (friend_id) REFERENCES user (user_id),
    CONSTRAINT expense_id_pk PRIMARY KEY(expense_id)
);

-- create group table
CREATE TABLE grp(
    group_id INT(10) NOT NULL AUTO_INCREMENT,
    group_name VARCHAR(60) NOT NULL,
    CONSTRAINT group_id_pk PRIMARY KEY(group_id)
);

-- create group_has_expense table
CREATE TABLE group_has_expense(
    group_id INT(10) NOT NULL, 
    expense_id INT(10) NOT NULL, 
    CONSTRAINT fk_group_id FOREIGN KEY (group_id) REFERENCES grp (group_id),
    CONSTRAINT fk_expense_id FOREIGN KEY (expense_id) REFERENCES expense (expense_id),
    CONSTRAINT group_has_expense_groupid_expenseid UNIQUE(group_id, expense_id)
);

-- create friendsWith table
CREATE TABLE friendsWith(
    user1 INT(10) NOT NULL,
    user2 INT(10) NOT NULL,
    CONSTRAINT fk_user1 FOREIGN KEY (user1) REFERENCES user (user_id),
    CONSTRAINT fk_user2 FOREIGN KEY (user2) REFERENCES user (user_id),
    CONSTRAINT friendsWith_user1_user2 UNIQUE(user1,user2)
);

CREATE TABLE belongsTo(
    user_id INT(10) NOT NULL,
    group_id INT(10) NOT NULL,
    CONSTRAINT fk_belongsto_user_id FOREIGN KEY (user_id) REFERENCES user (user_id),
    CONSTRAINT fk_belongsto_group_id FOREIGN KEY (group_id) REFERENCES grp (group_id),
    CONSTRAINT belongsTo_user_id UNIQUE(`user_id`, `group_id`)
);

-- populate the user tables
INSERT INTO user (name,username,password) VALUES("Jon Remonte", "jaremonte","passwordkoto");
INSERT INTO user (name,username,password) VALUES("Elvin Bautista", "ebautista","passwordkoto");
INSERT INTO user (name,username,password) VALUES("Mae SA", "jaremonte","passwordkoto");

-- user1 should be friends with user2 first before they can have a shared expense
INSERT INTO friendsWith (user1,user2) VALUES (1,2);
INSERT INTO friendsWith (user1,user2) VALUES (2,1);

INSERT INTO friendsWith (user1,user2) VALUES (2,3);


INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id,friend_id)
    VALUES (800, CURDATE(),0,"equal",400,"Trial Expense",1,2);

INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id,friend_id)
VALUES (800, CURDATE(),0,"equal",-400,"Trial Expense 2",1,2);

INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id,friend_id)
VALUES (900, "2023-05-25",0,"equal",900,"Trial Expense 3",1,2);

INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id,friend_id)
VALUES (900, "2021-05-25",0,"equal",900,"Trial Expense 4",1,2);

-- create group and add users to that group
INSERT INTO grp (group_name) VALUES ("Group 3 CMSC 127");
INSERT INTO grp (group_name) VALUES ("Remontenatics");

INSERT INTO belongsTo (user_id,group_id) VALUES (1,1);
INSERT INTO belongsTo (user_id,group_id) VALUES (2,1);
INSERT INTO belongsTo (user_id,group_id) VALUES (3,1);

-- create an expense without a friend (implying that is was made with a group)
INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id)
VALUES (900, CURDATE(),0,"equal",600,"1st Group Expense",1);

INSERT INTO group_has_expense (group_id,expense_id) VALUES (1,3);

-- search
SELECT user_id, name FROM user where name="Jon Remonte";
SELECT * FROM expense where expense_name="1st Group Expense";
SELECT * FROM grp where group_name="GROUP 3 CMSC 127";

-- delete a user
DELETE FROM friendsWith WHERE user2 = 3;
DELETE FROM belongsTo WHERE user_id = 3;
DELETE FROM user WHERE name = "Mae SA";

-- delete an expense
DELETE FROM expense WHERE expense_name = "Trial Expense 2";

-- delete a group
DELETE FROM grp WHERE group_name = "Remontenatics";

-- update user
UPDATE user
SET username = 'jaremonte123'
WHERE username = 'jaremonte';

-- update expense
UPDATE expense
SET isSettled = 1
WHERE expense_name = 'Trial Expense';
-- when updating an expense, need to create new if there is still a pending payment
-- update group
UPDATE grp
SET group_name = "Remontenatics 2"
WHERE group_id = 1;

-- View all expenses made within a month (by user with id 1)
SELECT * FROM expense WHERE user_id = 1 AND date_incurred IN (CURDATE(),DATE_SUB(CURDATE(), INTERVAL 1 MONTH));

-- View all expenses made with a friend
SELECT * FROM expense WHERE friend_id IS NOT NULL;

-- View all expenses made with a group
SELECT * FROM expense WHERE friend_id IS NULL;

--View current balance from all expenses (of the current user)
SELECT IF(SIGN(SUM(cash_flow))=1, 0, SUM(cash_flow)) as "Balance" FROM expense WHERE user_id = 1;

-- View all friends with outstanding balance
SELECT name FROM user JOIN expense 
    ON user.user_id=expense.friend_id 
    WHERE expense.user_id = 1 AND cash_flow > 0 AND expense.isSettled = 0 
GROUP BY expense.friend_id;

-- View all groups
SELECT * FROM grp;

-- View all group with outstanding balance
SELECT group_name FROM grp JOIN group_has_expense as `g`
    ON grp.group_id = g.group_id
    JOIN expense as `e`
    ON g.expense_id = e.expense_id
    JOIN belongsTo as `b`
    ON g.group_id = b.group_id AND b.user_id = 1 -- the user id should be the current user
    WHERE e.cash_flow > 0 AND e.isSettled = 0 GROUP BY grp.group_id;