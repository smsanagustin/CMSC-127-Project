CREATE TABLE IF NOT EXISTS user(user_id INT(10) NOT NULL AUTO_INCREMENT, name VARCHAR(50) NOT NULL, username VARCHAR(18) NOT NULL, password VARCHAR(16) NOT NULL, CONSTRAINT user_id_pk PRIMARY KEY(user_id));
CREATE TABLE IF NOT EXISTS expense(expense_id INT(10) NOT NULL AUTO_INCREMENT,total_value DECIMAL(7,2) NOT NULL,date_incurred DATE, isSettled BOOLEAN,
    split_method VARCHAR(6) NOT NULL CHECK (split_method IN ('custom', 'equal')),
    cash_flow INT(10),
    expense_name VARCHAR(60) NOT NULL,
    user_id INT(10) NOT NULL,
    friend_id INT(10),
    CONSTRAINT fk_expense_userid FOREIGN KEY (user_id) REFERENCES user (user_id),
    CONSTRAINT fk_expense_friendid FOREIGN KEY (friend_id) REFERENCES user (user_id),
    CONSTRAINT expense_id_pk PRIMARY KEY(expense_id)
);
CREATE TABLE IF NOT EXISTS grp(
    group_id INT(10) NOT NULL AUTO_INCREMENT,
    group_name VARCHAR(60) NOT NULL,
    CONSTRAINT group_id_pk PRIMARY KEY(group_id)
);
CREATE TABLE IF NOT EXISTS group_has_expense(
    group_id INT(10) NOT NULL, 
    expense_id INT(10) NOT NULL,
    user_id INT(10) NOT NULL, 
    cash_flow DECIMAL(5,2) NOT NULL, 
    CONSTRAINT fk_group_id FOREIGN KEY (group_id) REFERENCES grp (group_id),
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES user (user_id),
    CONSTRAINT group_has_expense_groupid_expenseid_userid UNIQUE(group_id, expense_id,user_id)
);
CREATE TABLE IF NOT EXISTS friendsWith(
    user1 INT(10) NOT NULL,
    user2 INT(10) NOT NULL,
    CONSTRAINT fk_user1 FOREIGN KEY (user1) REFERENCES user (user_id),
    CONSTRAINT fk_user2 FOREIGN KEY (user2) REFERENCES user (user_id),
    CONSTRAINT friendsWith_user1_user2 UNIQUE(user1,user2)
);
CREATE TABLE IF NOT EXISTS belongsTo(
    user_id INT(10) NOT NULL,
    group_id INT(10) NOT NULL,
    CONSTRAINT fk_belongsto_user_id FOREIGN KEY (user_id) REFERENCES user (user_id),
    CONSTRAINT fk_belongsto_group_id FOREIGN KEY (group_id) REFERENCES grp (group_id),
    CONSTRAINT belongsTo_user_id UNIQUE(`user_id`, `group_id`)
);