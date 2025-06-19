package org.assignment.bi_backend.Service;

import org.assignment.bi_backend.Entity.NewsMetadata;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.jdbc.core.BatchPreparedStatementSetter;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Component
public class NewsMetadataLoader {
//    private static final Map<String, NewsMetadata> metadataMap = new HashMap<>();

    @Value("${news.file.path}")
    private String path;

    @Autowired
    private ResourceLoader resourceLoader;

    @Autowired
    private JdbcTemplate jdbc;

    private static final String INSERT_SQL =
            "INSERT IGNORE INTO news_metadata(news_id, title, content, category, topic, title_length, content_length, create_time) " +
                    "VALUES (?,?,?,?,?,?,?,?)";

    @PostConstruct
    public void load() {
        // 1. 先加载已有 IDs，避免重复插入
        Set<String> existingIds = new HashSet<>(
                jdbc.queryForList("SELECT news_id FROM news_metadata", String.class)
        );

        Resource resource = resourceLoader.getResource(path);
        if (!resource.exists() || !resource.isReadable()) {
            throw new IllegalStateException("新闻元数据文件不存在或不可读: " + path);
        }

        List<NewsMetadata> toSave = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(resource.getInputStream(), StandardCharsets.UTF_8))) {
            String header = br.readLine();
            if (header == null) {
                throw new IllegalStateException("新闻元数据文件为空: " + path);
            }

            String line;
            int lineNum = 1;
            while ((line = br.readLine()) != null) {
                lineNum++;
                if (line.trim().isEmpty()) continue;

                String[] parts = line.split("\t");
                if (parts.length < 5) continue;

                String newsId = parts[0].trim();
                if (existingIds.contains(newsId)) {
                    continue; // 已存在，跳过
                }

                try {
                    // Expect columns: News ID, Category, Topic, Headline, News body
                    NewsMetadata m = getNewsMetadata(parts, newsId);

//                    metadataMap.put(newsId, m);
                    toSave.add(m);
                    existingIds.add(newsId);
                } catch (Exception ex) {
                    // 单行解析出错，打印日志继续
                    System.err.println("解析第 " + lineNum + " 行时出错: " + ex.getMessage());
                }
            }
        } catch (Exception e) {
            throw new RuntimeException("Failed to load news metadata", e);
        }

        if (!toSave.isEmpty()) {
            jdbc.batchUpdate(INSERT_SQL, new BatchPreparedStatementSetter() {
                @Override
                public void setValues(PreparedStatement ps, int i) throws SQLException {
                    NewsMetadata m = toSave.get(i);
                    ps.setString(1, m.getNewsId());
                    ps.setString(2, m.getTitle());
                    ps.setString(3, m.getContent());
                    ps.setString(4, m.getCategory());
                    ps.setString(5, m.getTopic());
                    ps.setInt(6, m.getTitleLength());
                    ps.setInt(7, m.getContentLength());
                    ps.setTimestamp(8, null);
                }

                @Override
                public int getBatchSize() {
                    return toSave.size();
                }
            });
        }
    }

    private static NewsMetadata getNewsMetadata(String[] parts, String newsId) {
        String category = parts[1].trim();
        String topic = parts[2].trim();
        String headline = parts[3].trim();
        String content = parts[4].trim();

        NewsMetadata m = new NewsMetadata();
        m.setNewsId(newsId);
        m.setCategory(category);
        m.setTopic(topic);
        m.setTitle(headline);
        m.setContent(content);
        m.setTitleLength(headline.length());
        m.setContentLength(content.length());
        m.setNewsCreateTime(null);
        return m;
    }

//    public NewsMetadata get(String newsId) {
//        return metadataMap.get(newsId);
//    }
}
