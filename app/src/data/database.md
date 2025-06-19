```sql
-- ----------------------------
-- Table structure for user_behavior_0613_0617
-- ----------------------------
DROP TABLE IF EXISTS `user_behavior_0613_0617`;
CREATE TABLE `user_behavior_0613_0617`  (
  `event_id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `news_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `event_time` datetime(6) NOT NULL,
  `duration` int NOT NULL,
  PRIMARY KEY (`event_id`) USING BTREE,
  INDEX `idx_user`(`user_id`) USING BTREE,
  INDEX `idx_news`(`news_id`) USING BTREE,
  INDEX `idx_event_time`(`event_time`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;
```

```sql

-- ----------------------------
-- Table structure for news_metadata
-- ----------------------------
DROP TABLE IF EXISTS `news_metadata`;
CREATE TABLE `news_metadata`  (
  `news_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` tinytext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `topic` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `title_length` int NULL DEFAULT NULL,
  `content_length` mediumint UNSIGNED NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  PRIMARY KEY (`news_id`) USING BTREE,
  INDEX `idx_title`(`title`) USING BTREE,
  INDEX `idx_category`(`category`) USING BTREE,
  INDEX `idx_topic`(`topic`) USING BTREE,
  INDEX `idx_create_time`(`create_time`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;
```